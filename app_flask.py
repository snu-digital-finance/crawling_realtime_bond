from flask import Flask, send_from_directory
from markupsafe import escape

from util import DATA_DIR

app = Flask(__name__)


@app.route("/")
def index():
    links = "".join(
        f'<li><a href="/download/{escape(p.name)}">{escape(p.name)}</a></li>'
        for p in sorted(DATA_DIR.iterdir())
    )
    return f"<h1>파일 목록</h1><ul>{links}</ul>"


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=False)
