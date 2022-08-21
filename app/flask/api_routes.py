import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from .utils import allow_upload
from .auth_routes import token_auth


api_route = Blueprint("app", __name__)


@api_route.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        upload_conf = current_app.config["UPLOAD_CONFIG"]

        if file and allow_upload(file.filename, upload_conf.file_extensions):
            if not os.path.exists(upload_conf.upload_dir):
                os.mkdir(upload_conf.upload_dir)
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_conf.upload_dir, filename))
            return "file saved!"


@api_route.route("/users", methods=["GET"])
@token_auth.login_required
def get_users():
    return jsonify(result=["user1", "user2"])
