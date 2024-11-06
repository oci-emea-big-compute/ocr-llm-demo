import base64
from openai import OpenAI
import gradio as gr
import magic
from pdf2image import convert_from_path
from io import BytesIO
from gradio_pdf import PDF
from PIL import Image as Pil


#client = OpenAI(
#base_url="http://localhost:8001/v1",
#api_key="EMPTY"  # vLLM doesn't require an API key by default
#)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "./test.png"

def is_pdf(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type == 'application/pdf'

def contact_llm(model_label,query,image_path):
 images=[]

 # Getting the base64 string
 if is_pdf(image_path[0]):
     images = convert_from_path(image_path[0])
     im_file = BytesIO()
     images[0].save(im_file, format="JPEG")
     im_bytes = im_file.getvalue()
     base64_image = base64.b64encode(im_bytes).decode('utf-8')
     image_path[0]=im_file
     image=images[0]
 else:
     base64_image = encode_image(image_path[0])
     image = Pil.open(image_path[0])

 if model_label=="Pixtral-12B":
      model="mistralai/Pixtral-12B-2409"
      port=str(8001)
 if model_label=="Qwen2-VL":
      model="Qwen/Qwen2-VL-7B-Instruct"
      port=str(8000)
 if model_label=="Llama-3.2-Vision":
      model="meta-llama/Llama-3.2-11B-Vision-Instruct"
      port=str(8002)


 if query != "":
    text_query=query
 else:
    text_query="Extract text from picture precisely as JSON"

 client = OpenAI(
  base_url="http://localhost:"+port+"/v1",
  api_key="EMPTY"  # vLLM doesn't require an API key by default
  )
 response = client.chat.completions.create(
  model=model,       
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": text_query,
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
 )

 #print(response.choices[0])
 return text_query,response.choices[0], image


if __name__ == "__main__":
    # Create the Gradio interface
    interface = gr.Interface(
        fn=contact_llm,
        inputs=[
            gr.Dropdown(
            ["Pixtral-12B", "Qwen2-VL", "Llama3.2-Vision"], label="Model", info="Pick the model to use"
        ),  gr.Textbox(label="Enter your query", placeholder="Ask a question about the content"),
            gr.FileExplorer(glob="**/**",root_dir="./pictures",ignore_glob="**/__init__.py",)
        ],
        outputs=[gr.Textbox(label="Query"), gr.Textbox(label="Response"), gr.Image(type="pil")],
        title="Pixtral-12b RAG Application",
        description="Provide an image URL and ask questions based on the context generated from it."
    )

    # Launch the interface
    interface.launch(share = True)

