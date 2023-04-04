polit = "путин", "байден", "зеленский", "спецопераци", "войн", "байдэн"
link = "https://www.youtube.com", "https://www.youtube.ru", "https://vk.com", "https://github.com", "https://aliexpress.ru", "https://www.thingiverse.com" #Список ссылок, которые разрешены в чате
parasite_symbols = "/-*!@#$^&()+=><?№;~'{}[]_ "
#Импорт необжодимых модулей

from datetime import datetime, date, time, timedelta #Модуль времени
from aiogram import Bot, Dispatcher, executor, types #Модуль для работы с Телеграм
import os #модуль для работы с ОС
import numpy as np #Модуль для работы с массивами
from temp import printTemp #Модуль для получения температуры cpu сервера (самописный)
import time #Модуль времени
import file_manager
import spam_class
import user_log
import log_manager


import white_list #Модуль для обработки белого списка пользователей (самописный)
'''
Белый список - список, в который заносятся пользователи, которых бот проверять не будет
'''

import top #Модуль для работы с топом пользователей по кол-ву сообщений в чате (самописный)


import asyncio
import aioschedule as schedule
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from contextlib import suppress
from sys import platform



from socialc import SocialScore, show, SocialScore_set, SocialScore_setp #Модуль для работы с социальным рейтингом пользователей (самописный)
'''
Социальный рейтинг - база всех пользователей и их рейтинга
При вступлении пользователя в чат, ему выдаётся 500 социального рейтинга
При нарушении правил, социальный рейтинг отнимается на n число (в зависимости от нарушения)
'''




if platform == "linux" or platform == "linux2":
    linux = True
elif platform == "win32":
	linux = False
#logging.basicConfig(level=logging.CRITICAL)

finded = False
triggered = False
up_c = 0
chat_spam_list = []
chat_log_list = log_manager.load_data()

flood_num = 5
maintenace_chat_id = -1001751640711
msg_id = 18

bot = Bot(token="5896801600:AAH9EgH0oAaH7C2kxsOsjqqNvj0IIEpr6V0") #Токен Телеграм бота
dp = Dispatcher(bot)


# Открытие файла с плохими словами, и запись его в переменную. Пример: Плохое слово/Плохое слово 2
try:
	bad_words_file = open('/home/orangepi/bot/bot/filt_l.txt', 'r', encoding = 'utf-8')
	
except Exception:
	bad_words_file = open('filt_l.txt', 'r', encoding = 'utf-8')


bad_words_list = bad_words_file.read().split("/") #Преобразование строки плохих слов в массив


print("Andcool Guard Bot приветствовать вас!\nВы добавить меня в группа и сделать админ.\nЯ навести там порядок!")

async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()
	



@dp.message_handler(content_types=['any'])

