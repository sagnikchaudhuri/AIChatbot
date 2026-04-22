from flask import Flask
from backend.routes.whatsapp_webhook import whatsapp_bp
import os

app = Flask(__name__)
app.register_blueprint(whatsapp_bp)

@app.route("/")
def home():
    return "WhatsApp AI Bot Running"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
