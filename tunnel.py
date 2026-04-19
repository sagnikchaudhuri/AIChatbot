from pyngrok import ngrok

public_url = ngrok.connect(5000)
print("Public URL:", public_url)

input("Running... Press Enter to stop")