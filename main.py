import os
from os import environ
from pyrogram import Client

from boto.s3.connection import S3Connection


api_id = environ.get('API_ID')
api_hash = environ.get("API_HASH")
info = "Greetings from **Heroku**!"

s3 = S3Connection(os.environ.get('S3_KEY'), os.environ.get('S3_SECRET'))

print(api_id)
print(api_hash)
print(s3)

app = Client(":memory:", api_id, api_hash)

print(info)

@app.on_message()
def work(client, message):
    app.send_message(message.chat.id, info)

app.run()
