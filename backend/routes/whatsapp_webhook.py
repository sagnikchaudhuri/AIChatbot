from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

import json

from services.intent import detect_intent
from utils.prompt_builder import build_gym_prompt
from services.lead_capture import save_lead
from services.llm_service import generate_response
from utils.logger import log_info, log_error

whatsapp_bp = Blueprint("whatsapp", __name__)

# Load business config
with open("data/business_info.json", "r", encoding="utf-8") as f:
    business_info = json.load(f)


@whatsapp_bp.route("/whatsapp", methods=["POST"])
def whatsapp_reply():

    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "").strip()

    log_info(f"Incoming: {sender} -> {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    try:
        # ----------------------------
        # 1. INTENT DETECTION
        # ----------------------------
        intent = detect_intent(incoming_msg.lower())

        # ----------------------------
        # 2. HIGH-CONVERSION RULES (NO AI)
        # ----------------------------

        # PRICE FLOW
        if intent == "pricing":
            msg.body(
                "₹1500/month only.\n"
                "Free trial available today.\n"
                "Shall I book your trial session?"
            )
            return str(resp)

        # LEAD / TRIAL FLOW
        if intent == "lead_capture":
            msg.body(
                "Awesome!\n"
                "To book your FREE trial, send:\n"
                "Name, Phone"
            )
            return str(resp)

        # ----------------------------
        # 3. LEAD CAPTURE HANDLING
        # ----------------------------
        if "," in incoming_msg:
            try:
                name, phone = incoming_msg.split(",", 1)

                save_lead(
                    name=name.strip(),
                    phone=phone.strip(),
                    message=incoming_msg
                )

                msg.body(
                    f"Perfect {name.strip()}!\n"
                    "Your FREE trial is confirmed.\n"
                    "Our trainer will contact you soon."
                )
                return str(resp)

            except Exception as e:
                log_error(f"Lead error: {str(e)}")

                msg.body(
                    "Please send in format:\n"
                    "Name, Phone"
                )
                return str(resp)

        # ----------------------------
        # 4. AI FALLBACK (SALES MODE)
        # ----------------------------
        prompt = build_gym_prompt(
            user_message=incoming_msg,
            business_info=business_info,
            intent=intent
        )

        ai_response = generate_response(prompt, business_info)

        log_info(f"AI Response: {ai_response}")

        if not ai_response:
            msg.body("Sorry, something went wrong. Please try again.")
        else:
            msg.body(ai_response)

        return str(resp)

    except Exception as e:
        log_error(f"Webhook crash: {str(e)}")

        msg.body(
            "Temporary issue. Please try again shortly."
        )

        return str(resp)