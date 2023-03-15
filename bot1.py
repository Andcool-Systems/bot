link = "https://www.youtube.com", "https://www.youtube.ru", "https://vk.com", "https://github.com", "https://aliexpress.ru", "https://www.thingiverse.com" #Список ссылок, которые разрешены в чате

#Импорт необжодимых модулей
import logging 
from datetime import datetime, date, time, timedelta #Модуль времени
from aiogram import Bot, Dispatcher, executor, types #Модуль для работы с Телеграм
import os #модуль для работы с ОС
import numpy as np #Модуль для работы с массивами
import random #Модуль рандома
from temp import printTemp #Модуль для получения температуры cpu сервера (самописный)
import time #Модуль времени
import fan #Модуль для работы с вентиляторами CPU (самописный)

import white_list #Модуль для обработки белого списка пользователей (самописный)
'''
Белый список - список, в который заносятся пользователи, которых бот проверять не будет
'''

import top #Модуль для работы с топом пользователей по кол-ву сообщений в чате (самописный)


import asyncio
import aioschedule
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from contextlib import suppress




from socialc import SocialScore, show, SocialScore_set, SocialScore_setp #Модуль для работы с социальным рейтингом пользователей (самописный)
'''
Социальный рейтинг - база всех пользователей и их рейтинга
При вступлении пользователя в чат, ему выдаётся 500 социального рейтинга
При нарушении правил, социальный рейтинг отнимается на n число (в зависимости от нарушения)
'''

import magic_filter




