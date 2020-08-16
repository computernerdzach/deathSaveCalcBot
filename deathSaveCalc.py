import os
import random
import discord
from dotenv import load_dotenv


def compare(hits, misses, save, user):
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
    compare_result = (hit_meter + " Successes\n" + miss_meter + " Failures")
    return f"```{user}'s Save: " + str(save) + "\n" + compare_result + "```"


def death_save(user):
    successes = rolls_dict[f'{user}']['hits']
    fails = rolls_dict[f'{user}']['misses']
    if successes <= 3 or fails <= 3:
        death_roll = random.randint(1, 20)
        if death_roll == 20:
            successes += 2
            rolls_dict[f'{user}']['hits'] = successes
        elif death_roll in range(10, 20):
            successes += 1
            rolls_dict[f'{user}']['hits'] = successes
        elif death_roll == 1:
            fails += 2
            rolls_dict[f'{user}']['misses'] = fails
        elif death_roll in range(2, 10):
            fails += 1
            rolls_dict[f'{user}']['misses'] = fails
        compare(rolls_dict[f'{user}']['hits'], rolls_dict[f'{user}']['misses'], rolls_dict[f'{user}']['save'], user)
        return successes, fails, death_roll


def reset(user):
    rolls_dict.pop(f'{user}', None)
    print(f'counters reset by {user}')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel1ID = int(os.getenv('CHANNEL1'))
channel2ID = int(os.getenv('CHANNEL2'))
client = discord.Client()
rolls_dict = {}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel1 = client.get_channel(channel1ID)
    channel2 = client.get_channel(channel2ID)
    await channel1.send("Let's make some death saves!")
    await channel2.send("Let's make some death saves!")


@client.event
async def on_message(message):
    user = f'{message.author}'
    if message.author == client.user:
        return
    if '!death' in message.content.lower():
        if user not in rolls_dict:
            rolls_dict[user] = {'hits': 0, 'misses': 0, 'save': 0}
            data = death_save(user)
            rolls_dict[user]['hits'] = data[0]
            rolls_dict[user]['misses'] = data[1]
            rolls_dict[user]['save'] = data[2]
            await message.channel.send(compare(rolls_dict[user]['hits'], rolls_dict[user]['misses'],
                                               rolls_dict[user]['save'], user))
            print(compare(rolls_dict[f'{message.author}']['hits'], rolls_dict[f'{message.author}']['misses'],
                          rolls_dict[f'{message.author}']['save'], user))
        else:
            if rolls_dict[user]['hits'] < 3 and rolls_dict[user]['misses'] < 3:
                data = death_save(user)
                rolls_dict[user]['save'] = data[2]
                await message.channel.send(compare(rolls_dict[user]['hits'], rolls_dict[user]['misses'], rolls_dict[user]
                ['save'], user))
                print(compare(rolls_dict[user]['hits'], rolls_dict[user]['misses'], rolls_dict[user]
                ['save'], user))
            else:
                await message.channel.send('reset counter before rolling again')
                print(f"{user} must reset before rolling again")
    elif '!reset' in message.content.lower():
        reset(message.author)
        await message.channel.send(f'counters reset for {message.author}')
    elif '!bye' in message.content.lower() or '!goodbye' in message.content.lower():
        await message.channel.send('Hope you survived! Goodbye!')
        print(f'{message.author} dismissed deathSaveCalcBot')
        await client.close()

client.run(TOKEN)