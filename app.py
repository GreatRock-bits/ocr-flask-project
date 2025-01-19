import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Initialize Flask App
app = Flask(__name__)

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'dfki.haal02@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'vuwa atob skel zbbx'  # Replace with your email password

# Set up folder for uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle file upload
        if 'image' not in request.files:
            return "No file part in the request", 400
        file = request.files['image']
        if file.filename == '':
            return "No file selected", 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform OCR
        text = extract_text(filepath)

        # Parse the invoice text into structured data
        table_data = parse_invoice_to_table(text)
        return render_template('table.html', table_data=table_data, text=text, filename=filename)

    return render_template('index.html')




def extract_text(image_path):
    """Extract text from an image."""
    image = Image.open(image_path)
    return pytesseract.image_to_text(image)



def parse_invoice_to_table(text):
    """
    Extract structured data from invoice text.
    """
    lines = text.split('\n')
    table_data = []
    pattern = re.compile(r"(.+?)\s+(\d+)\s+\$?([\d.,]+)\s+\$?([\d.,]+)")

    for line in lines:
        match = pattern.match(line)
        if match:
            item_name = match.group(1).strip()
            quantity = match.group(2).strip()
            unit_price = match.group(3).strip()
            total_price = match.group(4).strip()
            table_data.append([item_name, quantity, unit_price, total_price])

    # If no data found, return an empty list with a placeholder message
    if not table_data:
        table_data.append(["No valid data found", "", "", ""])
    return table_data

@app.route('/raw-text/<filename>', methods=['GET'])
def raw_text(filename):
    """Display the raw text extracted from the image."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        return f"File {filename} not found", 404

    # Perform OCR
    raw_text_content = extract_text(filepath)

    return render_template('raw_text.html', raw_text=raw_text_content, filename=filename)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part in the request", 400
        file = request.files['image']
        if file.filename == '':
            return "No file selected", 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform OCR
        text = extract_text(filepath)

        # Parse the invoice text into structured data
        table_data = parse_invoice_to_table(text)
        return render_template('table.html', table_data=table_data, filename=filename)

    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    """Send the raw OCR data via email."""
    recipient_email = request.form.get('email')
    raw_text = request.form.get('raw_text')

    if not recipient_email or not raw_text:
        return "Email or text data is missing", 400

    try:
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = recipient_email
        msg['Subject'] = "Raw OCR Data"

        # Email body
        body = f"<h1>Raw OCR Data</h1><pre>{raw_text}</pre>"
        msg.attach(MIMEText(body, 'html'))

        # Connect to SMTP server and send the email
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return "Email sent successfully!", 200
    except Exception as e:
        return f"Failed to send email: {str(e)}", 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
