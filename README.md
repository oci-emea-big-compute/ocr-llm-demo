# ocr-llm-demo
How to quickly setup a demo to demonstrate OCR capabilities of multimodal llm
New generation open multimodal llm are a very good fit for complex OCR workloads.
Many of the funcionalities that would require fine tuning with traditional OCR models can now be achieved with prompt engineering. 
The multilingual support, the hability to recognize handwriting are some of the features that can be used to improve OCR workloads.

## Prerequisites of the demo
To download model weights you will need access token to Hugging Face.
The demo was run on Ubuntu 24.04. But it should be possible to run it on other Ubuntu versions.
You need to install
- Cuda toolkit/Nvidia Driver
- anaconda or miniconda
- sudo apt-get install python-poppler


### Install and activate 
```
conda env create -f ocr-llm.yaml
conda activate ocr-llm
```

## LLM Models

In this Demo we use VLLM to serve multi modal models with the OpenAI API. We tested Pixtral-12B on a VM with 2 A10, and Qwen2-VL on a single A10. 
Llama-3.2-11B-Vision-Instruct is also an option.

You first need to login to Hugging Face to download the weights
```
huggingface-cli login
```
and you serve one of the VLLM supported visual models. According to the number of GPUs in your shape you might be able to execute one model or more concurrenlty. For llama-3.2 access in Europe is currenlty restricted.

```
vllm serve  mistralai/Pixtral-12B-2409 --dtype auto  --tokenizer-mode  mistral -tp 2 --port 8001 --max-model-len 32768

vllm serve  Qwen/Qwen2-VL-7B-Instruct  --dtype auto --max-model-len 8192 --enforce-eager --port 8000

vllm serve  meta-llama/Llama-3.2-11B-Vision-Instruct --dtype auto   --port 8002 --max-model-len 32768
```  
## Sample images

The folder pictures includes some example pictures that can be used in the demo. You can add additional images to improve the demo.
The LLM supported formats are PNG,JPG,WEBP, non animated GIF. I also added automated conversion for PDF images, but for multipage PDF only the firt page will be considered.


## Running the GUI

You have a Gradio based GUI available:
```
python gui5.py
```

Gradio is configured to proxy to a public connection, similar to the following one
 ![Alt text](gui.png?raw=true "GUI")

## Executing Qwen-2.5-VL as backend API

Qwen-2.5-VL are new models, and are not yet available in VLLM, so we use fastapi implementation from https://github.com/phildougherty/qwen2.5-VL-inference-openai to run it.
You first need to download the models with the downloads.sh script and later you can start it with python app.py (8B variant) and app72.py (72B). We provide a conda env, but you might need to install transofrmers manually from the repo.  
```
* Running on local URL:  http://127.0.0.1:7860
* Running on public URL: https://44250956c28a3b22ac.gradio.live

This share link expires in 72 hours. For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)
```


