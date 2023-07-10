import speech_recognition as sr
import wikipedia
from gtts import gTTS
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import pyjokes
from twilio.rest import Client


now = datetime.now()


def speak(b):
    tts = gTTS(text=b, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")


#for news update
def news():
    main_url= 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=3ae4390e85474194bcd4255e144ffa1c'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first","second","third","fourth","fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


def speech_to_text():

    required=-1
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "pulse" in name:
            required= index
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=4)
    try:
        input = r.recognize_google(audio)
        return str(input)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


while True:

    speak("Hi, drishya here")

    a = str(speech_to_text())
    print(a)

    if a == "None":
        print(' ')

    elif "date" in a:
        k=now.strftime("Today's date is %A, %B %d, %Y")
        speak(k)

    elif "time" in a:
        time=now.strftime(' %I: %M %p ')
        speak('time is' + time)

    elif a == "who are you":
        speak("I am Drishya, your assistant")

    elif a == "what can you do":
        speak("I can do lot of things, for example you can ask me time, date, weather,Location. I can send emergency messages, make a call,and many more tasks.")

    elif a == "how are you":
        speak("I am fine , how can I help you sir")

    elif a == "thank you":
        speak("It's my pleasure sir, always ready to help you sir")

    elif "temperature" in a:
        search = "temperature in mumbai"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div",class_="BNeawe").text
        speak(f"current {search} is {temp}")

    elif "joke" in a:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "news" in a:
        speak("please wait sir, fetching the latest news")
        news()

    elif a == "you can sleep":
        speak("thanks for using me sir, you can call me anytime.")
        sys.exit()

    elif "location" in a:
        speak("wait sir, let me check")
        speak("We are at Atharva College of Engineering, Mumbai, Maharashtra")

    elif a== 'send emergency message' :
        account_sid = 'AC97212b337621c954299613bc01a35cac'
        auth_token = 'c972876c2dcae69cb871b43033bc1a79'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body='I am Drishya, need urgent help.Please reach me out',
            from_='+13204387919',
            to='+919321633893'
        )

        print(message.sid)
        speak("Message has been sent sir, waiting for your next command")

    elif "call" in a :
        account_sid = 'AC97212b337621c954299613bc01a35cac'
        auth_token = 'c972876c2dcae69cb871b43033bc1a79'
        client = Client(account_sid, auth_token)
        message = client.calls.create(
            twiml='<Response><Say>Call from Drishya, need help.</Say></Response>',
            from_='+13204387919',
            to='+919321633893'
        )
        speak("Phone call has been made sir, waiting for your next command")

    else:
        result=wikipedia.summary(a, sentences=1)
        speak(result)
