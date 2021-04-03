import sys
try:
    import discord
except ImportError:
    print("Please install discord.py to continue.")
    sys.exit()
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import subprocess
import os
import random
import platform
import youtube_dl
client = commands.Bot(command_prefix=".")


command_list = []

command_dict = {}

argument_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

arg_number = 0

bot_token = ""



class simple_discord_bot:
    def add_command(self, command_to_add, response, react_to=None, reaction=None, delete=False, connect_to_voicechannel=False, source_to_play=None, DM=False, disconnect_from_voice_channel=False):

        command_dict[str(command_to_add)] = {
            "response": response,
            "react_to": react_to,
            "reaction": reaction,
            "delete": delete,
            "connect_to_voicechannel": connect_to_voicechannel,
            "source_to_play": source_to_play,
            "DM": DM,
            "disconnect_from_voice_channel": disconnect_from_voice_channel
        }

        command_list.append(command_to_add)

    def set_token(self, token):
        global client
        try:
            client.run(token)
        except RuntimeError as bot_killed_error:
            print("Bot killed.")
        except Exception as login_error:
            print(login_error)

    def config(self, show_dms=False, status="online", activity=None, respond_to_other_bots=True, show_server_count=False):

        command_dict["config_options"] = {
            "show_dms": show_dms,
            "status": status,
            "activity": activity,
            "respond_to_other_bots": respond_to_other_bots,
            "show_server_count": show_server_count
        }
        if status == "do not disturb":
            command_dict["config_options"]["status"] = "dnd"


@client.event
async def on_ready():
    server_count = 0
    print(f"Successfully logged in to Discord as user '{client.user}'")
    try:
        if command_dict["config_options"]["activity"] == None:
            await client.change_presence(status=command_dict["config_options"]["status"])
            return

        await client.change_presence(status=command_dict["config_options"]["status"], activity=discord.Game(command_dict["config_options"]["activity"]))
    except KeyError:
        pass
    
    try:
        if command_dict["config_options"]["show_server_count"] == True:
            for x in client.guilds:
                server_count += 1

            print(f"Bot is in {server_count} servers.")
    except KeyError:
        pass

