#!/usr/bin/python3
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

from time import sleep

class PrintObserver(CardObserver):
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))

if __name__ == '__main__':
    cardmonitor = CardMonitor()
    cardobserver = PrintObserver()
    cardmonitor.addObserver(cardobserver)

    sleep(10)

    cardmonitor.deleteObserver(cardobserver)
