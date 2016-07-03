#! /usr/bin/env python
# Author: Emmanouil Kampitakis <madonius@entropia.de>
# Organisation: Entropia e.V.
# Licence: Public Domain

from pykeyboard import PyKeyboard
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest

def main():
    """
        Retrieves the ID of the attached Card and returns it as keyboard-presses
    """
    while True:
        try:
            # define the apdus used in this script
            apdu = [0xFF, 0xCA, 0x00, 0x00, 0x00]

            # request card insertion
            card_request = CardRequest(timeout=None, cardType=AnyCardType(), newcardonly=True)
            card_service = card_request.waitforcard()

            # connect to the card and perform a few transmits
            card_service.connection.connect()
            response, sw1, sw2 = card_service.connection.transmit(apdu)
            rfid_string = '_'.join([str(id_val) for id_val in response])

            keyboard = PyKeyboard()
            keyboard.type_string('RFID_ID_'+rfid_string)
        except:
            continue

if __name__ == '__main__':
    main()
