from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.analyze import analyze_bp

def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

    CORS(
        app,
        resources={
            r"/analyze": {
                "origins": "*"
            }
        }
    )
    app.register_blueprint(analyze_bp)

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "service": "NoticeGuard API"
        })

    @app.errorhandler(413)
    def file_too_large(error):
        return jsonify({
            "error": "File is too large. Maximum size is 10 MB."
        }), 413

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Endpoint not found."
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error."
        }), 500

    return app

app = create_app()
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
