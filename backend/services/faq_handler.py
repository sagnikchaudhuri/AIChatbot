def check_faq(user_message, business_info):
    user_message = user_message.lower()

    for item in business_info["faq"]:
        keywords = item["q"].lower().split()

        if any(word in user_message for word in keywords):
            return item["a"]

    return None