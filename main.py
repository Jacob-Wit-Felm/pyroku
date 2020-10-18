import os
from os import environ

from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import BadRequest, FloodWait

import sqlite3

import datetime
import random

api_id = environ.get('API_ID')
api_hash = environ.get('API_HASH')
hey = "Cannot wait to send some /hentai/!"
allowed_groups = [-1001317920976, -1001339765569]

app = Client("my_account", api_id, api_hash)

@app.on_message(filters.command(["new"]))
def new_img(client, message):
	if message.chat.id in allowed_groups:
		conn = sqlite3.connect("database")
		cur = conn.cursor()
		
		try:
			text = message.text.split("/new ")[1]
			print("gender is " + text)
			gender = text.split()

			sql = """	SELECT id, title, volume from Channels
						WHERE gender = ?
			"""
			operation = cur.execute(sql, (gender))
			channels = operation.fetchall()

			if len(channels) == 0:
				client.send_message(text = "Dear, try better 😉 There is no such a gender", chat_id = message.chat.id, reply_to_message_id = message.message_id)
		except:
			print("going random")

			sql = """	SELECT id, title, volume from Channels
						WHERE gender IS NOT NULL
			"""
			operation = cur.execute(sql)
			channels = operation.fetchall()

		print(channels)
		conn.close()

		random_channel_num = random.randint(0, len(channels)-1)
		random_channel = channels[random_channel_num]
		random_img = random.randint(0, random_channel[2])

		print(random_channel)
		print(random_img)

		sourse_message = client.get_history(chat_id = random_channel[0], offset = random_img, limit = 1)[0]

		print(sourse_message)

		try:
			if sourse_message["photo"]:
				client.send_photo(message.chat.id, photo = sourse_message["photo"]["file_id"], file_ref = sourse_message["photo"]["file_ref"])
		except:
			pass
		try:
			if sourse_message["video"]:
				client.send_video(message.chat.id, video = sourse_message["video"]["file_id"], file_ref = sourse_message["video"]["file_ref"])
		except:
			pass
		try:
			if sourse_message["animation"]:
				client.send_animation(message.chat.id, animation = sourse_message["animation"]["file_id"], file_ref = sourse_message["animation"]["file_ref"])
		except:
			pass

		print(sourse_message.animation)
		# client.send_photo(message.chat.id, file_ref)


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
				client.send_message(message.chat.id, "No need update in {}".format(channel[2]))
		conn.commit()
		conn.close()

app.run()