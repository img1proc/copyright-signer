from flask import Flask, request, render_template
import hashlib
import base64
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            author_name = request.form["author_name"]
            pdf = request.files["pdf"]
            private_key = request.files["private_key"]

            # ファイル保存
            pdf_path = f"/tmp/{pdf.filename}"
            key_path = f"/tmp/{private_key.filename}"
            sig_path = "/tmp/signature.bin"
            pdf.save(pdf_path)
            private_key.save(key_path)

            # ハッシュ計算
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
                hash_value = hashlib.sha256(pdf_bytes).hexdigest()

            # OpenSSLで署名
            result = subprocess.run([
                "openssl", "dgst", "-sha256", "-sign", key_path,
                "-out", sig_path, pdf_path
            ], capture_output=True, text=True)

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "署名に失敗しました（OpenSSLエラー）"
                return render_template("index.html", error=error_msg)

            with open(sig_path, "rb") as f:
                signature_b64 = base64.b64encode(f.read()).decode()

            return render_template("index.html", hash_value=hash_value, signature_b64=signature_b64)

        except Exception as e:
            return render_template("index.html", error=f"エラー: {str(e)}")

    return render_template("index.html")