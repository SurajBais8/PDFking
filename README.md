PDFking

PDFking — A feature-rich PDF tools web application (Merge, Split, Compress, OCR, Convert, etc.) built with Flask (Python) and HTML/CSS/JS.

🔹 Overview

PDFking is a web-based toolkit that allows users to upload PDF files and perform tasks such as merge, split, compress, convert (PDF ↔ Word/Images), and OCR. The frontend is made with HTML/CSS/JS, and the backend is powered by Flask (Python). Each tool is implemented as a separate route for modularity.

🔹 Features

Merge multiple PDFs

Split PDF by pages or ranges

Compress PDF (reduce file size)

Convert PDF ↔ Image (PNG/JPEG) and Image → PDF

Convert PDF ↔ Word (where possible)

OCR support to extract text from scanned PDFs

Drag & Drop file upload UI

Responsive design

🔹 Tech Stack

Backend: Python, Flask

Frontend: HTML5, CSS3, JavaScript

PDF Libraries: PyPDF2, pikepdf, pdf2image, Pillow, pdfminer, pytesseract (OCR)

Database (optional): SQLite (for logs or user submissions)

Deployment: Heroku / Render / Railway / Docker

🔹 Project Structure
PDFking/
├─ app.py
├─ requirements.txt
├─ Procfile            # (for Heroku deployment)
├─ runtime.txt         # (optional for Heroku)
├─ README.md
├─ /templates
│   ├─ index.html
│   └─ tools/*.html
├─ /static
│   ├─ css/style.css
│   ├─ js/script.js
│   └─ assets/
├─ /pdf_tools
│   ├─ merge.py
│   ├─ split.py
│   ├─ compress.py
│   └─ ocr.py
├─ /uploads
└─ .gitignore

🔹 Local Setup

Clone the repository:

git clone https://github.com/<your-username>/PDFking.git
cd PDFking


Create and activate a virtual environment:

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


(Optional) Generate requirements.txt:

pip freeze > requirements.txt


Run the Flask app:

# macOS/Linux
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

# Windows (PowerShell)
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run


Then open http://127.0.0.1:5000 in your browser.

🔹 Common Issues

OCR Error → Install Tesseract:

Windows: via installer / Chocolatey

Linux: sudo apt-get install tesseract-ocr

PDF to Image Issues → Install Poppler:

macOS: brew install poppler

Linux: sudo apt install poppler-utils

🔹 Contact

Author: Suraj Bais

📧 Email: surajkumarbais392@gmail.com

🐙 GitHub: SurajBais8
