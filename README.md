OCR application to read documents including invoices

# 📝 OCR Flask API (English & Indonesian)

A lightweight and efficient Optical Character Recognition (OCR) API built using **Flask**. This API extracts text from uploaded images and supports both **English** and **Indonesian** languages using Tesseract OCR.

---

## 🚀 Features

- 🔤 **Multi-language OCR**: Supports text extraction in **English** and **Bahasa Indonesia**
- 🖼️ Accepts standard image formats (`.png`, `.jpg`, `.jpeg`)
- 🖼️ Email functionality to send the extracted text 
- ⚡ Lightweight Flask-based REST API
- 📦 Easy deployment with minimal setup
- 🐳 Dockerized for easy deployment
- 🔁 Optional language selection via query parameter

---
## 📺 Live Demo

👉 Try it now: [https://grb-ocr-app.onrender.com/](https://grb-ocr-app.onrender.com/)

## 📦 Requirements

- Python 3.8+
- Flask
- pytesseract
- Pillow
- Tesseract OCR engine (installed on your system)

---

## 📄 License

Licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.  

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ocr-flask-api.git
   cd ocr-flask-api

   # Set up virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt

---

## 🐳 Alternatively Run with Docker

You can run this OCR Flask app directly using Docker. No setup needed!

### ✅ Prerequisites
- Docker installed on your system ([Get Docker](https://www.docker.com/products/docker-desktop))

### 📥 Pull the Image from Docker Hub

```bash
docker pull tifat58/flask_project_v3
```

## 📬 Contact
- contact@greatrockbits.com

