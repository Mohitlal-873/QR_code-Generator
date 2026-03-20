from flask import Flask, render_template, request, send_file
import qrcode
import os

app = Flask(__name__)

# Folder to store generated QR codes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QR_FOLDER = os.path.join(BASE_DIR, "qr_codes")

# Create folder if it does not exist
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():
    qr_image_path = None

    if request.method == "POST":
        user_input = request.form.get("data")

        if user_input:
            # Create QR image
            qr_img = qrcode.make(user_input)

            file_name = "generated_qr.png"
            full_path = os.path.join(QR_FOLDER, file_name)

            qr_img.save(full_path)

            # Path used in HTML
            qr_image_path = os.path.join("qr_codes", file_name)

    return render_template(
        "index.html",
        qr_image_path=qr_image_path
    )


@app.route("/download")
def download_qr():
    file_path = os.path.join(QR_FOLDER, "generated_qr.png")
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)