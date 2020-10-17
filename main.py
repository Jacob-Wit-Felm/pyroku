from os import environ
from pyrogram import Client

api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
info = "Greetings from **Heroku**!"

app = Client(":memory:", api_id, api_hash)

print(info)

@app.on_message()
def work(client, message):
    app.send_message(message.chat.id, info)

app.run()
