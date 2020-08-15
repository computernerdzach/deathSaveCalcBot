import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel1ID = int(os.getenv('CHANNEL1'))
client = discord.Client()
successes = 0
fails = 0
hit_meter = '[ ][ ][ ]'
miss_meter = '[ ][ ][ ]'


def compare(hits, misses):
    if hits == 0:
        hit_meter = '[ ][ ][ ]'
    if hits == 1:
        hit_meter = '[*][ ][ ]'
    if hits == 2:
        hit_meter = '[*][*][ ]'
    if hits == 3:
        hit_meter = '[*][*][*]'
    if misses == 0:
        miss_meter = '[ ][ ][ ]'
    if misses == 1:
        miss_meter = '[*][ ][ ]'
    if misses == 2:
        miss_meter = '[*][*][ ]'
    if misses == 3:
        miss_meter = '[*][*][*]'
    compare_result = (hit_meter + " Successes\n" + miss_meter + " Failures")
    print(compare_result)
    return compare_result


def death_save(hits, misses):
    death_roll = random.randint(1, 20)
    print(death_roll)
    if death_roll == 20:
        hits += 2
    elif death_roll in range(10,20):
        hits += 1
    elif death_roll == 1:
        misses += 2
    elif death_roll in range(2,10):
        misses += 1
    compare(hits, misses)


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
        death_save(successes, fails)
        hit_meter, miss_meter = compare(successes, fails)
        await message.channel.send()

death_save(successes, fails)

