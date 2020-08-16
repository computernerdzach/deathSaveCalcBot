import os
import random
import discord
from dotenv import load_dotenv


def compare(user_name, user_stats):
    """
    Builds ascii death save visualization
    :param user_name: Name of the current User
    :param user_stats: The User's current death save stats
    :return: String, User's current message output
    """
    hit_meter = '[0]' * user_stats['hits'] + '[ ]' * (3 - user_stats['hits'])
    miss_meter = '[0]' * user_stats['misses'] + '[ ]' * (3 - user_stats['misses'])
    compare_result = (hit_meter + " Successes\n" + miss_meter + " Failures")
    return f"```{user_name}'s Save: {user_stats['save']}\n{compare_result}```"


def death_save(user):
    """
    Updates the global rolls_dict with Death Save roll results
    :param user: String, representing the user key to reference in the global rolls_dict
    :return: the d20 roll result
    """
    if rolls_dict[user]['hits'] <= 3 or rolls_dict[user]['misses'] <= 3:
        death_roll = random.randint(1, 20)
        if death_roll == 20:
            rolls_dict[user]['hits'] += 2
        elif death_roll in range(10, 20):
            rolls_dict[user]['hits'] += 1
        elif death_roll == 1:
            rolls_dict[user]['misses'] += 2
        elif death_roll in range(2, 10):
            rolls_dict[user]['misses'] += 1

        return death_roll


def reset(user):
    rolls_dict.pop(f'{user}', None)
    print(f'counters reset for {user}')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
channel1ID = int(os.getenv('CHANNEL1'))
channel2ID = int(os.getenv('CHANNEL2'))
client = discord.Client()
rolls_dict = {}


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # TODO: Instead of expecting a static set of Channels,
    #       try dynamically getting the list of installed Channels
    #       using the Client Guilds attribute:
    #       https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.guilds
    channel1 = client.get_channel(channel1ID)
    channel2 = client.get_channel(channel2ID)
    # TODO: Then, this becomes: for channel in channels: channel.send('blah')
    await channel1.send("Let's make some death saves!")
    await channel2.send("Let's make some death saves!")


@client.event
async def on_message(message):
    user = str(message.author)
    if message.author == client.user:
        return
    if '!death' in message.content.lower():
        if user not in rolls_dict:
            rolls_dict[user] = {'hits': 0, 'misses': 0, 'save': 0}
            rolls_dict[user]['save'] = death_save(user)
            output = compare(user_name=user, user_stats=rolls_dict[user])
            await message.channel.send(output)
            print(output)
        else:
            if rolls_dict[user]['hits'] < 3 and rolls_dict[user]['misses'] < 3:
                rolls_dict[user]['save'] = death_save(user)
                output = compare(user_name=user, user_stats=rolls_dict[user])
                await message.channel.send(output)
                print(output)
            else:
                await message.channel.send(f'```{user} must reset counter before rolling again```')
                print(f"{user} must reset before rolling again")
    elif '!reset' in message.content.lower():
        reset(message.author)
        await message.channel.send(f'```counters reset for {message.author}```')
    elif '!bye' in message.content.lower() or '!goodbye' in message.content.lower():
        await message.channel.send('```Hope you survived! Goodbye!```')
        print(f'{message.author} dismissed deathSaveCalcBot')
        await client.close()


client.run(TOKEN)
