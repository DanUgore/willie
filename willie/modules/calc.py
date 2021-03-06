# coding=utf-8
"""
calc.py - Willie Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://willie.dfbta.net
"""

import re
from willie import web
from willie.module import commands, example
from willie.tools import eval_equation
from socket import timeout
import string
import HTMLParser


@commands('c', 'calc')
@example('.c 5 + 3', '8')
def c(bot, trigger):
    """Google calculator."""
    if not trigger.group(2):
        return bot.reply("Nothing to calculate.")
    try:
        result = str(eval_equation(trigger.group(2)))
    except ZeroDivisionError:
        result = "Division by zero is not supported in this universe."
    except Exception:
        result = ("Sorry, I can't calculate that with this command. "
                  "I might have another one that can. "
                  "Use .commands for a list.")
    bot.reply(result)


@commands('py')
@example('.py len([1,2,3])', '3')
def py(bot, trigger):
    """Evaluate a Python expression."""
    query = trigger.group(2)
    uri = 'http://tumbolia.appspot.com/py/'
    answer = web.get(uri + web.quote(query))
    if answer:
        bot.say(answer)
    else:
        bot.reply('Sorry, no result.')


@commands('wa', 'wolfram')
@example('.wa sun mass / earth mass',
         '[WOLFRAM] M_(.)\/M_(+)  (solar mass per Earth mass) = 332948.6')
def wa(bot, trigger):
    """Wolfram Alpha calculator"""
    if not trigger.group(2):
        return bot.reply("No search term.")
    query = trigger.group(2)
    uri = 'http://tumbolia.appspot.com/wa/'
    try:
        answer = web.get(uri + web.quote(query.replace('+', '%2B')), 45)
    except timeout as e:
        return bot.say('[WOLFRAM ERROR] Request timed out')
    if answer:
        answer = answer.decode('string_escape')
        answer = HTMLParser.HTMLParser().unescape(answer)
        # This might not work if there are more than one instance of escaped
        # unicode chars But so far I haven't seen any examples of such output
        # examples from Wolfram Alpha
        match = re.search('\\\:([0-9A-Fa-f]{4})', answer)
        if match is not None:
            char_code = match.group(1)
            char = unichr(int(char_code, 16))
            answer = answer.replace('\:' + char_code, char)
        waOutputArray = string.split(answer, ";")
        if(len(waOutputArray) < 2):
            if(answer.strip() == "Couldn't grab results from json stringified precioussss."):
                # Answer isn't given in an IRC-able format, just link to it.
                bot.say('[WOLFRAM]Couldn\'t display answer, try http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
            else:
                bot.say('[WOLFRAM ERROR]' + answer)
        else:

            bot.say('[WOLFRAM] ' + waOutputArray[0] + " = "
                    + waOutputArray[1])
        waOutputArray = []
    else:
        bot.reply('Sorry, no result.')


if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
