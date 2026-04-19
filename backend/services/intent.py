def detect_intent(message):
    msg = message.lower()

    if any(x in msg for x in ["price", "fee", "cost", "membership"]):
        return "pricing"

    if any(x in msg for x in ["trial", "join", "book", "visit"]):
        return "lead_capture"

    if any(x in msg for x in ["timing", "open", "close"]):
        return "timing"

    return "general"