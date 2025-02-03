#!/usr/bin/env python3
import base64
import json
import os
import requests
import argparse
import shutil
from urllib.parse import urlparse
from urllib.request import urlretrieve

# Ollama inference server details
OLLAMA_URL = "http://localhost:11434/api/generate"
PROMPT = "Classify the image. Return the class name in the format: ```{ \"class\" : \"CLASS_NAME\" }```"

# Function to find image files in a directory
def find_image_files(directory):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return [os.path.join(root, file) 
            for root, _, files in os.walk(directory) 
            for file in files if os.path.splitext(file)[1].lower() in image_extensions]

# Function to query the Ollama API
def query_ollama(file_path, model):
    with open(file_path, 'rb') as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')

    data = {
        "model": model,
        "prompt": PROMPT,
        "images": [encoded_image],
        "stream": False,  # Ensure single response
        "format": "json"  # Expect JSON output
    }

    response = requests.post(OLLAMA_URL, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API Error {response.status_code}"}

# Function to classify images in a dataset
def classify_dataset(dataset_path, model):
    results = {}
    image_files = find_image_files(dataset_path)

    for file_path in image_files:
        response = query_ollama(file_path, model)
        if "response" in response:
            try:
                class_name = json.loads(response["response"])["class"]
                results[file_path] = class_name
                print(f"Image: {file_path} → Classified as: {class_name}")
            except KeyError:
                print(f"Unexpected response for {file_path}: {response}")
        else:
            print(f"Error processing {file_path}: {response}")

    return results

# Function to download an image from a URL
def download_image(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    local_path = os.path.join("/tmp", filename)

    try:
        urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None

# Function to classify a single image from a URL
def classify_url(image_url, model):
    local_image_path = download_image(image_url)
    if not local_image_path:
        return

    response = query_ollama(local_image_path, model)
    if "response" in response:
        try:
            class_name = json.loads(response["response"])["class"]
            print(f"Image URL: {image_url} → Classified as: {class_name}")
        except KeyError:
            print(f"Unexpected response: {response}")
    else:
        print(f"Error processing image: {response}")

    # Cleanup
    os.remove(local_image_path)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Image classification script")
    parser.add_argument("--dataset", type=str, help="Path to dataset (folder structure)")
    parser.add_argument("--url", type=str, help="Image URL for classification")
    parser.add_argument("--model", type=str, required=True, help="Model name to use for classification")

    args = parser.parse_args()

    if args.dataset:
        if not os.path.isdir(args.dataset):
            print("Error: Dataset path is not a valid directory.")
            return
        classify_dataset(args.dataset, args.model)

    elif args.url:
        classify_url(args.url, args.model)

    else:
        print("Please provide either a dataset path (--dataset) or an image URL (--url).")

if __name__ == "__main__":
    main()
