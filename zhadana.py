import re
import os
import sys
import time
import traceback

try:
	import pyowm
	import configparser
	from cfgParser import *
	from gtts import gTTS
	import speech_recognition as sr

except Exception as e:
	print('''На жаль, сталася помилка. Наймовірніше, у Вас не встановлено необхідні бібліотеки Python.'
Ми можемо спробувати встановити їх самочинно (для цього вказівковий рядок має бути запущений з підвищеними правами).
Якщо ви згодні, двічі натисніть "Ввід", якщо ні - закрийте вказівковий рядок. Зауважте, програма написана на Python 3.7.2.
Код помилки:''')
	traceback.print_exc()
	print("Якщо Ви впевнені, що помилка не пов'язана з відсутністю бібліотек, надішліть код помилки розробнику")
	input('Натисніть "Ввід", щоб підтвердити встановлення')
	input('Натисніть "Ввід" ще раз, щоб підтвердити')
	if sys.platform == 'win32':
		os.system('pip install gTTS')
		os.system('pip install SpeechRecognition')
		os.system('pip install pipwin')
		os.system('pip install pyowm')
		os.system('pip install configparser')
		os.system('pipwin install pyaudio')
		import pyowm
		import configparser
		from cfgParser import *
		from gtts import gTTS
		import speech_recognition as sr
	else:
		os.system('pip install gTTS')
		os.system('pip install SpeechRecognition')
		os.system('pip install pyowm')
		os.system('pip install configparser')
		os.system('pip install pyaudio')
		import pyowm
		import configparser
		from cfgParser import *
		from gtts import gTTS
		import speech_recognition as sr

owm_data = pyowm.OWM(API_key='45df05b9b355c1d0ebe3d019e5e17021',language='uk')

def ZhadanaSay(textSay='Пустий текст'):
	zhadanaSay = textSay
	tts = gTTS(zhadanaSay,lang='uk')
	tts.save('zhadana.mp3')
	os.system('zhadana.mp3')
	print('Жадана: ',zhadanaSay)

try:
	cfgFile = 'config.ini'
	cfg = get_config(cfgFile)
except:
	create_config(cfgFile)

r = sr.Recognizer()
ZhadanaSay("Будь ласка, зачекайте, здійснюється прибирання шумів...")

with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source, duration=5)

ZhadanaSay('Шуми успішно прибрано')
time.sleep(1.5)
if sys.platform == 'win32':
	os.system('cls')
elif sys.platform == 'linux':
	os.system('clear')

'''
zhadanaSay = "Привіт, ми не знайомі. Будь ласка, скажи як тебе звуть. Скажи тільки ім'я, додаткових слів казати не потрібно, бо тоді я заплутаюсь"
tts = gTTS(zhadanaSay,lang='uk')
tts.save('zhadana.mp3')
os.system('start zhadana.mp3')
print('Жадана: ',zhadanaSay)
'''

username = get_setting(cfgFile,'Settings','USERNAME')

if username == '[NO_USERNAME]':
	ZhadanaSay("Привіт, ми не знайомі. Будь ласка, скажи як тебе звуть. Скажи тільки ім'я, додаткових слів казати не потрібно, бо тоді я заплутаюсь")
	with sr.Microphone() as source:
		audio = r.listen(source)
	# recognize speech using Google Speech Recognition
	try:
		# for testing purposes, we're just using the default API key
		# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
		# instead of `r.recognize_google(audio)`
		#print("Ви сказали: " + r.recognize_google(audio, language='uk-UA'))
		#print(r.recognize_google(audio, language='uk-UA'))
		username = r.recognize_google(audio, language='uk-UA').capitalize()
		#if r.recognize_google(audio, language='uk-UA').lower() == 'привіт жадана':
		ZhadanaSay('Рада знайомству, '+username+', я - Жадана, твій особистий помічник у твоєму обчислювачі')
		time.sleep(6.5)
		set_setting(cfgFile,'Settings','USERNAME',username)
		ZhadanaSay('''Твоє ім'я збережено в моїй пам'яті, і наступного разу я більше не питатиму, як тебе звуть. Якщо ти захочеш його змінити, скажи мені "Жадано, змінити ім'я" ''')
		time.sleep(14)
	except sr.UnknownValueError:
		print("Розпізнавання мовлення Google не змогло розпізнати голос")
	except sr.RequestError as e:
		print("Не вдалося подати запит на отримання підсумків від служби розпізнавання мовлення Google; {0}".format(e))
