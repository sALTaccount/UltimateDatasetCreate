import gradio as gr
import os
import globals as c


def change_directory(directory):
    log = ""
    if not os.path.isabs(directory):
        directory = os.path.join(os.getcwd(), directory)
        log += f"Converting to absolute path: {directory}\n"
    if not os.path.exists(directory):
        log += "Directory does not exist, creating...\n"
        os.makedirs(directory)
        log += f"Created {directory}\n"
    else:
        log += f"Directory {directory} already exists!\n"
        log += f"Using {directory}\n"
    c.PROJECT_DIRECTORY = directory
    return log


def load():
    with gr.Tab('Config'):
        directory = gr.components.Textbox(label="Directory", lines=1, value="Projects/MyProject")
        log = gr.components.Textbox(label="Log", lines=3, interactive=False)
        set_directory_button = gr.components.Button("Set Directory")
    set_directory_button.click(change_directory, inputs=[directory], outputs=[log])
