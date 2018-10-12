#! /usr/bin/env python
# Author: Emmanouil Kampitakis <madonius@entropia.de>
# Organisation: Entropia e.V.
# Licence: Public Domain

import socketio
from flask import Flask
import eventlet
import eventlet.wsgi

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest

def get_card_id():
    # define the apdus used in this script
    apdu = [0xFF, 0xCA, 0x00, 0x00, 0x00]

    # request card insertion
    card_request = CardRequest(timeout=None, cardType=AnyCardType(), newcardonly=True)
    card_service = card_request.waitforcard()

    # connect to the card and perform a few transmits
    card_service.connection.connect()
    response, sw1, sw2 = card_service.connection.transmit(apdu)
    rfid_string = '_'.join([str(id_val) for id_val in response])

    return rfid_string

card_server = socketio.AsyncServer()
app = Flask(__name__)

@card_server.on('card')
async def card(card_id):
    """
    :param card_id: The RFID-Card's id
    :type: str
    :return: None
    """
    await card_server.emit(data=card_id)

if __name__ == '__main__':
    app = socketio.Middleware(card_server, app)
    eventlet.wsgi.server(eventlet.listen(('',24421)),app)

    while True:
        try:
            rfid_string = get_card_id()
            if rfid_string: card_server.emit(card(rfid_string))
        except:
            continue