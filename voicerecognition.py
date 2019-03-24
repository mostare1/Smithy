import speech_recognition as sr



def voice_rec():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Say Something")
        audio = r.listen(source)
        print("waiting")
        #print("time over, thanks")

    print('its working so far')
    try:
        text = r.recognize_google(audio)
        print('it worked')
        return str(text)
    
    except:
        return "Your message wasn't clear"