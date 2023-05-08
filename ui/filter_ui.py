import gradio as gr
import ui.manual_filter_ui as manual_filter_ui
import ui.sort_filter_ui as age_filter_ui


def load():
    with gr.Tab('Filter'):
        manual_filter_ui.load()
        age_filter_ui.load()
