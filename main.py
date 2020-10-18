import os
from os import environ

from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import BadRequest, FloodWait

import sqlite3

import datetime

api_id = environ.get('API_ID')
api_hash = environ.get('API_HASH')
hey = "Cannot wait to send some /hentai/!"
allowed_groups = [-1001317920976, -1001339765569]

app = Client("my_account", api_id, api_hash)

@app.on_message(filters.command(["hey"]))
def innitiation(client, message):
	if message.chat.id in allowed_groups:
		app.send_message(message.chat.id, hey)

@app.on_message(filters.command(["straight"]))
def straight(client, message):
	if message.chat.id in allowed_groups:
		client.send_message(message.chat.id, hey)
		client.send_photo(chat_id=message.chat.id, photo = "https://images.unsplash.com/photo-1581456495146-65a71b2c8e52?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=333&q=80")


@app.on_message(filters.command(["add"]))
def add_channel(client, message):
	if message.chat.id in allowed_groups:
		conn = sqlite3.connect("database")

		text = message.text.split()
		channel = text[-1]

		try: 
			channel_info = client.join_chat(channel)
			client.send_message(message.chat.id,"@JaWitf, go ahead and moderate. 😘)) ")
			
			time_now = datetime.datetime.now()
			time_delta = datetime.timedelta(days = 50)

			print(channel_info.id)
			print(channel_info.title)
			print(time_now)

			sql = """	INSERT INTO channels(id, title, last_update)
							VALUES(?,?,?)
			"""
			cur = conn.cursor()
			cur.execute(sql, (channel_info.id, channel_info.title, time_now-time_delta))
			conn.commit()
			conn.close()
		except BadRequest as e:
			if e:
				channel_info = client.get_chat(channel)
				client.send_message(message.chat.id,"@JaWitf, go ahead and moderate 😘)) ")

				time_now = datetime.datetime.now()
				time_delta = datetime.timedelta(days = 50)

				print(channel_info.id)
				print(channel_info.title)
				print(time_now)

				try:
					sql = """	INSERT INTO channels(id, title, last_update)
									VALUES(?,?,?)
					"""
					cur = conn.cursor()
					cur.execute(sql, (channel_info.id, channel_info.title, time_now-time_delta))
					conn.commit()
					conn.close()
				except:
					client.send_message(message.chat.id,"already added 😏")

@app.on_message(filters.command(["update"]))
def updare(client, message):
	if message.chat.id in allowed_groups:
		conn = sqlite3.connect("database")
		cur = conn.cursor()

		sql = """	SELECT id, last_update, title from Channels
		"""
		operation = cur.execute(sql)
		channels = operation.fetchall()

		for channel in channels:
			if datetime.datetime.fromisoformat(channel[1]) < datetime.datetime.now() - datetime.timedelta(hours = 1):

				channel_volume = client.get_history_count(channel[0])
				print("There is " + str(channel_volume) + " messages in " + channel[2])

				sql = """	UPDATE Channels
							SET 
								volume = ?,
								last_update = ?
							WHERE 
								id = ?
				"""
				cur.execute(sql, (channel_volume, datetime.datetime.now(), channel[0]))

			else:
				client.send_message(message.chat.id, "No need in update")
		conn.commit()
		conn.close()

app.run()