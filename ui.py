import gradio as gr
import os


from invoice_rotation import process_image


def image_mod(image_path):
    return process_image(image_path)


demo = gr.Interface(
    fn=image_mod,
    inputs=gr.inputs.Image(label="Upload Image File", type='filepath'),
    outputs=gr.outputs.Image(label="Download Image", type='pil'),
    live=False
)

if __name__ == "__main__":
    demo.launch()
