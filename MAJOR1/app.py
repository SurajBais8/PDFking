from flask import Flask, request, send_file, jsonify
from PyPDF2 import PdfReader, PdfWriter
import io
import os
import tempfile
import subprocess
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert
import pythoncom
try:
    from pdf2image import convert_from_bytes
except ImportError:
    convert_from_bytes = None
from PIL import Image

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('files')
    if not files or len(files) < 2:
        return jsonify({'error': 'Please upload at least two PDF files to merge.'}), 400

    pdf_writer = PdfWriter()

    try:
        for file in files:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)

        return send_file(output_stream, as_attachment=True, download_name='merged.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/split', methods=['POST'])
def split_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Please upload a PDF file to split.'}), 400

    page_number = request.form.get('page_number')
    if not page_number or not page_number.isdigit():
        return jsonify({'error': 'Please provide a valid page number to split at.'}), 400

    page_number = int(page_number)

    try:
        pdf_reader = PdfReader(file)
        total_pages = len(pdf_reader.pages)
        if page_number < 1 or page_number >= total_pages:
            return jsonify({'error': 'Page number out of range.'}), 400

        pdf_writer1 = PdfWriter()
        pdf_writer2 = PdfWriter()

        for i in range(page_number):
            pdf_writer1.add_page(pdf_reader.pages[i])
        for i in range(page_number, total_pages):
            pdf_writer2.add_page(pdf_reader.pages[i])

        output_stream1 = io.BytesIO()
        pdf_writer1.write(output_stream1)
        output_stream1.seek(0)

        output_stream2 = io.BytesIO()
        pdf_writer2.write(output_stream2)
        output_stream2.seek(0)

        # Return a zip file containing both split PDFs
        from zipfile import ZipFile
        zip_stream = io.BytesIO()
        with ZipFile(zip_stream, 'w') as zip_file:
            zip_file.writestr('part1.pdf', output_stream1.read())
            zip_file.writestr('part2.pdf', output_stream2.read())
        zip_stream.seek(0)

        return send_file(zip_stream, as_attachment=True, download_name='split.zip', mimetype='application/zip')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Please upload a PDF file to compress.'}), 400

    try:
        # Basic compression by rewriting the PDF (PyPDF2 does not support advanced compression)
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)

        return send_file(output_stream, as_attachment=True, download_name='compressed.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pdf-to-word', methods=['POST'])
def pdf_to_word():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Please upload a PDF file to convert to Word.'}), 400
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            tmp_pdf.write(file.read())
            tmp_pdf_path = tmp_pdf.name
        tmp_docx_path = tmp_pdf_path.replace('.pdf', '.docx')
        cv = Converter(tmp_pdf_path)
        cv.convert(tmp_docx_path, start=0, end=None)
        cv.close()
        return send_file(tmp_docx_path, as_attachment=True, download_name='converted.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            os.remove(tmp_pdf_path)
            os.remove(tmp_docx_path)
        except:
            pass

@app.route('/word-to-pdf', methods=['POST'])
def word_to_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Please upload a Word file to convert to PDF.'}), 400
    try:
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_docx:
            tmp_docx.write(file.read())
            tmp_docx_path = tmp_docx.name
        tmp_pdf_path = tmp_docx_path.replace('.docx', '.pdf')
        # Initialize COM before conversion
        pythoncom.CoInitialize()
        docx2pdf_convert(tmp_docx_path, tmp_pdf_path)
        pythoncom.CoUninitialize()
        return send_file(tmp_pdf_path, as_attachment=True, download_name='converted.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            os.remove(tmp_docx_path)
            os.remove(tmp_pdf_path)
        except:
            pass

@app.route('/pdf-to-jpg', methods=['POST'])
def pdf_to_jpg():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Please upload a PDF file to convert to JPG.'}), 400
    try:
        if convert_from_bytes is None:
            return jsonify({'error': 'pdf2image library is not installed.'}), 500
        images = convert_from_bytes(file.read())
        zip_stream = io.BytesIO()
        from zipfile import ZipFile
        with ZipFile(zip_stream, 'w') as zip_file:
            for i, image in enumerate(images):
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                zip_file.writestr(f'page_{i+1}.jpg', img_byte_arr.getvalue())
        zip_stream.seek(0)
        return send_file(zip_stream, as_attachment=True, download_name='converted_images.zip', mimetype='application/zip')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/jpg-to-pdf', methods=['POST'])
def jpg_to_pdf():
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'Please upload JPG/PNG images to convert to PDF.'}), 400
    try:
        images = []
        for file in files:
            img = Image.open(file.stream).convert('RGB')
            images.append(img)
        output_stream = io.BytesIO()
        if images:
            images[0].save(output_stream, format='PDF', save_all=True, append_images=images[1:])
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='converted.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PyPDF2.generic import NameObject, create_string_object
from PyPDF2.errors import PdfReadError

