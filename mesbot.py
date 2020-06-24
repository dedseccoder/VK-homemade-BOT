import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token='тут токен группы')

i = 0
id_of_users = []


def remember (id_add):
    id_of_users.append(id_add)

def forget (id_delete):
    id_of_users.remove(id_delete)



def sender(id,text):
    vk_session.method("messages.send", {'user_id' : id, 'message' : text, 'random_id' : 0})



longpool = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        msg = event.text.lower()
        user_id = event.user_id
        if msg == "подписаться":
            remember (user_id)
            sender (user_id, "оки, доки, ты подписан на мои сообщения, надеюсь мой разработчик не будет тебе спамить :3")
        if msg == "отписаться":
            forget (user_id)
            sender (user_id, "оки, теперь ты отписан :3")
        if msg == "покажи id":
            while i < len(id_of_users):
                sender (user_id, id_of_users[i])
                i = i + 1
            i = 0
        if msg == "отправить всем":
            for event in longpool.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    spam = event.text.lower()
                    while i < len(id_of_users):
                        sender (id_of_users[i], spam)
                        i = i + 1
                    i = 0
                    break
