import os

import PIL.Image
import gradio as gr
import huggingface_hub
import numpy as np
import onnxruntime as rt
import pandas as pd

import globals
from tagger import dbimutils

SWIN_MODEL_REPO = "SmilingWolf/wd-v1-4-swinv2-tagger-v2"
CONV_MODEL_REPO = "SmilingWolf/wd-v1-4-convnext-tagger-v2"
CONV2_MODEL_REPO = "SmilingWolf/wd-v1-4-convnextv2-tagger-v2"
VIT_MODEL_REPO = "SmilingWolf/wd-v1-4-vit-tagger-v2"
MODEL_FILENAME = "model.onnx"
LABEL_FILENAME = "selected_tags.csv"

cur_model = None, None
tag_names = None
rating_indexes = None
general_indexes = None
character_indexes = None


def load_model(model_repo: str, model_filename: str) -> rt.InferenceSession:
    global cur_model, tag_names, rating_indexes, general_indexes, character_indexes
    path = huggingface_hub.hf_hub_download(
        model_repo, model_filename)
    model = rt.InferenceSession(path)

    path = huggingface_hub.hf_hub_download(
        CONV2_MODEL_REPO, LABEL_FILENAME)
    df = pd.read_csv(path)

    tag_names = df["name"].tolist()
    rating_indexes = list(np.where(df["category"] == 9)[0])
    general_indexes = list(np.where(df["category"] == 0)[0])
    character_indexes = list(np.where(df["category"] == 4)[0])
    return model


def predict(image: PIL.Image.Image, threshold: float, detect_chara: bool, character_threshold: float):
    model = cur_model[1]
    _, height, width, _ = model.get_inputs()[0].shape

    # Alpha to white
    image = image.convert("RGBA")
    new_image = PIL.Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, mask=image)
    image = new_image.convert("RGB")
    image = np.asarray(image)

    # PIL RGB to OpenCV BGR
    image = image[:, :, ::-1]

    image = dbimutils.make_square(image, height)
    image = dbimutils.smart_resize(image, height)
    image = image.astype(np.float32)
    image = np.expand_dims(image, 0)

    input_name = model.get_inputs()[0].name
    label_name = model.get_outputs()[0].name
    probs = model.run([label_name], {input_name: image})[0]

    labels = list(zip(tag_names, probs[0].astype(float)))

    # First 4 labels are actually ratings: pick one with argmax
    ratings_names = [labels[i] for i in rating_indexes]
    rating = dict(ratings_names)

    # Then we have general tags: pick anywhere prediction confidence > threshold
    general_names = [labels[i] for i in general_indexes]
    general_res = [x for x in general_names if x[1] > threshold]
    general_res = dict(general_res)

    # Everything else is characters: pick anywhere prediction confidence > threshold
    character_names = [labels[i] for i in character_indexes]
    character_res = [x for x in character_names if x[1] > character_threshold]
    character_res = dict(character_res)

    detections = general_res if not detect_chara else general_res | character_res

    detections = dict(sorted(detections.items(), key=lambda item: item[1], reverse=True))
    tag_str = ", ".join(list(detections.keys()))
    tag_str = tag_str.replace("_", " ")
    return tag_str


def tag(tagger_model, threshold, detect_chara, character_threshold, progress=gr.Progress()):
    global cur_model
    if not os.path.isdir(globals.PROJECT_DIRECTORY):
        return "Project directory doesn't exist! Set it in the config tab."
    if cur_model[0] != tagger_model:
        if tagger_model == "ConvNextV2":
            cur_model = tagger_model, load_model(CONV2_MODEL_REPO, MODEL_FILENAME)
    file_list = []
    for file in os.listdir(globals.PROJECT_DIRECTORY):
        if file.split('.')[-1] in globals.VALID_EXTENSIONS:
            file_list.append(os.path.join(globals.PROJECT_DIRECTORY, file))
    if not file_list:
        return "No images found! Make sure your project directory is set!"
    for file in progress.tqdm(file_list):
        image = PIL.Image.open(file)
        caption = predict(image, threshold, detect_chara, character_threshold)
        open(file.split('.')[0] + '.txt', 'w').write(caption)
    return "Captioned Successfully!"
