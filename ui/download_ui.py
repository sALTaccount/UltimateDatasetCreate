import gradio as gr
import ui.dynamic_tools as dt
import seasalt.seasalt as seasalt


def load():
    seasalt_modules = dt.get_seasalt_modules()
    with gr.Tab('Download'):
        gr.components.Markdown("### SeaSalt Downloader")
        module_box = gr.components.Dropdown(choices=seasalt_modules["scrapers"], label="Module")
        url = gr.components.Textbox(lines=1, label="URL")
        parallel_dl = gr.components.Checkbox(label="Parallel Download", value=True)
        limit = gr.components.Number(value=-1, label="Limit", interactive=True)
        with gr.Row():
            start_button = gr.components.Button("Start Download")
        output = gr.components.Textbox(lines=1, label="Log", interactive=False)
    start_button.click(seasalt.download, inputs=[module_box, url, parallel_dl, limit], outputs=[output])
