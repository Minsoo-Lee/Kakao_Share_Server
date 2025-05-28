from automation import automator as a
import os

chat_rooms = []
age = 20

if age > 10:
    chat_rooms = os.getenv("ROOM").split(',')
print(chat_rooms)