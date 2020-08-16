import os
import random
import discord
from dotenv import load_dotenv


def compare(hits, misses):
    if hits == 0:
        hit_meter = '[ ][ ][ ]'
    elif hits == 1:
        hit_meter = '[0][ ][ ]'
    elif hits == 2:
        hit_meter = '[0][0][ ]'
    elif hits >= 3:
        hit_meter = '[X][X][X]'
    if misses == 0:
        miss_meter = '[ ][ ][ ]'
    elif misses == 1:
        miss_meter = '[0][ ][ ]'
    elif misses == 2:
        miss_meter = '[0][0][ ]'
    elif misses >= 3:
        miss_meter = '[X][X][X]'

    compare_result = ("```" + hit_meter + " Successes\n" + miss_meter + " Failures```")
    print(compare_result)
    return compare_result


successes = 0
fails = 0


def death_save():
    global successes
    global fails
    while successes <= 3 or fails <= 3:
        death_roll = random.randint(1, 20)
        print(death_roll)
        if death_roll == 20:
            successes += 2
        elif death_roll in range(10, 20):
            successes += 1
        elif death_roll == 1:
            fails += 2
        elif death_roll in range(2, 10):
            fails += 1
        return str("```" + str(death_roll) + "```" + "\n" + compare(successes, fails))
    while successes >= 4 or fails >= 4:
        return "too many saves"


def reset():
    global successes
    global fails
    successes = 0
    fails = 0
    print('counters reset')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel1ID = int(os.getenv('CHANNEL1'))
client = discord.Client()
hits = 0
misses = 0
hit_meter = '[ ][ ][ ]'
miss_meter = '[ ][ ][ ]'


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel1 = client.get_channel(channel1ID)
    await channel1.send("Let's make some death saves!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '!death' in message.content.lower():
        if successes > 2 or fails > 2:
            await message.channel.send('reset counter before rolling again')
        else:
            await message.channel.send(death_save())
    elif '!reset' in message.content.lower():
        reset()
        await message.channel.send('counters reset')
    elif '!bye' in message.content.lower() or '!goodbye' in message.content.lower():
        await message.channel.send('Hope you survived! Goodbye!')
        print(f'{message.author} dismissed deathSaveCalcBot')
        await client.close()

client.run(TOKEN)
