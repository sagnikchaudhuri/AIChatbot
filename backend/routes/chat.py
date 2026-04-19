from flask import Blueprint, request, jsonify
from services.llm_service import generate_response
from services.faq_handler import check_faq
from services.lead_capture import save_lead
from services.intent import detect_intent
from utils.logger import log_info, log_error
import json

chat_bp = Blueprint("chat", __name__)

# Load business data
with open("data/business_info.json") as f:
    business_info = json.load(f)



@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    # 1. FAQ
    faq_response = check_faq(user_message, business_info)
    if faq_response:
        return jsonify({"response": faq_response})

    # 2. Lead capture (simple format: Name, Phone)
    if "," in user_message:
        try:
            name, phone = user_message.split(",", 1)
            save_lead(name.strip(), phone.strip())

            return jsonify({
                "response": f"Thanks {name.strip()}! We'll contact you shortly."
            })
        except:
            return jsonify({
                "response": "Please send details in this format:\nName, Phone"
            })

    # 3. AI fallback
    ai_response = generate_response(user_message, business_info)
    return jsonify({"response": ai_response})
    log_info(f"User message: {user_message}")