from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

conversaciones = []

class Trainer:
    chatbot = ChatBot('LimbertBoot')

    trainer = ListTrainer(chatbot)

    trainer.train(conversaciones)

    response = chatbot.get_response('como estas')

