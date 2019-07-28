# -*- coding: utf-8 -*-
from telethon import TelegramClient, sync
from telethon.errors.rpcerrorlist import FloodWaitError
import os
from time import sleep
import logging
from telethon.tl.types import PeerUser

logger = logging.getLogger(__name__)


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
           'вакансии, или искать работу.\n\nМы учли все недостатки' \
           ' существующих ботов в телеграм, и создали очень удобного' \
           ' и просто бота.'

    print('I start the newsletter')

    count = len(ids)
    counter = 0

    def _send(ids):
        for send_id in ids:
            nonlocal counter
            counter += 1
            print('I send to client msg')
            user = client.get_entity(PeerUser(send_id))
            sec = None
            try:
                client.send_message(user, text)
            except FloodWaitError as error:
                msg = error.message
                sec = msg.split(' ')[3]

            nonlocal count
            count -= 1
            print('Отправлено: {}'.format(counter))
            print('Осталось отправить: {}'.format(count))

            print('I sleep 5 seconds')
            sleep(sec)
            print('continue')

        return print('I finished the newsletter')

    return _send(ids)


if __name__ == '__main__':
    print('Start Sender')
    print(sync)
    main()
