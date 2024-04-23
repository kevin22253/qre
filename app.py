from flask import Flask, render_template, request, send_file
import qrcode
import os

app = Flask(__name__)

# Path to the upload folder
upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Create the upload folder if it doesn't exist
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    event = request.form['event']
    date = request.form['date']

    data = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nEvent: {event}\nDate: {date}"
    filename = f"{name.replace(' ', '_')}_event_qr_code.png"
    file_path = os.path.join(upload_folder, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

    # Send the file to the user for download
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
