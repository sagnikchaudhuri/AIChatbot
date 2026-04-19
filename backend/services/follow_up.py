from concurrent.futures.thread import _worker
import time
import threading

def send_follow_up(phone):
    print(f"Sending follow-up to {phone}")


def start_follow_up_worker():
    def worker():
        while True:
            print("Checking inactive leads...")
            # later: fetch DB + send WhatsApp message
            time.sleep(3600)  # every 1 hour

def send_follow_up(phone):
    print(f"Follow-up sent to {phone}: Still want your free gym trial?")

    
    thread = threading.Thread(target=_worker)
    thread.daemon = True
    thread.start()
