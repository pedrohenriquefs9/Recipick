import os
from flask import Blueprint, send_from_directory, current_app

main_bp = Blueprint("main", __name__)

@main_bp.route("/", defaults={"path": ""})
@main_bp.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, "index.html")