import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import config

from random import randrange
import time
import math


sticker_list = ['CAACAgIAAxkBAAEbUmZjpuWexamqwlaqBdAyJqLK5BX4vQACQCIAAnq2YEur-eo2cza__iwE',
               'CAACAgIAAxkBAAEbUmhjpuW92pQ6gVtByKXjtClER5k__wACVyIAAiFbuErNTRKGYB-QGCwE',
               'CAACAgIAAxkBAAEbUm9jpuZSTrblvrY-CcJA564aFXi1IAACISIAAv5kOEhTSI6YqQABCUwsBA',
               'CAACAgIAAxkBAAEbUnljpuaNIhrRtJSUq9SIUa-DJwnNRQACNBsAAtsLmUjo-Y2vVy3QaSwE',
               'CAACAgIAAxkBAAEbUn5jpubCcTnW8Zf1THUny9TDigfWjgAC2x0AAlvi8Epokk5or58EiiwE',
               'CAACAgIAAxkBAAEbUoNjpubZxQ8n737g4JWVrgfMBUVlQgAC2BYAAhWhyUslJmJXTr84-SwE',
               'CAACAgIAAxkBAAEbUodjpubseIJtIqYtTVQ0UsNC2Co_EgACcRcAAjM66UusqJoFw8fvdiwE',
               'CAACAgIAAxkBAAEbUo1jpucN1YHniQqzsGFiEyu8-dsXYAACixsAAtJZyEucBTSR34lQXCwE',
               'CAACAgIAAxkBAAEbUo9jpucgUEGmILu-HkHV5r8hDFiYFQACoBYAAhw5yUvDYzB8Lm7wLSwE',
               'CAACAgIAAxkBAAEbUsljpuwMRD__t21Y0u7m-NGaqOShHgACmxcAAmSDQEjU83K8JprsJiwE',
               'CAACAgIAAxkBAAEbUstjpuwxFEef0UJWnGjf1Nd5Wx2QyAAC5h0AApS7QUhvvZGHSYCQ-ywE',
               'CAACAgIAAxkBAAEbUs9jpuw-PpOckFA8Du-tdxUoT7GL1gAC1RsAAo1mQUg65Vd0P3Gm3CwE',
               'CAACAgIAAxkBAAEbUtFjpuxPHYd6sCxiPdAsr-vmYo0SbAACbBgAAv4yQUhP1wMVhoIdmywE',
               'CAACAgIAAxkBAAEbUtVjpuzDlRzNvZbR5H7i6MuBG_Ao9AACChUAAsOu0EsImCPWqF4-niwE',
               'CAACAgIAAxkBAAEbUttjpuzsha25sJknPOpH1RlDB7fQggAC2RgAAoYcaUiWJNePzJU3HiwE',
               'CAACAgIAAxkBAAEbUt1jpuz8capbfFyTkzE5ke0DvLq0NAACPhYAAvWFSUn4mBhkQ2YMfSwE',]

levels = {1: 50,
          2: 100,
          3: 250,
          4: 500,
          5: 800,
          6: 1500}

user_monkey_dict = dict()
user_feed_dict = dict()
user_level_dict = dict()
user_feedtime_dict = dict()

user_coins_dict = dict()

new_level_stickers = ['CAACAgIAAxkBAAEbU6xjpwABpPSUytP8pjiEHX6CxLZeAAEWAAIMGgAC5JvJS8w3gbhF0IONLAQ', # 1->2
                      'CAACAgIAAxkBAAEbU7RjpwAB_CK3vlM71vJKc_a5F2iay3YAApIdAAJx8clLyXZHiQrXgyssBA',  # 2->3
                      'CAACAgIAAxkBAAEbU7ZjpwEL6t9hxPYKyIzmtvu5wxuGTgACrhkAAsddyUvBYQfxDEVYcCwE',    # 3->4
                      'CAACAgIAAxkBAAEbU7ljpwGQaxof_8oV11bex3jGVrAsMAACuxoAAn4V0EvC70mmFZwwLSwE',   # 4->5
                      'CAACAgIAAxkBAAEbU85jpwUg45HcK5WmIu8d2kJMJfSv9gACdB0AAlSeyUtU3EAiry6FmiwE',    # 5->6
                      ]


