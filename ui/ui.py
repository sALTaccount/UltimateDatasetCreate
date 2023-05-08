import gradio as gr
import ui.config_ui as config_ui
import ui.download_ui as download_ui
import ui.filter_ui as filter_ui
import ui.tag_ui as tag_ui


def load():
    with gr.Blocks() as demo:
        config_ui.load()
        download_ui.load()
        filter_ui.load()
        tag_ui.load()

    demo.queue().launch(server_port=9005)
