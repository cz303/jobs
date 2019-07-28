from telethon import TelegramClient
import os
from time import sleep
from telethon.tl.types import PeerUser


def main():
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')

    client = TelegramClient('kolya', api_id, api_hash)
    client.start()

    print('Start find clients')
    participants = client.get_participants('u_job')
    ids = list(map(lambda x: x.id, participants))
    print('I findes {} clients'.format(len(ids)))

    text = 'Добрый день.\n\nНаша команда разработала замечательного бота для '\
           'поиска работы: @RS_Work_bot\n\nВы можете создавать в нём свои ' \
           'вакансии, или искать работу.\n\nМы учли все недостатки ' \
           'существующих ботов в телеграм, и создали очень' \
           ' удобного и просто бота.'

    print('I start the newsletter')

    for send_id in ids:
        print('I send to client msg')
        user = client.get_entity(PeerUser(send_id))
        client.send_message(user, text)
        print('I sleep 5 seconds')
        sleep(5)
        print('continue')

    return print('I finished the newsletter')


if __name__ == '__main__':
    print('Start Sender')
    main()