@app.route('/sign-pdf', methods=['POST'])
def sign_pdf():
    # Placeholder: Implement digital signature addition
    return jsonify({'error': 'Sign PDF feature not implemented yet.'}), 501

@app.route('/watermark', methods=['POST'])
def watermark_pdf():
    file = request.files.get('file')
    watermark_file = request.files.get('watermark')
    if not file or not watermark_file:
        return jsonify({'error': 'Please upload both PDF and watermark PDF files.'}), 400
    try:
        pdf_reader = PdfReader(file)
        watermark_reader = PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]

        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)

        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)

        return send_file(output_stream, as_attachment=True, download_name='watermarked.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rotate', methods=['POST'])
def rotate_pdf():
    file = request.files.get('file')
    direction = request.form.get('direction', 'clockwise')
    if not file:
        return jsonify({'error': 'Please upload a PDF file to rotate.'}), 400
    if direction not in ['clockwise', 'counterclockwise']:
        return jsonify({'error': 'Invalid rotation direction.'}), 400
    try:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        angle = 90 if direction == 'clockwise' else -90
        for page in pdf_reader.pages:
            page.rotate(angle)
            pdf_writer.add_page(page)
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='rotated.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/unlock', methods=['POST'])
def unlock_pdf():
    file = request.files.get('file')
    password = request.form.get('password', '')
    if not file:
        return jsonify({'error': 'Please upload a PDF file to unlock.'}), 400
    try:
        pdf_reader = PdfReader(file)
        if pdf_reader.is_encrypted:
            if not pdf_reader.decrypt(password):
                return jsonify({'error': 'Incorrect password.'}), 400
        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='unlocked.pdf', mimetype='application/pdf')
    except PdfReadError as e:
        return jsonify({'error': 'Failed to read PDF: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/protect', methods=['POST'])
def protect_pdf():
    file = request.files.get('file')
    password = request.form.get('password', '')
    if not file or not password:
        return jsonify({'error': 'Please upload a PDF file and provide a password to protect.'}), 400
    try:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        pdf_writer.encrypt(password)
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='protected.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/organize', methods=['POST'])
def organize_pdf():
    file = request.files.get('file')
    order = request.form.get('order')  # Expected comma-separated page indices (0-based)
    if not file or not order:
        return jsonify({'error': 'Please upload a PDF file and provide page order.'}), 400
    try:
        page_order = [int(i) for i in order.split(',')]
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        total_pages = len(pdf_reader.pages)
        for i in page_order:
            if i < 0 or i >= total_pages:
                return jsonify({'error': f'Page index {i} out of range.'}), 400
            pdf_writer.add_page(pdf_reader.pages[i])
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='organized.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-page-numbers', methods=['POST'])
def add_page_numbers():
    # Placeholder: Implement adding page numbers to PDF pages
    return jsonify({'error': 'Add page numbers feature not implemented yet.'}), 501

@app.route('/crop', methods=['POST'])
def crop_pdf():
    file = request.files.get('file')
    left = request.form.get('left', type=float)
    bottom = request.form.get('bottom', type=float)
    right = request.form.get('right', type=float)
    top = request.form.get('top', type=float)
    if not file or None in (left, bottom, right, top):
        return jsonify({'error': 'Please upload a PDF file and provide crop box coordinates (left, bottom, right, top).'}), 400
    try:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            page.mediabox.lower_left = (left, bottom)
            page.mediabox.upper_right = (right, top)
            pdf_writer.add_page(page)
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)
        return send_file(output_stream, as_attachment=True, download_name='cropped.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
