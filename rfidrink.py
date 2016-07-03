#! /usr/bin/env python
from pykeyboard import PyKeyboard
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString

while True:
    try:
        # define the apdus used in this script
        SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]

        # request card insertion
        cardrequest = CardRequest(timeout=None, cardType=AnyCardType(), newcardonly=True)
        cardservice = cardrequest.waitforcard()

        # connect to the card and perform a few transmits
        cardservice.connection.connect()
        apdu = SELECT
        response, sw1, sw2 = cardservice.connection.transmit(apdu)
        rfid_string = '_'.join(map(str, response))

        keyboard = PyKeyboard()
        keyboard.type_string('RFID_ID_'+rfid_string)
    except:
        continue
