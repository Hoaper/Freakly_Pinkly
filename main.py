import vk_api
import config as cfg
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

session = vk_api.VkApi(token=cfg.token)
parser = cfg.Parser()

help_page = """
To use me, just type: @freakly_pink mode umode nickname

To list available modes type: @freakly_pink list modes

To list available umodes: @freakly_pink list umodes
"""


while True:
	longpoll = VkBotLongPoll(session, '207927627')
	try:
		for event in longpoll.listen():

			if event.from_chat:
				msg = event.message.text
				if "[club207927627|@freakly_pinkly]" in msg[:29]:

					msg = msg[30:]
					msg_list = msg.split(" ")

					if msg_list[0] == "list":
						if msg_list[1] == "modes":
							session.method('messages.send', {"chat_id": event.chat_id, "message": "Available modes: " + " ".join(parser.available_modes), "random_id": 0})
							continue
						elif msg_list[1] == "umodes":
							available_umodes = []
							for key,value in parser.available_umodes.items():
								available_umode = f"{key}:"
								for i in value:
									available_umode += f" {i}"
								
								available_umodes.append(available_umode + "\n")


							session.method('messages.send', {"chat_id": event.chat_id, "message": " ".join(available_umodes), "random_id": 0})
							continue

						else:
							session.method('messages.send', {"chat_id": event.chat_id, "message": "Так а чо выводить то? Наверно ты ввел umode неправильно ъуъ", "random_id": 0})
							continue

					if msg_list[0] == "help":
						session.method('messages.send', {"chat_id": event.chat_id, "message": help_page, "random_id": 0})
						continue

					try:
						print(msg_list)
						mode, umode, nick = msg_list
					except ValueError:
						session.method('messages.send', {"chat_id": event.chat_id, "message": "Непонял", "random_id": 0})
						continue

					if (mode in parser.available_modes) and (umode in parser.available_umodes[mode]):
						
						result = parser.parsePlanckeIO(mode, umode, nick)

						session.method('messages.send', {"chat_id": event.chat_id, "message": result, "random_id": 0})
				


	except Exception as e:
		print(e)
		continue

