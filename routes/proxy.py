from flask import request, send_file, Blueprint, Flask, jsonify
import requests
from io import BytesIO
from threading import Thread

proxy_blueprint = Blueprint("proxy", __name__)


def fetch_image(image_url, result):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_bytes = BytesIO(response.content)
        content_type = response.headers.get("Content-Type", "image/jpeg")
        result["data"] = (image_bytes, content_type)
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)


@proxy_blueprint.route("/proxy")
def proxy():
    image_url = request.args.get("url")
    if not image_url:
        return "URL parameter is required", 400

    result = {}
    thread = Thread(target=fetch_image, args=(image_url, result))
    thread.start()
    thread.join()

    if "error" in result:
        return result["error"], 500

    image_bytes, content_type = result["data"]
    return send_file(image_bytes, mimetype=content_type)
