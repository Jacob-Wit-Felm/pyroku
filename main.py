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
admin = 537288423

app = Client("my_account", api_id, api_hash)

@app.on_message(filters.command(["new"]))
def new_img(client, message):
	if message.chat.id in allowed_groups:
		conn = sqlite3.connect("database")
		cur = conn.cursor()
		
		try:
			text = message.text.split("/new ")[1]
			gender = text.split()

			sql = """	SELECT id, title, volume from Channels
						WHERE gender = ?
			"""
			operation = cur.execute(sql, (gender))
			channels = operation.fetchall()

			if len(channels) == 0:
				client.send_message(text = "Dear, try better 😉 There is no such a gender", chat_id = message.chat.id, reply_to_message_id = message.message_id)
		except:

			sql = """	SELECT id, title, volume from Channels
						WHERE gender IS NOT NULL
			"""
			operation = cur.execute(sql)
			channels = operation.fetchall()

		conn.close()

		random_channel_num = random.randint(0, len(channels)-1)
		random_channel = channels[random_channel_num]
		while 1:
			mistake = 0
			random_img = random.randint(0, random_channel[2])

			sourse_message = client.get_history(chat_id = random_channel[0], offset = random_img, limit = 1)[0]

			try:
				client.send_photo(message.chat.id, photo = sourse_message["photo"]["file_id"], file_ref = sourse_message["photo"]["file_ref"])
			except:
				mistake += 1
			try:
				client.send_video(message.chat.id, video = sourse_message["video"]["file_id"], file_ref = sourse_message["video"]["file_ref"])
			except:
				mistake += 1
			try:
				client.send_animation(message.chat.id, animation = sourse_message["animation"]["file_id"], file_ref = sourse_message["animation"]["file_ref"])
			except:
				mistake += 1

			print(mistake)
			if mistake != 3:
				break
			print("misake")

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

@app.on_message(filters.command(["update"]) & filters.user(admin))
def update(client, message):
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

				sql = """	UPDATE Channels
							SET 
								volume = ?,
								last_update = ?
							WHERE 
								id = ?
				"""
				cur.execute(sql, (channel_volume, datetime.datetime.now(), channel[0]))

		client.send_message(message.chat.id, "No need in updating~ Thank you for worrying 🤤" )
		conn.commit()
		conn.close()

@app.on_message(filters.command(["moderate"]) & filters.user(admin))
def moderate(client, message):
	if message.chat.id in allowed_groups:
		conn = sqlite3.connect("database")
		cur = conn.cursor()

		sql = """	SELECT id, title, volume FROM Channels
					WHERE gender IS NULL
		"""
		operation = cur.execute(sql)


		try: 
			channel = operation.fetchall()[0]
		except:
			message.reply_text("Hey, everything fine here, don't touch my files without a permission ☺️")
			return

		client.send_message(message.chat.id, "What do you think about this channe?)")
		client.send_message(message.chat.id, "{}".format(channel[0]))
		for a in range(0, 3):
			random_img = random.randint(0, channel[2])
			sourse_message = client.get_history(chat_id = channel[0], offset = random_img, limit = 1)[0]
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

		conn.close()

@app.on_message(filters.command(["set"]) & filters.user(admin))
def set_gender(client, message):
	if message.chat.id in allowed_groups:
		try:
			text = message.text.split("/set ")[1]
			info = text.split()
			channel_id = info[0]
			channel_gender = info[1]

			conn = sqlite3.connect("database")
			cur = conn.cursor()

			sql = """	UPDATE Channels
						SET
							gender = ?
						WHERE
							id = ?
			"""
			operation = cur.execute(sql, (channel_gender, channel_id))	

			conn.commit()
			conn.close()

			if channel_gender == "straight":
				message.reply_text("Ha-ha, you are a pervert...")
			elif channel_gender == "yaoi":
				message.reply_text("I kind of like these images 😆, but where are girls?))))")
			else:
				message.reply_text("Hmmm, so this is not an art????😕 What should I do with these boring images?(")

		except:
			message.reply_text("Even you make mistakes👌 Just take your time~")

app.run()