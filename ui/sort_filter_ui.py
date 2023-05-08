import gradio as gr
import filtering.sort_filter as sort_filter


def load():
    with gr.Tab("Sort Filter"):
        sort_type = gr.Dropdown(choices=["Name"], label="Sort Type")
        gr.Markdown("Enter a fractional value to trim a %, or an integer to trim that many images.")
        trim = gr.Number(value=0, label="Trim")
        trim_button = gr.Button("Remove Images")
        output = gr.Textbox(lines=1, label="Log", interactive=False)
    trim_button.click(sort_filter.remove, inputs=[sort_type, trim], outputs=[output])