shop_price_dict = {'Buy Monke Rich': 100,
                   'Buy Monke Woman': 40,
                   'Buy Monke Snowy': 15,
                   'Buy Monke Fat': 5,
                   'Buy Monke WTF': 50,
                   'Buy Monke Romantic': 25
                   }
shop_monke_dict = {'Buy Monke Rich': 'CAACAgIAAxkBAAEbVE5jpxjtm8rY3K2UjNnjbocQRiC0CwACkh0AAnHxyUvJdkeJCteDKywE',
                   'Buy Monke Woman': 'CAACAgIAAxkBAAEbVH5jpyDWhlbwqjSaoG7F4BTWo2eFcwACoBUAAu3XAUh-YJdIqCyaVCwE',
                   'Buy Monke Snowy': 'CAACAgIAAxkBAAEbVFhjpxnMrYpWtjFznC7E0WaqbN5eZQACwyYAAv_7QEjEBfF9uhSiuSwE',
                   'Buy Monke Fat': 'CAACAgIAAxkBAAEbVN5jpzHH_fnl3fvjnkunfWWWu8JZ7wACWR0AAuFZyUsdkhUhT-497ywE',
                   'Buy Monke WTF': 'CAACAgIAAxkBAAEbVOtjpzRVW9ZYZaytGBICg-xNaNOQKgACnhgAAoh5sEktWDqKQKSeTSwE',
                   'Buy Monke Romantic': 'CAACAgIAAxkBAAEbVPFjpzUg_-bxcGrsD4Q1CCu9i9Kk7AAC5xUAAsgiyEv5-1C7vm1_sCwE'}



bot = Bot(token=config.TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['help'])
async def help_command(message):
    await bot.send_message(message.chat.id, 
    "MonkeyBot commands:\n/GetMonkey to get ur monkey\n/ShowMonkey to show everyone ur pretty monkey\n/FeedMonkey to feed ur monkey\n/ShowLevel to see ur monkey's level\n/PlayWithMonkey to play with ur monkey\n/CheckBalance to check ur balance\n/MonkeyShop to enter the MonkeyShop\n/ShopPrices to check current prices in da shop")


@dp.message_handler(commands=['start'])
async def welcome_ahahaha(message):
    # sti = open('AAMCAgADGQEAARtSKmOm3Z-q9PCmogoeOLU4fD6ANhOpAALMBwACRvusBATMghcIOXJCAQAHbQADLAQ', 'rb')
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEbUjpjpt8mal2IF-x3bESOz7Ro-WBfOgAC0RwAAv8TYUs-Sxr816vUjywE')

    await bot.send_message(message.chat.id, '@{}, Вас приветствует FuutexBot'.format(message.from_user.username))

@dp.message_handler(commands=['GetMonkey'])
async def monkey(message):
    user = message.from_user.username

    monkey = randrange(len(sticker_list))
    await bot.send_sticker(message.chat.id, sticker_list[monkey])

    user_monkey_dict[user] = sticker_list[monkey]

    #init
    user_feed_dict[user] = 0
    user_level_dict[user] = 1
    user_feedtime_dict[user] = 0
    user_coins_dict[user] = 0


@dp.message_handler(commands=['FeedMonkey'])
async def feed(message):
    user = message.from_user.username

    if user_monkey_dict.keys().__contains__(user) == False:
        await bot.send_message(message.chat.id, "First u need to get monkey")

    elif time.perf_counter() - user_feedtime_dict[user] < 10:  # 10 sec
        await bot.send_message(message.chat.id, "U can feed ur monkey in {} seconds".format(math.ceil(10 + user_feedtime_dict[user] - time.perf_counter())))

    else:
        bananas = randrange(20, 51)

        user_feed_dict[user] += bananas
        user_feedtime_dict[user] = time.perf_counter()

        await bot.send_message(message.chat.id, "U gave {} bananas to ur monkey".format(bananas))
        await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEbU9Rjpwgvf34Wo8DtVNUBrYPvwh0TKgACLhsAArNeCEuScccFiBHKIiwE')  # chewing monke

        if levels[user_level_dict[user]] <= user_feed_dict[user]:
            user_feed_dict[user] -= levels[user_level_dict[user]]
            user_level_dict[user] += 1

            await bot.send_message(message.chat.id, "Ur monkey is now level {}! Congratulations!!!".format(user_level_dict[user]))
            if user_level_dict[user] == 2 or user_level_dict[user] == 3:
                await bot.send_message(message.chat.id, "Check MonkeyShop for new cool monkeys!!!")
            await bot.send_sticker(message.chat.id, new_level_stickers[user_level_dict[user] - 2])
            return


        # number of bananas left
        if levels[user_level_dict[user]] - user_feed_dict[user] > 1:
            await bot.send_message(message.chat.id, "monke happy, u need {} bananas more to reach level {}".format(levels[user_level_dict[user]] - user_feed_dict[user], user_level_dict[user] + 1))
        else:
            await bot.send_message(message.chat.id, "monke happy, u need {} banana more to reach level {}".format(levels[user_level_dict[user]] - user_feed_dict[user], user_level_dict[user] + 1))


