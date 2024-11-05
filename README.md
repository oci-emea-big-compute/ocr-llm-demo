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

## LLM Models

In this Demo we use VLLM to serve multi modal models with the OpenAI API. We tested Pixtral-12B on a VM with 2 A10, and Qwen2-VL on a single A10. 
Llama-3.2-11B-Vision-Instruct is also an option.

vllm serve  mistralai/Pixtral-12B-2409 --dtype auto  --tokenizer-mode  mistral -tp 2 --port 8001 --max-model-len 32768
 vllm serve  Qwen/Qwen2-VL-7B-Instruct  --dtype auto --max-model-len 8192 --enforce-eager --port 8000


  
