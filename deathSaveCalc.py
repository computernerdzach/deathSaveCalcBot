import os
import random
import discord
from dotenv import load_dotenv


def assemble_output_message(user_name, user_stats):
    """
    Builds ascii death save visualization
    :param user_name: Name of the current User
    :param user_stats: The User's current death save stats
    :return: String, User's current message output
    """
    hit_meter = '[0]' * user_stats['hits'] + '[ ]' * (3 - user_stats['hits'])
    miss_meter = '[0]' * user_stats['misses'] + '[ ]' * (3 - user_stats['misses'])

    # X's indicate a full meter
    if user_stats['hits'] == 3:
        hit_meter = hit_meter.replace('0', 'X')
    if user_stats['misses'] == 3:
        miss_meter = miss_meter.replace('0', 'X')

    compare_result = f"{hit_meter} Successes\n{miss_meter} Failures"
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
            rolls_dict[user]['hits'] = 3
        elif death_roll in range(10, 20):
            rolls_dict[user]['hits'] += 1
        elif death_roll == 1:
            if rolls_dict[user]['misses'] < 2:
                rolls_dict[user]['misses'] += 2
            elif rolls_dict[user]['misses'] >= 2:
                rolls_dict[user]['misses'] = 3
        elif death_roll in range(2, 10):
            rolls_dict[user]['misses'] += 1
        return death_roll


def reset(user):
    rolls_dict.pop(f'{user}', None)
    print(f'counters reset for {user}')


def add_user(user):
    rolls_dict[user] = {'hits': 0, 'misses': 0, 'save': 0}
    rolls_dict[user]['save'] = death_save(user)
    return assemble_output_message(user_name=user, user_stats=rolls_dict[user])


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
rolls_dict = {}
calculon_quotes = ['He knows that the key to a good scene is a dramatic… PAUSE!', 'Noooooooooooooo!!!!', 'Oh, fate most '
                   'cruel, would that my boundless acting skills would avail mе a sword with which to slay this wretched'
                   ' curse.', "Let's kick him some more.", "No, wait, let me explain", "Dramatic........ pause.", "Hey, "
                   "this one's for the new couple. It's your day. It's all about you. Who's that singing at your "
                   "wedding? It's Calculon, Calculon, Calculon!"]
helpMessage = '''```Welcome to Calculon, the death save calculator!
To get Calculon's attention, use '!Calculon' then enter your command:
    * death - Makes and tracks death saves for each user.
    * reset - Resets your own personal tracker.
    * quote - Generates a random Calculon quote from Futurama.
    * help  - Brings up this message```'''


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    user = str(message.author)
    if message.author == client.user:
        return
    if '!calculon' in message.content.lower():
        if 'death' in message.content.lower():
            if user not in rolls_dict:
                output = add_user(user)
                await message.channel.send(output)
                print(output)
            else:
                if rolls_dict[user]['hits'] < 3 and rolls_dict[user]['misses'] < 3:
                    rolls_dict[user]['save'] = death_save(user)
                    output = assemble_output_message(user_name=user, user_stats=rolls_dict[user])
                    await message.channel.send(output)
                    print(output)
                else:
                    await message.channel.send(f'```{user} must reset counter before rolling again```')
                    print(f"{user} must reset before rolling again")
        if 'reset' in message.content.lower():
            reset(message.author)
            await message.channel.send(f'```counters reset for {message.author}```')
        if 'quote' in message.content.lower():
            await message.channel.send(random.choice(calculon_quotes))
        if 'help' in message.content.lower():
            await message.channel.send(helpMessage)


client.run(TOKEN)