@client.event
async def on_message(message):


    dir_path = None

    song_name_given = False

    on_message.triggering_message = message

    global triggering_message
    triggering_message = message

    try:
        if command_dict["config_options"]["respond_to_other_bots"] != False:
            if message.author.bot == True:
                return
        if message.author == client.user:
            return

        if command_dict["config_options"]["show_dms"] == True:
            if message.guild == None:
                print(f"Recieved DM from {message.author}:  {message.content}")
    except KeyError:
        pass

    for c in command_list:
        if str(message.content).startswith(c):
            #            message_content_list_seperated_by_spaces = f"{message.content}".split(" ")
            #            argument_count = len(message_content_list_seperated_by_spaces)
            #
            #            global arg1
            #            global arg2
            #            global arg3
            #            global arg4
            #            global arg5
            #            global arg6
            #            global arg7
            #            global arg8
            #            global arg9
            #            global arg10
            #
            #            if argument_count == 1:
            #                arg1 = message_content_list_seperated_by_spaces[0]

            #            if argument_count == 2:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #
            #            if argument_count == 3:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]

            #            if argument_count == 4:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #
            #            if argument_count == 5:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #                arg5 = message_content_list_seperated_by_spaces[4]

            #            if argument_count == 6:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #                arg5 = message_content_list_seperated_by_spaces[4]
            #                arg6 = message_content_list_seperated_by_spaces[5]

            #            if argument_count == 7:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #                arg5 = message_content_list_seperated_by_spaces[4]
            #                arg6 = message_content_list_seperated_by_spaces[5]
            #                arg7 = message_content_list_seperated_by_spaces[6]
            #
            #            if argument_count == 8:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #                arg5 = message_content_list_seperated_by_spaces[4]
            #                arg6 = message_content_list_seperated_by_spaces[5]
            #                arg7 = message_content_list_seperated_by_spaces[6]
            #                arg8 = message_content_list_seperated_by_spaces[7]

            #            if argument_count == 9:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #                arg5 = message_content_list_seperated_by_spaces[4]
            #                arg6 = message_content_list_seperated_by_spaces[5]
            #                arg7 = message_content_list_seperated_by_spaces[6]
            #                arg8 = message_content_list_seperated_by_spaces[7]
            #                arg9 = message_content_list_seperated_by_spaces[8]

            #            if argument_count == 10:
            #                arg1 = message_content_list_seperated_by_spaces[0]
            #                arg2 = message_content_list_seperated_by_spaces[1]
            #                arg3 = message_content_list_seperated_by_spaces[2]
            #                arg4 = message_content_list_seperated_by_spaces[3]
            #                arg5 = message_content_list_seperated_by_spaces[4]
            #                arg6 = message_content_list_seperated_by_spaces[5]
            #                arg7 = message_content_list_seperated_by_spaces[6]
            #                arg8 = message_content_list_seperated_by_spaces[7]
            #                arg9 = message_content_list_seperated_by_spaces[8]
            #                arg10 = message_content_list_seperated_by_spaces[9]

            #            command_dict[c]["arguments"] = {
            #            "argument1" : arg1,
            #            "argument2" : arg2,
            #            "argument3" : arg3,
            #            "argument4" : arg4,
            #            "argument5" : arg5,
            #            "argument6" : arg6,
            #            "argument7" : arg7,
            #            "argument8" : arg8,
            #            "argument9" : arg9,
            #            "argument10": arg10
            #            }
            #
            #            arg1 = command_dict[c]["arguments"]["argument1"]
            #            arg2 = command_dict[c]["arguments"]["argument2"]
            #            arg3 = command_dict[c]["arguments"]["argument3"]
            #            arg4 = command_dict[c]["arguments"]["argument4"]
            #            arg5 = command_dict[c]["arguments"]["argument5"]
            #            arg6 = command_dict[c]["arguments"]["argument6"]
            #            arg7 = command_dict[c]["arguments"]["argument7"]
            #            arg8 = command_dict[c]["arguments"]["argument8"]
            #            arg9 = command_dict[c]["arguments"]["argument9"]
            #            arg10 = command_dict[c]["arguments"]["argument10"]

            if len(message.content.split(" ")) > 0:
                n = 0
                for arguments in message.content.split(" "):
                    argument_list.clear()
                    if arguments == c:
                        continue
                    argument_list.append(arguments)

            bot_message = await message.channel.send(command_dict[c]["response"])
            if command_dict[c]["react_to"] != None:
                if command_dict[c]["react_to"] == "command":
                    await message.add_reaction(f"{command_dict[c]['reaction']}")

                if command_dict[c]["react_to"] == "response":
                    await bot_message.add_reaction(f"{command_dict[c]['reaction']}")

                if command_dict[c]["delete"] == True:
                    await message.delete()

            if command_dict[c]["connect_to_voicechannel"] != False:
                
                try:
                    if len(message.content.split(" ")) >= 2:
                        dir_path = os.path.dirname(os.path.realpath(__file__))
                        song_name_given = True
                        song_name = random.randint(1, 1000)
                        if platform.system() == "Windows":
                            command_dict[c]["source_to_play"] = f"{dir_path}\{song_name}.mp3"
                            ytl = youtube_dl.YoutubeDL({"outtmpl" : f"{dir_path}\{song_name}.mp3", "format" : "bestaudio"})
                            ytl.download([f"ytsearch:{message.content.split(' ')[1:]}"])
                        if platform.system() != "Windows":
                            command_dict[c]["source_to_play"] = f"{dir_path}/{song_name}.mp3"
                            if "Usage" not in subprocess.getoutput("youtube-dl"):
                                print("Please install Youtube-dl to continue")
                                return
                            ytl = youtube_dl.YoutubeDL({"outtmpl" : f"{dir_path}/{song_name}.mp3", "format" : "bestaudio"})
                            ytl.download([f"ytsearch:{message.content.split(' ')[1:]}"])

                    channel_to_connnect_to = message.author.voice.channel
                    voice_object = await channel_to_connnect_to.connect()
                    if command_dict[c]["source_to_play"] == None:
                        if song_name_given != True:
                            await message.channel.send("Please give a YouTube link to play, then try again.")
                            return


                    file_to_play = FFmpegPCMAudio(
                        command_dict[c]["source_to_play"])
                    voice_object.play(file_to_play)
                    print(
                        f"Playing audio from file '{command_dict[c]['source_to_play']}' in channel '{channel_to_connnect_to}'")
                    user = message.author
                except Exception as play_error:
                    if "already" in str(play_error):
                        await message.channel.guild.voice_client.disconnect()
                        await message.channel.send("Bot has been disconnected from voice channel. Please try again.")
                        print(
                            "Could not connect to voice channel because bot is already in it. Please disconnect before trying to connect again.")

                    if str(play_error) == "'NoneType' object has no attribute 'channel'":
                        await message.channel.send("Please get in a voice channel, then try again.")
                        print(
                            "Bot could not join voice channel because member is not in one.")

                    else:
                        print(str(play_error))
                    return

            if command_dict[c]["DM"] != False:
                try:
                    await message.author.send(str(command_dict[c]["DM"]))

                except Exception as DM_error:
                    print(str(DM_error))
            if command_dict[c]["disconnect_from_voice_channel"] != False:
                try:
                    await message.guild.voice_client.disconnect()
                except Exception as disconnect_error:
                    print(disconnect_error)


print("Attempting to login to Discord...")

