import os
import random
import discord
from dotenv import load_dotenv


def compare(hits, misses):
    if hits == 0:
        hit_meter = '[ ][ ][ ]'
    if hits == 1:
        hit_meter = '[0][ ][ ]'
    if hits == 2:
        hit_meter = '[0][0][ ]'
    if hits == 3:
        hit_meter = '[0][0][0]'
    if misses == 0:
        miss_meter = '[ ][ ][ ]'
    if misses == 1:
        miss_meter = '[0][ ][ ]'
    if misses == 2:
        miss_meter = '[0][0][ ]'
    if misses == 3:
        miss_meter = '[0][0][0]'
    compare_result = (hit_meter + " Successes\n" + miss_meter + " Failures")
    print(compare_result)
    return compare_result


successes = 0
fails = 0


def death_save():
    global successes
    global fails
    while successes < 3 or fails < 3:
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
        return str(str(death_roll) + "\n" + compare(successes, fails))


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
        await message.channel.send(death_save())


client.run(TOKEN)
