# LLM_classifier
Comparing local Visual Language Models on classification tasks

For the following demo pipeline you need to provide a sample dataset (each folder is a class containing images from that class).
E.g. download the MNIST dataset using:
```
python download_mnist.py
```

Demo pipeline:
1. On Linux, Download ollama (llm server) as:
```
  !curl https://ollama.ai/install.sh | sh
  !ollama serve &
```

2. Pull a vision-language model (e.g. minicpm-v):
```
!ollama pull minicpm-v
```

3. run the python script:
```
!python main.py --model='minicpm-v' --dataset='mini_mnist/mnist_png/testing'
```

Alternatively, provide the url to an image for single image classification.
