import os
import urllib.request
import tarfile

# URL of the dataset (a subset of MNIST in PNG format)
MINI_MNIST_URL = "https://github.com/myleott/mnist_png/raw/master/mnist_png.tar.gz"
DATASET_DIR = "mini_mnist"

def download_and_extract_mini_mnist():
    """Downloads and extracts the Mini-MNIST dataset."""
    os.makedirs(DATASET_DIR, exist_ok=True)
    dataset_path = os.path.join(DATASET_DIR, "mnist_png.tar.gz")

    if not os.path.exists(dataset_path):
        print("Downloading Mini-MNIST dataset...")
        urllib.request.urlretrieve(MINI_MNIST_URL, dataset_path)
        print("Download complete.")

    print("Extracting dataset...")
    with tarfile.open(dataset_path, "r:gz") as tar:
        tar.extractall(DATASET_DIR)

    print("Dataset ready in:", os.path.join(DATASET_DIR, "mnist_png"))

if __name__ == "__main__":
    download_and_extract_mini_mnist()
