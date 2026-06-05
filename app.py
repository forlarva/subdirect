from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"


@app.route("/sub")
def sub():

    url = request.args.get("url")

    if not url:
        return "missing url", 400

    try:
        r = requests.get(
            url,
            timeout=15,
            allow_redirects=True
        )

        excluded = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection"
        ]

        headers = {
            k: v for k, v in r.headers.items()
            if k.lower() not in excluded
        }

        return Response(
            r.content,
            status=r.status_code,
            headers=headers
        )

    except Exception as e:
        return str(e), 500


@app.route("/vip/<token>")
def vip(token):

    return {
        "status": "ok",
        "token": token
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
