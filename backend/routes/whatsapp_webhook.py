from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from backend.services.llm_service import generate_response
from backend.services.faq_handler import check_faq
from backend.services.lead_capture import save_lead
from backend.utils.prompt_builder import is_lead_intent
from backend.utils.logger import log_info, log_error

import json
import os

whatsapp_bp = Blueprint("whatsapp", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "business_info.json")

with open(DATA_PATH) as f:
    business_info = json.load(f)


@whatsapp_bp.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    log_info(f"Msg from {sender}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # FAQ
    faq_response = check_faq(incoming_msg, business_info)
    if faq_response:
        msg.body(faq_response)
        return str(resp)

    # Lead intent
    if is_lead_intent(incoming_msg):
        msg.body("Great! Please send your name and phone number like this:\nName, Phone")
        return str(resp)

    # Lead capture
    if "," in incoming_msg:
        try:
            name, phone = incoming_msg.split(",", 1)
            save_lead(name.strip(), phone.strip())

            msg.body(f"Thanks {name.strip()}! We'll contact you shortly.")
            return str(resp)

        except Exception as e:
            log_error(str(e))
            msg.body("Please send details like:\nName, Phone")
            return str(resp)

    # AI fallback
    ai_response = generate_response(incoming_msg, business_info)
    msg.body(ai_response)

    return str(resp)
