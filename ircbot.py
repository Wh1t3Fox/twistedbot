#!/usr/bin/env python

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor


from datetime import datetime
from random import random
import logging
import argparse
import time
import os

from plugins import *

class MyBot(irc.IRCClient):

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
        logging.info(msg)
        user = user.split('!', 1)[0]

        if msg.startswith('!isup'):
            try:
                command, site = msg.split(' ', 2)
                msg = isup.ISUP(site).status
            except:
                msg = "Your formatting is incorrect"

            self.msg(channel, msg)

        elif msg.startswith('!fortune'):
            msg = fortune.Fortune().msg
            self.msg(channel, msg)

        elif msg.startswith('!hash'):
            command, alg, message = msg.split(' ', 2)
            h = hashes.Hash(alg, message)
            self.msg(channel, h.result)

        #look for youtube link
        elif msg.find("youtube.com/watch?v=") != -1:
            pos = msg.find('youtube')+20
            token = msg[pos:pos + 11]
            info = youtube.Youtube(token)
            self.msg(channel, info.title)
            self.msg(channel, info.author)
            self.msg(channel, info.description)

        #get the url and lets print the title of the page
        elif msg.find('http') != -1:
            if msg.find(' ') != -1:
                url = msg[msg.find('http'):msg.find(' ')]
            else:
                url = msg[msg.find('http'):]
            info = webpage.Webpage(url)
            self.msg(channel, info.title)


        #Not a command so build corpus or talk
        else:
            msg = ' '.join(msg.split()[1:])
            speak.add_to_brain(msg, self.factory.chain_length, write_to_file=True)
            if random() <= self.factory.chattiness:
                sentence = speak.generate_sentence(msg, self.factory.chain_length,self.factory.max_words)
                #private message
                if channel == self.nickname and sentence:
                    self.msg(user, sentence)
                    return

                #channel message to me
                if msg.startswith(self.nickname) and sentence:
                    self.msg(channel, sentence)

#Interfaces the bot with Twisted
class MyBotFactory(protocol.ClientFactory):

    def __init__(self, channel, nickname, password=None, chain_length=3, chattiness=1.0, max_words=10000):
        self.channel = channel
        self.nickname = nickname
        self.password = password
        self.booted = datetime.now()
        self.chain_length = chain_length
        self.chattiness = chattiness
        self.max_words = max_words

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

    if os.path.exists('corpus.txt'):
        with open('corpus.txt', 'r') as fr:
            for line in fr:
                speak.add_to_brain(line, 3)

    f = MyBotFactory("b01lers", "BotMaster")
    reactor.connectTCP("irc.freenode.net", 6667, f)
    reactor.run()
