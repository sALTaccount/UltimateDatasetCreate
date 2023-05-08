import gradio as gr
import filtering.manual_filter as manual_filter


def load():
    with gr.Tab("Manual Filtering"):
        with gr.Row():
            display_image = gr.components.Image(interactive=False, shape=(384, 384))
            with gr.Column():
                tags_box = gr.components.Textbox(lines=10, label="Tags")
                message = gr.Markdown("")
        with gr.Row():
            refresh_button = gr.components.Button("Refresh")
            delete_image_button = gr.components.Button("Delete Image")
            prev_image_button = gr.components.Button("Previous Image")
            next_image_button = gr.components.Button("Next Image")
            save_tag_button = gr.components.Button("Save Tags")

    refresh_button.click(manual_filter.refresh, outputs=[display_image, message, tags_box])
    prev_image_button.click(manual_filter.decrement, outputs=[display_image, message, tags_box])
    delete_image_button.click(manual_filter.delete, outputs=[display_image, message, tags_box])
    next_image_button.click(manual_filter.increment, outputs=[display_image, message, tags_box])
    save_tag_button.click(manual_filter.modify_tags, inputs=[tags_box], outputs=[message])
