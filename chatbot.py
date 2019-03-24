from chatterbot import ChatBot
from weather import print_temp
chatbot = ChatBot("Gigel cel mai bot")

from chatterbot.trainers import ListTrainer
import datetime
chatbot.storage.drop()

now = datetime.datetime.now()

trainer = ListTrainer(chatbot)#

trainer.train([
    "Hello",
    "Hello dear user",
    "Have a good day"

    
])

trainer.train([
    "How are you?",
    "Great!",

    
])
trainer.train([
    "what's your name",
    "My name is Smithy"
])
trainer.train([
    "What's my bank account",
    "Your IBAN code is:"
])
trainer.train([
    "How many cash do I have?",
    "$..."
])
trainer.train([
    "What's my health?",
    "You are Healthy"
])
trainer.train([
    "Health",
    "Healthy"
])
trainer.train([
    "bank account",
    "$200"
])
trainer.train([
    "Tell me a Joke",
    "Why is Peter Pan flying all the time? He Neverlands!",
    "What do you get when you cross a snake with a tasty dessert? A pie-thon!",
    "Where did the vampire college student go clothes shopping? Forever 21",
    "My email password has been hacked. That’s the third time I’ve had to rename the cat.",
])
trainer.train([
    "take me to home",
    "Homepage_link"
])
trainer.train([
    "take me to health",
    "Healthpage_link"
])
trainer.train([
    "take me to weather",
    "Weatherpage_link"
])
trainer.train([
    "take me to bank",
    "Bankpage_link"
])
trainer.train([
    "take me to office",
    "Officepage_link"
])
trainer.train([
    "Take me to calendar",
    "Calendar_link"
])
trainer.train([
    "How is the traffic",
    "traficpage_link"
])


### mark safe 
###muzica 


#trainer.train(conversation)

def chat(input_data):
    response = chatbot.get_response(input_data)
    return response

   
