import gradio as gr
import tagger.wd_tagger as wd_tagger
from tagger import modify_tags


def load():
    with gr.Tab('Caption'):
        with gr.Tab('WD Tagger'):
            gr.components.Markdown("### WD Tagger")
            tagger_model = gr.components.Dropdown(choices=["ConvNextV2"], label="Model", value="ConvNextV2")
            threshold = gr.components.Slider(minimum=0, maximum=1, step=0.01, label="General Threshold", value=0.35, interactive=True)
            detect_chara = gr.components.Checkbox(label="Detect Characters", value=False)
            character_threshold = gr.components.Slider(minimum=0, maximum=1, step=0.01, label="Character Threshold", value=0.85, interactive=True)
            tag_button = gr.components.Button("Tag")
            tagger_output = gr.components.Textbox(lines=1, label="Log", interactive=False)

            tag_button.click(wd_tagger.tag, inputs=[tagger_model, threshold, detect_chara, character_threshold], outputs=[tagger_output])

        with gr.Tab('Modify Caption'):
            gr.components.Markdown("### Modify Tags")
            with gr.Tab('Add to Caption'):
                add_tags = gr.components.Textbox(lines=1, label="Text to be added")
                add_tags_button = gr.components.Button("Add")
                add_tags_output = gr.components.Textbox(lines=1, label="Log", interactive=False)
                add_tags_button.click(modify_tags.add, inputs=[add_tags], outputs=[add_tags_output])

            with gr.Tab('Remove from Caption'):
                remove_tags = gr.components.Textbox(lines=1, label="Text to be removed")
                remove_tags_button = gr.components.Button("Remove")
                remove_tags_output = gr.components.Textbox(lines=1, label="Log", interactive=False)
                remove_tags_button.click(modify_tags.remove, inputs=[remove_tags], outputs=[remove_tags_output])
