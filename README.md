# Pystegno 🔐🖼️

Pystegno is a lightweight web application that allows you to hide secret text messages inside image files without noticeably changing the image's appearance. It implements **Image Steganography** using the **Least Significant Bit (LSB)** technique. 

---

## ✨ Features

* **Image Steganography (LSB Algorithm):** Conceal text-based messages directly inside image pixels (PNG, JPG) without degrading visual quality.
* **FastAPI Backend:** A highly performant, asynchronous Python backend handling uploads and processing instantly.
* **Clean Web UI:** A simple, user-friendly HTML/CSS interface allowing you to easily upload images to encode and decode messages.
* **Lossless Output Data:** Ensures encoded images are exported in lossless `PNG` format preventing compression algorithms from accidentally stripping away your secret messages.
* **Secure Delimiters:** Automatically inserts `###` delimiters into hidden messages, ensuring exact extraction down to the letter without reading noisy data.

## 🛠️ How it Works

### Encoding
1. You upload an image and input a secret text message. 
2. The system converts your message into binary.
3. The image's RGB pixels are read. It iteratively replaces the **least significant bit** of each color channel (Red, Green, Blue) with the bits of your message.
4. It outputs and downloads a newly synthesized PNG image that looks completely identical to the human eye but holds the hidden data.

### Decoding
1. You upload a previously encoded image.
2. The application extracts the least significant bit of every color channel across the image pixels.
3. It reconstructs the binary string back into ASCII characters.
4. Once it detects the `###` delimiter, it stops and displays your completely restored secret message.

## 🚀 Running Locally

### Prerequisites
Make sure you have Python 3.10+ installed.

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server (runs on port 8000 by default, but configured for 7860 in Docker):
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser and navigate to: `http://localhost:8000`

## 🐳 Docker Deployment

Pystegno is completely configured to run in containerized environments (such as Hugging Face Spaces).

```bash
docker build -t pystegno .
docker run -p 7860:7860 pystegno
```
Then visit `http://localhost:7860`.

## 📦 Hugging Face Spaces

This repository comes pre-packaged with a Hugging Face configuration block at the top of this README and a Space deployment `Dockerfile`. 
To deploy:
1. Create a new **Docker Space** on [Hugging Face](https://huggingface.co/spaces).
2. Upload these project files (via Git push or their Web UI).
3. The server will build and run immediately.