finded = False
triggered = False
up_c = 0
last_id = 0
flood = 0

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
	
	
	if message.chat.id == -1001751640711: await message.delete() # Если сообщение отправлено в информационный чат, удаляем его


	if message.chat.type != "private": # Если сообщение отправлено в общий чат

		up_c = 0
		global last_id
		global flood
		triggered = False
		#------------------FLOOD----------------------

		# Проверка на спам
		'''
		Считаем количесво сообщений от одного пользователя подряд, если >= 10, -50 социального рейтинга
		'''
		if last_id == message.from_user.id:
			flood += 1
		else:
			flood = 0
		if flood >=10:
			await message.answer(message.from_user.first_name + ", прекрати спамить в этом чате!\n" + "Социальный рейтинг понижен на 50.")
			SocialScore(message.from_user.id, -50, message.chat.id)
			flood = 0
			if triggered == False:
				print(message.from_user.first_name + ', ' + message.text + " -> flood")
			triggered = True
		last_id = message.from_user.id
			#--------------------------------------------

		if message.content_type == "text": # Если отправлено текстовое сообщение
			member = await bot.get_chat_member(message.chat.id, message.from_user.id)
			
		#----------------SCORE_SHOW------------------


			if message.reply_to_message: # Если проверяемое сообщение - ответ
				if member.is_chat_admin(): # Если проверяемое сообщение от админа чата

					if message.text == "/sc" or message.text == "/sc@andcool_bot": # Получение соц. рейтинга у пользователя
						await message.reply("Социальный рейтинг пользователя " + message.reply_to_message.from_user.first_name + " равен " + str(show(message.reply_to_message.from_user.id, message.chat.id)))

					if message.text.find("/sc_set") != -1: # Установка соц. рейтинга для пользователя
						sc_am = int(message.text[message.text.find("/sc_set") + 8:])
						SocialScore_set(message.reply_to_message.from_user.id, sc_am, message.chat.id)

					if message.text.find("/p_set") != -1: # Установка степени наказания для пользователя
						sc_am = int(message.text[message.text.find("/p_set") + 7:])
						SocialScore_setp(message.reply_to_message.from_user.id, sc_am, message.chat.id)

					if message.text.find("/mute") != -1: # Комманда для запрета пользователь писать в чат на n кол-во времени
						mute_t = float(message.text[message.text.find("/mute") + 6:])
						dt = datetime.now() + timedelta(hours=mute_t)
						timestamp = dt.timestamp()
						flood = 0
						await message.delete()
						await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)

					if message.text.find("/ban") != -1: # Блокировка пользователя
						await message.delete()
						await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, revoke_messages=False)

					if message.text == "/white_list_add": #Добавление пользователя в белый список
						done = white_list.add_to_whitelist(message.reply_to_message.from_user.id, message.chat.id)
						if done == False:
							await message.reply("Пользователь уже в белом списке")

					if message.text == "/white_list_remove": #Удаление пользователя из белого списка
						done = white_list.remove_from_whitelist(message.reply_to_message.from_user.id, message.chat.id)
						if done == False:
							await message.reply("Пользователя нет в белом списке")

			else: # Если сообщение не ответ на другое
				if message.from_user.id == 1197005557:
					
					if message.text == "/reboot":
						os.system("sudo reboot")
					if message.text == "/shutdown":
						os.system("sudo poweroff")
				#----------------SCORE_SHOW------------------
				# Отображение собственного соц. рейтинга пользователя
				if message.text == "/sc" or message.text == "/sc@andcool_bot":
					await message.delete()
					msg = await message.answer(message.from_user.first_name + ", ваш социальный рейтинг равен " + str(show(message.from_user.id, message.chat.id)))
					asyncio.create_task(delete_message(msg, 60))

				# Отображение топа пользователей по кол-ву сообщений
				if message.text == "/top":

					topl, count = top.sort(message.chat.id)
					text = "Топ пользователей по количеству сообщений:\n"
					for x_top in range(count):
						member = await bot.get_chat_member(message.chat.id, round(topl[x_top][0]))
						text = text + f"{x_top + 1}. {member.user.first_name} - {round(topl[x_top][1])}\n"
					await message.reply(text)


				#Реализованная, но не использующееся часть кода, отвечающая за игру в русскую рулетку на соц. рейтинг

				'''	
				if message.text.find("/sc_roulette") != -1:
					try:

						sc_n = show(message.from_user.id, message.chat.id)
						sc_tx = message.text[message.text.find("/sc_roulette") + 13:]
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
				for mess_ch in range(len(message.text)):
					if message.text[mess_ch].isupper():
						up_c += 1
				#--------------------------------------------

				mess = message.text.lower() # Переводим сообщение в нижний регистр



				#-------------------------------------------- Проверка, не является ли сообщение ссылкой, если да и её нет в списке разрешённых удаляем и -50 соц. рейтинга
				finded_link = False
				for i in range(len(link)):
					if mess.find(link[i]) != -1:
						finded_link = True
					if "https://" in mess and not finded_link:
						await message.answer("Неизвестные ссылки присылать нельзя! \nСоциальный рейтинг понижен на 50.")
						await message.delete()
						SocialScore(message.from_user.id, -50, message.chat.id)
						break

				finded_link = False
				#--------------------------------------------


				# Проверка на плохие слова. Берём по одному слову из масива и проверяем, есть ли оно в сообщении, если да, то удаляем и -100 соц. рейтинга
				#----------------FILT------------------------
				try:
					for i in range(len(bad_words_list)):
						if mess.find(bad_words_list[i].lower()) != -1:
							answer = message.from_user.first_name + ", молчать!\n" + "Мат и оскорбления запрещены в этом чате!\n" + "Социальный рейтинг понижен на 100."
							await message.answer(answer)
							await message.delete()
							SocialScore(message.from_user.id, -100, message.chat.id)
							flood = 0
							if triggered == False:
								print(message.from_user.first_name + ', ' + message.text + " -> swearing")
							triggered = True
							break
					#-------------------------------------------


					#-------------CAPS_GUARD-------------------- # Окончательная проверка на капс, если заглавные буквы составляют более 50% от всего сообщения, то -10 соц. рейтинга
					if(up_c * 100) / len(message.text) >= 50 and len(message.text) >= 4:
						await message.reply("Писать капсом некультурно!\n" + "Социальный рейтинг понижен на 10.")
						if triggered == False:
							print(message.from_user.first_name + ', ' + message.text + " -> CAPS")
						triggered = True
						SocialScore(message.from_user.id, -10, message.chat.id)
						flood = 0
					#-------------------------------------------

				except Exception:
					pass

			



		#------------------------------MUTE-------------------------------------------- 
		#Алгоритм для запрета пользователю писать в чате на время, если его соц. рейтинг <= 0
		#Время, на которое запрещается писать с каждым разом увеличивается 12, 24, 36, 48... часов
		
		if os.path.exists("SocialScore" + str(message.chat.id) +".npy") == False:
			sc = np.zeros((3, 100))
			for sc_c_f in range(99):
				sc[1][sc_c_f] = 500

		else:
			sc = np.load("SocialScore" + str(message.chat.id) +".npy")

		for sc_c in range(99):
			#print(sc[1][sc_c])
			if sc[1][sc_c] == 0 or sc[1][sc_c] < 0:
				mutted = False
				member = await bot.get_chat_member(message.chat.id, sc[0][sc_c])
				print(member)
				if member.status == "member" or member.status == "restricted":
					sc[2][sc_c] += 1
					dt = datetime.now() + timedelta(hours=12 * sc[2][sc_c])

					timestamp = dt.timestamp()
					await message.answer(member.user.first_name + "!\nВы себя плохо ведёте!\n" + "Мут на " + str(round(12 * sc[2][sc_c])) + " часа!\n")
					mutted = await bot.restrict_chat_member(message.chat.id, sc[0][sc_c], types.ChatPermissions(False), until_date = timestamp)
					
				
				sc[1][sc_c] = 300
				np.save("SocialScore" + str(message.chat.id) +".npy", sc)
		
	else:
		
		txt = "Andcool Guard Bot приветствовать вас!\nВы добавить меня в группа и сделать админ.\nЯ навести там порядок!\n" + "Раздаю муты за:\n- Обсуждение политики\n- Нецензурные выражения\n- Сообщения капсом\n- Флуд (куча сообщений подряд)\n\n"
		txt1 = "Команды для админов (ответь на сообщение цели):\n/sc - социальный рейтинг пользователя\n/sc_set - установка социального рейтинга для пользователя\n/p_set - установка степени наказания для пользователя\n/ban - выгнать участника\n/mute 1 - замутить участника на 1 час\n"
		txt2 = "\nБелый список - привилегия, на необработку сообщений ботом\nКоманды белого списка (ответь на сообщение цели):\n/white_list_add - добавить пользователя в белый список\n/white_list_remove - удалить пользователя из белого списка"
		await bot.send_message(chat_id = message.from_user.id, text = txt + txt1 + txt2)

	#------------------------------------------------------------------------------


@dp.message_handler()
async def choose_your_dinner():
    try:
    	await bot.edit_message_text(chat_id = -1001751640711, message_id = 18, text = f"Температура {round(printTemp(), 1)}°C")
    except Exception:
    	pass




async def scheduler():
    aioschedule.every(5).seconds.do(choose_your_dinner)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(dp): 
    asyncio.create_task(scheduler())
if __name__ == "__main__":
	started = True
	while started:
		try:
			executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
			started = False
		except Exception:
			started = True
			print("An error has occurred, reboot in 10 seconds")
			time.sleep(10)
			print("rebooting...")