else:
	ZhadanaSay('Вітаю '+username+'! Рада тебе бачити')
	time.sleep(2)

ZhadanaSay('Я готова до роботи. Лишень скажи "Гей, Жадано". Щоб вимкнути мене, скажи "Прощавай, Жадано"')

while True:
	try:
		with sr.Microphone() as source:
			audio = r.listen(source)

		# Сигнатури вказівок Жадани
		heyZhadano = \
		re.search(r'ге',r.recognize_google(audio, language='uk-UA').lower())\
		and re.search(r'жадан',r.recognize_google(audio, language='uk-UA').lower())
		goodbayZhadano = \
		re.search(r'прощавай',r.recognize_google(audio, language='uk-UA').lower())\
		and re.search(r'жадан',r.recognize_google(audio, language='uk-UA').lower())
		clearPrompt = \
		re.search(r'жадан',r.recognize_google(audio, language='uk-UA').lower())\
		and re.search(r'очистити рядок',r.recognize_google(audio, language='uk-UA').lower())
		changeName = \
		re.search(r'жадан',r.recognize_google(audio, language='uk-UA').lower())\
		and re.search(r"змінити ім'я",r.recognize_google(audio, language='uk-UA').lower())
		zhadanaRestart = \
		re.search(r'жадан',r.recognize_google(audio, language='uk-UA').lower())\
		and re.search(r"перезапусти",r.recognize_google(audio, language='uk-UA').lower())
		changeTown = \
		re.search(r'жадан',r.recognize_google(audio, language='uk-UA').lower())\
		and re.search(r"змінити місце проживання",r.recognize_google(audio, language='uk-UA').lower())

		#print(username+': '+r.recognize_google(audio, language='uk-UA'))
		if heyZhadano:
			print(username+': гей, Жадано')
			ZhadanaSay('В очікуванні вказівок')
			twPass = False
			while True:
				with sr.Microphone() as source:
					audio = r.listen(source)
				if r.recognize_google(audio, language='uk-UA').lower() == 'яке сьогодні число':
					if time.strftime('%A') == 'Monday':
						weekday = 'понеділок'
					if time.strftime('%A') == 'Tuesday':
						weekday = 'вівторок'
					if time.strftime('%A') == 'Wednesday':
						weekday = 'середа'
					if time.strftime('%A') == 'Thursday':
						weekday = 'четвер'
					if time.strftime('%A') == 'Friday':
						weekday = "п'ятниця"
					if time.strftime('%A') == 'Saturday':
						weekday = 'субота'
					if time.strftime('%A') == 'Sunday':
						weekday = 'неділя'
					presentTime = time.strftime('%d/%m/%Y, %H:%M,')
					ZhadanaSay('Сьогодні '+presentTime+' '+weekday)
					break
				if r.recognize_google(audio, language='uk-UA').lower() == 'котра година':
					ZhadanaSay(time.strftime('%H:%M'))
					break
				if r.recognize_google(audio, language='uk-UA').lower() == 'яка погода':
					townWeather = get_setting(cfgFile,'Settings','TOWN')
					if townWeather == '[NO_TOWN]':
						twPass = True
						ZhadanaSay('Скажи назву міста, про яке хочеш взнати. Поки що підтримуються лише українські міста')
						with sr.Microphone() as source:
							audio = r.listen(source)
						townWeather = r.recognize_google(audio,language='uk-UA').capitalize()
					try:
						observation = owm_data.weather_at_place(townWeather+',UA')
						w = observation.get_weather()
						temp = w.get_temperature('celsius')
						status = w.get_detailed_status()
						humidity = w.get_humidity()
						ZhadanaSay('Температура у місті '+townWeather+' '+str(round(temp.get('temp')))+'°. '+'Рівень вологості '+str(humidity)+'%. '+status.capitalize())
						if twPass == True:
							time.sleep(8)
							set_setting(cfgFile,'Settings','TOWN',townWeather)
							ZhadanaSay('Місто збережено як місце проживання. Щоб його змінити, скажи "Жадано, змінити місце проживання"')
							twPass = False

					except pyowm.exceptions.api_response_error.NotFoundError:
						ZhadanaSay('Мені не вдалося знайти населений пункт під назвою "'+townWeather+' в Україні". Впевнися, що говориш про українське місто і воно справді існує')
					except Exception:
						print('Сталася помилка: ',traceback.print_exc())
						input('Натисніть Ввід')

					break
				if r.recognize_google(audio, language='uk-UA').lower() == 'скасувати':
					ZhadanaSay('Надання вказівки скасовано')
					break
				else:
					ZhadanaSay('Вибачте, я не змогла розпізнати вказівку: '+r.recognize_google(audio, language='uk-UA'))

		elif goodbayZhadano:
			print(username+': прощавай, Жадано')
			ZhadanaSay('Що ж, до побачення, '+username)
			time.sleep(3)
			exit()
		elif changeName:
			print(username+": Жадано, змінити ім'я")
			ZhadanaSay("Твоє нинішнє ім'я - "+username+". Яке нове ім'я ти хочеш встановити?")
			time.sleep(3)
			with sr.Microphone() as source:
				audio = r.listen(source)
			if r.recognize_google(audio, language='uk-UA').lower() == 'скасувати':
				ZhadanaSay('Зміну імені скасовано')
			else:
				username = r.recognize_google(audio, language='uk-UA').capitalize()
				f = open("username.txt", "w")
				f.write(username)
				f.close()
				ZhadanaSay("Нове ім'я встановлено успішно. Віднині ти "+username)
		elif changeTown:
			print(username+": Жадано, змінити місце проживання")
			ZhadanaSay('Скажи назву населеного пункту, в якому живеш')
			with sr.Microphone() as source:
				audio = r.listen(source)
			townWeather = r.recognize_google(audio, language='uk-UA').capitalize()
			set_setting(cfgFile,'Settings','TOWN',townWeather)
			ZhadanaSay('Місце проживання успішно змінено. Віднині ти живеш у населеному пункті "'+townWeather+'"')
		elif clearPrompt:
			if sys.platform == 'win32':
				os.system('cls')
				ZhadanaSay('Вказівковий рядок успішно очищено')
			elif sys.platform == 'linux':
				os.system('clear')
				ZhadanaSay('Вказівковий рядок успішно очищено')
		elif zhadanaRestart:
			print(username+': Жадано, перезапустись')
			ZhadanaSay('Здійснюю самоперезапуск')
			time.sleep(1)
			os.system('python zhadana.py')
			exit()
		elif r.recognize_google(audio, language='uk-UA').lower() == "жадана здійснити прибирання шумів":
			with sr.Microphone() as source:
				ZhadanaSay('Здійснюю прибирання шумів, зачекайте будь ласка')
				r.adjust_for_ambient_noise(source, duration=5)
				ZhadanaSay('Шуми успішно прибрано')

	except sr.UnknownValueError:
		print("Розпізнавання мовлення Google не змогло розпізнати голос")
	except sr.RequestError as e:
		print("Не вдалося подати запит на отримання підсумків від служби розпізнавання мовлення Google; {0}".format(e))