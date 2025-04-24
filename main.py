import os

token = os.getenv("BOT_TOKEN")
print("Loaded token:", token if token else "No token found")
