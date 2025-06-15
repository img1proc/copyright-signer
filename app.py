# app.py
from flask import Flask, render_template, request, send_file, redirect, url_for
from io import BytesIO
from utils.pdf_generator import generate_pdf
from utils.crypto import generate_keys_and_signature
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "generated"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    title = request.args.get("title", "[No Title Provided]")

    if request.method == "POST":
        author_name = request.form.get("author_name")
        affiliation = request.form.get("affiliation")
        address = request.form.get("address")
        date = request.form.get("date")

        # 1. Generate PDF
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], "copyright_transfer.pdf")
        generate_pdf(title, author_name, affiliation, address, date, pdf_path)

        # 2. Generate keys, certificate, signature
        priv_path, cert_path, sig_path, hash_value = generate_keys_and_signature(pdf_path, app.config['UPLOAD_FOLDER'])

        return render_template("index.html",
                               title=title,
                               author_name=author_name,
                               pdf_path=os.path.basename(pdf_path),
                               cert_path=os.path.basename(cert_path),
                               sig_path=os.path.basename(sig_path),
                               priv_path=os.path.basename(priv_path),
                               hash_value=hash_value)

    return render_template("index.html", title=title)

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
