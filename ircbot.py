#!/usr/bin/env python

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

from datetime import datetime
import logging
import argparse
import time
import os

from plugins import *

class MyBot(irc.IRCClient):

    COLORS = {
            'white': '\x030',
            'black': '\x031',
            'navy': '\x032',
            'green': '\x033',
            'red': '\x034',
            'maroon': '\x035',
            'purple': '\x036',
            'olive': '\x037',
            'yellow': '\x038',
            'lime': '\x039',
            'teal': '\x0310',
            'cyan': '\x0311',
            'blue': '\x0312',
            'pink': '\x0313',
            'grey': '\x0314',
            'silver': '\x0315'
    }

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    #signed on to network
    def signedOn(self):
        logging.info("[+] Signed on to network")
        if self.factory.password:
            self.msg("NickServ", "IDENTIFY %s" % (self.factory.password,))
        self.join(self.factory.channel)

    #joined a channel
    def joined(self, channel):
        logging.info("[+] Joined %s" % channel)

    #receive message
    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]

        #private message
        if channel == self.nickname:
            self.msg(user, "hi there")
            return

        #channel message to me
        if msg.startswith(self.nickname):
            msg = "I'm a work in progress"
            self.msg(channel, msg)

        if msg.startswith('!fortune'):
            msg = fortune.Fortune().msg
            self.msg(channel, msg)

        if msg.startswith('!hash'):
            command, alg, message = msg.split(' ', 2)
            h = hashes.Hash(alg, message)
            self.msg(channel, h.result)

        #look for youtube link
        if msg.find("youtube.com/watch?v=") != -1:
            pos = msg.find('youtube')+20
            token = msg[pos:pos + 11]
            info = youtube.Youtube(token)
            self.msg(channel, info.title)
            self.msg(channel, info.author)
            self.msg(channel, info.description)


#Interfaces the bot with Twisted
class MyBotFactory(protocol.ClientFactory):

    def __init__(self, channel, nickname, password=None):
        self.channel = channel
        self.nickname = nickname
        self.password = password
        self.booted = datetime.now()

    def buildProtocol(self, addr):
        p = MyBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        logging.info("[-] Client Connection Lost: {0}".format(reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        logging.info("[-] Could not connect: {0}".format(reason))
        reactor.stop()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename='ircbot.log',level=logging.INFO)

    f = MyBotFactory("b01lers", "Wh1t3FoxTesting_")
    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()
