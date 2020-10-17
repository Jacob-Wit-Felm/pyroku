import os
from os import environ
from pyrogram import Client

api_id = environ.get('API_ID')
api_hash = environ.get("API_HASH")
info = "Greetings from **Heroku**!"

print(api_id)
print(api_hash)

app = Client(":memory:", api_id, api_hash)

print(info)

@app.on_message()
def work(client, message):
    app.send_message(message.chat.id, info)

app.run()
