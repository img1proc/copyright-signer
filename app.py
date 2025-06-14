from flask import Flask, request, render_template
import hashlib
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        author_name = request.form["author_name"]
        pdf = request.files["pdf"]
        private_key = request.files["private_key"]

        # ファイルを一時保存
        pdf_path = f"/tmp/{pdf.filename}"
        key_path = f"/tmp/{private_key.filename}"
        pdf.save(pdf_path)
        private_key.save(key_path)

        # PDFのハッシュを生成
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            hash_value = hashlib.sha256(pdf_bytes).hexdigest()

        # 鍵で署名
        import subprocess
        sig_path = "/tmp/signature.bin"
        subprocess.run([
            "openssl", "dgst", "-sha256", "-sign", key_path,
            "-out", sig_path, pdf_path
        ], check=True)

        # Base64でエンコード
        with open(sig_path, "rb") as f:
            signature_b64 = base64.b64encode(f.read()).decode()

        return render_template("index.html", hash_value=hash_value, signature_b64=signature_b64)

    return render_template("index.html")