async def echo(message: types.Message): # главная функция

	top.add(message.from_user.id, message.chat.id) #Сразу пребавляем 1 к количеству сообщений от пользователя message.from_user.id в топ сообщений
	global maintenace_chat_id
	global msg_id
	if message.chat.id == maintenace_chat_id: await message.delete() # Если сообщение отправлено в информационный чат, удаляем его
	print(message.content_type)

	if message.chat.type != "private" and message.chat.id != maintenace_chat_id: # Если сообщение отправлено в общий чат
		log_txt = []
		answer_log_txt = []
		up_c = 0
		
		global flood_num
		global chat_spam_list
		global chat_log_list

		triggered = False

		if chat_log_list == []: chat_log_list = [user_log.Chat(message.chat.id)]
		else:
			log_finded = False
			for log_list in chat_log_list:
				if log_list.chat_id == message.chat.id: log_finded = True
			if not log_finded: chat_log_list.append(user_log.Chat(message.chat.id))
		current_chat = -1
		current_user = -1
		answer_user = -1
		
		for log_list in range(len(chat_log_list)):
				if chat_log_list[log_list].chat_id == message.chat.id: current_chat = log_list


		if chat_log_list[current_chat].users == []: chat_log_list[current_chat].users = [user_log.User(message.from_user.username)]
		else:
			user_finded = False
			for log_list_users in chat_log_list[current_chat].users:
				if log_list_users.username == message.from_user.username: user_finded = True
			if not user_finded: chat_log_list[current_chat].users.append(user_log.User(message.from_user.username))
		
		for pr in range(len(chat_log_list[current_chat].users)):
			if chat_log_list[current_chat].users[pr].username == message.from_user.username: current_user = pr

		#print(chat_log_list[current_chat].users[current_user].username)
		#------------------FLOOD----------------------

		# Проверка на спам
		'''
		Считаем количесво сообщений от одного пользователя подряд, если >= flood_num, -50 социального рейтинга
		'''
		position_in_list = -1
		spam_return = [-1]
		if len(chat_spam_list) == 0: chat_spam_list = [spam_class.Spam(message.chat.id, flood_num)]
		else: 
			for spam_list_found in range(len(chat_spam_list)):
				if chat_spam_list[spam_list_found].chat_id == message.chat.id: position_in_list = spam_list_found

			if position_in_list != -1: spam_return = chat_spam_list[position_in_list].tick(message.from_user.id, message, message.text)
			else:
				chat_spam_list.append(spam_class.Spam(message.chat.id, flood_num))
				for spam_list_found in range(len(chat_spam_list)):
					if chat_spam_list[spam_list_found].chat_id == message.chat.id: 
						spam_return = chat_spam_list[spam_list_found].tick(message.from_user.id, message, message.text)
						position_in_list = spam_list_found

		
		
		if spam_return[0] != -1:
			log_txt.append(f"{message.from_user.username}, {message.text} -> spam")
			await message.answer(f"{message.from_user.first_name}, прекрати спамить в этом чате!\nСоциальный рейтинг понижен на 50.\nМут на 20 минут!")
			SocialScore(message.from_user.id, -50, message.chat.id)
			
			triggered = True
			dt = datetime.now() + timedelta(minutes=20)
			timestamp = dt.timestamp()
			
			try: await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
			except Exception: pass

			for spam_delete in range(spam_return[1]):
				try: await spam_return[0][spam_delete].delete()
				except Exception: pass
		
			#--------------------------------------------
		supported_content = ["text", "photo", "document", "video"]
		no_text_supported_content = ["photo", "document", "video"]
		if message.content_type in no_text_supported_content:
			try:
				message_txt = message.caption
			except: message_txt = "."
		else: message_txt = message.text
		if message.content_type in supported_content: # Если отправлено текстовое сообщение
			member = await bot.get_chat_member(message.chat.id, message.from_user.id)
			
		#----------------SCORE_SHOW------------------


			if message.reply_to_message: # Если проверяемое сообщение - ответ
				if member.is_chat_admin(): # Если проверяемое сообщение от админа чата

					if chat_log_list[current_chat].users == []: chat_log_list[current_chat].users = [user_log.User(message.reply_to_message.from_user.username)]
					else:
						user_finded = False
						for log_list_users in chat_log_list[current_chat].users:
							if log_list_users.username == message.reply_to_message.from_user.username: user_finded = True
						if not user_finded: chat_log_list[current_chat].users.append(user_log.User(message.reply_to_message.from_user.username))
					
					for pr in range(len(chat_log_list[current_chat].users)):
						if chat_log_list[current_chat].users[pr].username == message.reply_to_message.from_user.username: answer_user = pr


						
					if message_txt == "/sc" or message_txt == "/sc@andcool_bot": # Получение соц. рейтинга у пользователя
						await message.reply(f"Социальный рейтинг пользователя {message.reply_to_message.from_user.first_name} равен {show(message.reply_to_message.from_user.id, message.chat.id)}")

					if message_txt.find("/sc_set") != -1: # Установка соц. рейтинга для пользователя
						sc_am = int(message_txt[message_txt.find("/sc_set") + 8:])
						SocialScore_set(message.reply_to_message.from_user.id, sc_am, message.chat.id)
						answer_log_txt.append(f"Set social score for {message.reply_to_message.from_user.first_name} to {round(sc_am)}")

					if message_txt.find("/p_set") != -1: # Установка степени наказания для пользователя
						sc_am = int(message_txt[message_txt.find("/p_set") + 7:])
						SocialScore_setp(message.reply_to_message.from_user.id, sc_am, message.chat.id)
						answer_log_txt.append(f"Set degree of punishment for {message.reply_to_message.from_user.first_name} to {round(sc_am)}")

					if message_txt.find("/mute") != -1: # Комманда для запрета пользователь писать в чат на n кол-во времени
						mute_t = float(message_txt[message_txt.find("/mute") + 6:])
						answer_log_txt.append(f"{message.reply_to_message.from_user.first_name} is muted for {mute_t} hours")

						dt = datetime.now() + timedelta(hours=mute_t)
						timestamp = dt.timestamp()
						flood = 0
						await message.delete()
						await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)

					if message_txt.find("/ban") != -1: # Блокировка пользователя
						answer_log_txt.append(f"{message.reply_to_message.from_user.first_name} banned")
						await message.delete()
						await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, revoke_messages=False)

					if message_txt == "/white_list_add": #Добавление пользователя в белый список
						done = white_list.add_to_whitelist(message.reply_to_message.from_user.id, message.chat.id)
						if done == False: await message.reply("Пользователь уже в белом списке")

					if message_txt == "/white_list_remove": #Удаление пользователя из белого списка
						done = white_list.remove_from_whitelist(message.reply_to_message.from_user.id, message.chat.id)
						if done == False: await message.reply("Пользователя нет в белом списке")

			else: # Если сообщение не ответ на другое
				if message.from_user.id == 1197005557:
					
					if message_txt == "/reboot":
						os.system("sudo reboot")
					if message_txt == "/shutdown":
						os.system("sudo poweroff")

				if member.is_chat_admin():
					if message_txt.find("/get_chat_id") != -1:
						await message.delete()
						msg = await message.answer(f"{message.chat.id}")
						asyncio.create_task(delete_message(msg, 60))
				#----------------SCORE_SHOW------------------
				# Отображение собственного соц. рейтинга пользователя
				if message_txt == "/sc" or message_txt == "/sc@andcool_bot":
					await message.delete()
					msg = await message.answer(f"{message.from_user.first_name}, ваш социальный рейтинг равен {show(message.from_user.id, message.chat.id)}")
					asyncio.create_task(delete_message(msg, 60))

				
					

				# Отображение топа пользователей по кол-ву сообщений
				if message_txt == "/top":

					topl, count = top.sort(message.chat.id)
					text = "Топ пользователей по количеству сообщений:\n"
					for x_top in range(count):
						member = await bot.get_chat_member(message.chat.id, round(topl[x_top][0]))
						text = text + f"{x_top + 1}. {member.user.first_name} - {round(topl[x_top][1])}\n"
					await message.delete()
					msg = await message.answer(text)
					asyncio.create_task(delete_message(msg, 120))


				#Реализованная, но не использующееся часть кода, отвечающая за игру в русскую рулетку на соц. рейтинг

				'''	
				if message_txt.find("/sc_roulette") != -1:
					try:

						sc_n = show(message.from_user.id, message.chat.id)
						sc_tx = message_txt[message_txt.find("/sc_roulette") + 13:]
						if sc_tx.find("all") != -1:
							sc_rl = sc_n - 1
						else:
							sc_rl = int(sc_tx)
						print(type(sc_n))
						if sc_rl > 1 and sc_rl <= sc_n:
							rand_sc = random.randint(0, 5)
							if rand_sc == 2:
								await message.reply(message.from_user.first_name + " поставил " + str(sc_rl) + " социального рейтинга и выиграл!\n+" + str(sc_rl) + " социального рейтинга")
								SocialScore(message.from_user.id, sc_rl, message.chat.id)
							else:
								await message.reply(message.from_user.first_name + " поставил " + str(sc_rl) + " социального рейтинга и проиграл!\n-" + str(sc_rl) + " социального рейтинга")
								SocialScore(message.from_user.id, sc_rl * -1, message.chat.id)
						else:
							await message.reply("Введите число от 1 до " + str(show(message.from_user.id, message.chat.id)) + "\nПример: /sc_roulette " + str(random.randint(1, sc_n)))
					except Exception:
						await message.reply("Введите число от 1 до " + str(show(message.from_user.id, message.chat.id)) + "\nПример: /sc_roulette " + str(random.randint(1, sc_n)))
				'''

			#--------------------------------------------
			if white_list.is_in(message.from_user.id, message.chat.id) == False: # Если пользователя нет в белом списке


				#----------------CAPS_GUARD------------------ часть кода отвечающая за защиту от капса (считает кол-во заглавных букв в сообщении)
				for mess_ch in range(len(message_txt)):
					if message_txt[mess_ch].isupper():
						up_c += 1
				#--------------------------------------------

				mess = message_txt.lower() # Переводим сообщение в нижний регистр
				


				#-------------------------------------------- Проверка, не является ли сообщение ссылкой, если да и её нет в списке разрешённых удаляем и -50 соц. рейтинга
				finded_link = False
				for i in range(len(link)):
					if mess.find(link[i]) != -1:
						finded_link = True
					if "https://" in mess and not finded_link:
						dt = datetime.now() + timedelta(minutes=20)
						timestamp = dt.timestamp()
			
						try: await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
						except Exception: pass

						log_txt.append(f"{message.from_user.username}, {message_txt} -> link")
						await message.answer("Неизвестные ссылки присылать нельзя! \nСоциальный рейтинг понижен на 50.\nМут на 20 минут!")
						await message.delete()
						SocialScore(message.from_user.id, -50, message.chat.id)
						
						break

				finded_link = False
				
				#--------------------------------------------
				for replace_l in parasite_symbols: mess = mess.replace(str(replace_l), "")

				for i in range(len(polit)):
					if mess.find(polit[i].lower()) != -1:
						dt = datetime.now() + timedelta(minutes=20)
						timestamp = dt.timestamp()
			
						try: await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
						except Exception: pass
						log_txt.append(f"{message.from_user.username}, {message_txt} -> polit")
						await message.answer("Партия запрещать обсуждать политика в этом чате!\nСоциальный рейтинг понижен на 120.\nМут на 20 минут!")
						await message.delete()
						SocialScore(message.from_user.id, -120, message.chat.id)
						
						break
				# Проверка на плохие слова. Берём по одному слову из масива и проверяем, есть ли оно в сообщении, если да, то удаляем и -100 соц. рейтинга
				#----------------FILT------------------------
				
				for i in range(len(bad_words_list)):
					try:
						if mess.find(bad_words_list[i].lower()) != -1:
							dt = datetime.now() + timedelta(minutes=20)
							timestamp = dt.timestamp()
			
							try: await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
							except Exception: pass

							log_txt.append(f"{message.from_user.username}, {message_txt} -> bad word")
							answer = message.from_user.first_name + ", молчать!\n" + "Мат и оскорбления запрещены в этом чате!\n" + "Социальный рейтинг понижен на 100.\nМут на 20 минут!"
							await message.answer(answer)
							await message.delete()
							SocialScore(message.from_user.id, -100, message.chat.id)
							
							break
					except Exception: pass
					#-------------------------------------------


					#-------------CAPS_GUARD-------------------- # Окончательная проверка на капс, если заглавные буквы составляют более 50% от всего сообщения, то -10 соц. рейтинга
				if(up_c * 100) / len(message_txt) >= 50 and len(message_txt) >= 4:
					try:
						dt = datetime.now() + timedelta(minutes=20)
						timestamp = dt.timestamp()
			
						try: await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
						except Exception: pass
						await message.reply("Писать капсом некультурно!\n" + "Социальный рейтинг понижен на 10.\nМут на 20 минут!")
						SocialScore(message.from_user.id, -10, message.chat.id)
					except Exception: pass
					log_txt.append(f"{message.from_user.username}, {message_txt} -> caps")
					
						
					#-------------------------------------------
					

		#------------------------------MUTE-------------------------------------------- 
		#Алгоритм для запрета пользователю писать в чате на время, если его соц. рейтинг <= 0
		#Время, на которое запрещается писать с каждым разом увеличивается 12, 24, 36, 48... часов
		
		sc = file_manager.open("SocialScore", message.chat.id, 3)
		for sc_c in range(len(sc)):
			if sc[sc_c][1] <= 0 and sc[sc_c][0] != 0:


				member = await bot.get_chat_member(message.chat.id, sc[sc_c][0])

				
				if member.status == "member" or member.status == "restricted":
					chat_spam_list[position_in_list].spam_count = 0
					
					await bot.ban_chat_member(message.chat.id, sc[sc_c][0], revoke_messages=False)
					log_txt.append(f"{message.from_user.username} banned")
					
					
					
				
				sc[sc_c][1] = 300
		file_manager.save("SocialScore", message.chat.id, sc)

		now_time_log = datetime.now()

		now_time_format = "{}.{}.{}-{}:{}".format(now_time_log.day, now_time_log.month, now_time_log.year, now_time_log.hour, now_time_log.minute)
		if current_chat != -1 and current_user != -1 and log_txt != []:
			for i_log in log_txt:
				chat_log_list[current_chat].users[current_user].deleted_messages.append(f"[{now_time_format}] {i_log}")


		if current_chat != -1 and answer_user != -1 and answer_log_txt != []:
			for i_log in answer_log_txt:
				chat_log_list[current_chat].users[answer_user].deleted_messages.append(f"[{now_time_format}] {i_log}")

		
		log_manager.save_data(chat_log_list)
		
		
	else:
		if message.text.find("/send_log") != -1:
			
			log_print_list = message.text.split(" ")
			try:
				member = await bot.get_chat_member(log_print_list[1], message.from_user.id)
			
				if member.status == "creator" or member.status == "administrator":
					try:
					#if True:
					
						chat_id_print = -1
						user_id_print = -1
						for log_list in range(len(chat_log_list)):
							if chat_log_list[log_list].chat_id == int(log_print_list[1]): chat_id_print = log_list
						if chat_id_print != -1:
							for pr in range(len(chat_log_list[chat_id_print].users)):
								if chat_log_list[chat_id_print].users[pr].username == log_print_list[2]: user_id_print = pr
							
							if user_id_print != -1 and chat_log_list[chat_id_print].users[user_id_print].deleted_messages != []:
								log_file = open('log_file.txt', 'w')
								for log_txt_write in chat_log_list[chat_id_print].users[user_id_print].deleted_messages:
									
									log_file.write(log_txt_write + '\n')
								log_file.close()
								log_file_send = open("log_file.txt", 'rb')
								await bot.send_document(message.chat.id, log_file_send)
								log_file_send.close()
							else:
								await message.answer("На этого пользователя ещё нет логов")
						else: await message.answer("На этот чат ещё нет логов")


					except Exception as e: await message.answer(f"Извините, произошла какая-то ошибка\n{e}")
				else: await message.answer("Вы не администратор в этом чате!")
			except Exception: await message.answer("Неправильно указан id чата или бот не состоит в этом чате")

			
		elif message.text.find("/help") != -1:
			txt = "Andcool Guard Bot приветствовать вас!\nВы добавить меня в группа и сделать админ.\nЯ навести там порядок!\n" + "Раздаю муты за:\n- Обсуждение политики\n- Нецензурные выражения\n- Сообщения капсом\n- Флуд (куча сообщений подряд)\n\n"
			txt1 = "Команды для админов (ответь на сообщение цели):\n/sc - социальный рейтинг пользователя\n/sc_set - установка социального рейтинга для пользователя\n/p_set - установка степени наказания для пользователя\n/ban - выгнать участника\n/mute 1 - замутить участника на 1 час\n"
			txt2 = "\nБелый список - привилегия, на необработку сообщений ботом\nКоманды белого списка (ответь на сообщение цели):\n/white_list_add - добавить пользователя в белый список\n/white_list_remove - удалить пользователя из белого списка"
			txt3 = "\n/send_log (chat_id) (username)- получить логи пользователя в чате chat_id и именем пользователя username\n/get_chat_id - получить chat_id (использовать в чате)"
			await bot.send_message(chat_id = message.from_user.id, text = txt + txt1 + txt2 + txt3)

		
				

	#------------------------------------------------------------------------------


@dp.message_handler()
async def update_temp():
	try:
		if linux == True:
			fan_state = os.system("sudo cat /sys/class/gpio/gpio228/value")
			await bot.edit_message_text(chat_id = maintenace_chat_id, message_id = msg_id, text = f"Температура {round(printTemp(), 1)}°C {fan_state}")
	except Exception:
		pass
		


      

async def scheduler():
    schedule.every(5).seconds.do(update_temp)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(dp): 
    asyncio.create_task(scheduler())
if __name__ == "__main__":
	started = True
	while started:
		try:
			executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
			started = False
		except Exception:
			started = True
			print("An error has occurred, reboot in 10 seconds")
			time.sleep(10)
			print("rebooting...")