@dp.message_handler(commands=['ShowMonkey'])
async def monkey(message):
    if user_monkey_dict.keys().__contains__(message.from_user.username) == False:
        await bot.send_message(message.chat.id, "First u need to get monkey")
    else:
        await bot.send_sticker(message.chat.id, user_monkey_dict[message.from_user.username])


@dp.message_handler(commands=['ShowLevel'])
async def showlevel(message):
    if user_monkey_dict.keys().__contains__(message.from_user.username) == False:
        await bot.send_message(message.chat.id, "First u need to get monkey")
    else:
        await bot.send_message(message.chat.id, "Ur monkey level is {}".format(user_level_dict[message.from_user.username]))


@dp.message_handler(commands=['PlayWithMonkey'])
async def play(message):
    user = message.from_user.username

    if user_monkey_dict.keys().__contains__(user) == False:
        await bot.send_message(message.chat.id, "First u need to get monkey")
        return

    coins = randrange(5, 11)

    user_coins_dict[user] += coins

    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEbVB9jpxEBszYk4K-oUmWHwlBDPvHVqAACMRoAAo8nuEq_SYP2vo8MjSwE') #friendly monkey
    await bot.send_message(message.chat.id, "U played with ur monkey, and it gives u {} BananaCoins".format(coins))

@dp.message_handler(commands=['CheckBalance'])
async def balance(message):
    user = message.from_user.username

    if user_monkey_dict.keys().__contains__(user) == False:
        await bot.send_message(message.chat.id, 'U have 0 BananaCoins on ur balance')
        return
    
    await bot.send_message(message.chat.id, "U have {} BananaCoins on ur balance".format(user_coins_dict[user]))


@dp.message_handler(commands=['MonkeyShop'])
async def shop(message):
    user = message.from_user.username

    if user_monkey_dict.keys().__contains__(user) == False:
        await bot.send_message(message.chat.id, 'Cannot enter shop without monkey')
        return
    

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("Buy Monke Rich")
    btn1 = types.KeyboardButton("Buy Monke Woman")
    btn2 = types.KeyboardButton("Buy Monke Snowy")
    btn3 = types.KeyboardButton("Buy Monke Fat")

    markup.add(btn1, btn2, btn3)

    cool_monkeys = list()
    if user_level_dict[user] >= 2:
        cool_monkeys.append(KeyboardButton("Buy Monke Rich"))
        cool_monkeys.append(KeyboardButton("Buy Monke Romantic"))
    if user_level_dict[user] >= 3:
        cool_monkeys.append(KeyboardButton("Buy Monke WTF"))
    markup.add(*cool_monkeys)


    await bot.send_message(message.chat.id, "Welcome to Monke Shop!", reply_markup=markup)

@dp.message_handler(commands=['ShopPrices'])
async def shopprices(message):
    for key, price in shop_price_dict.items():
        await bot.send_message(message.chat.id, "{}  --- {} Banana Coins".format(key, price))

@dp.message_handler(content_types=['text'])
async def texter(message):
    user = message.from_user.username

    if user_monkey_dict.keys().__contains__(user) == False:
        await bot.send_message(message.chat.id, 'Cannot enter shop without monkey')
        return

    if shop_price_dict.keys().__contains__(message.text) == False:
        await bot.send_message(message.chat.id, "Undefined command")
        return

    if user_coins_dict[user] >= shop_price_dict[message.text]:
        await bot.send_message(message.chat.id, 'U successfully purchased a new Monkey!')
        user_coins_dict[user] -= shop_price_dict[message.text]
        user_monkey_dict[user] = shop_monke_dict[message.text]
    else:
        await bot.send_message(message.chat.id, 'Not enough BananaCoins to buy this cool monke')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
