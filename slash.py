import discord
import aiohttp
import inspect
from discord.ext import commands
import asyncio
import json
import typing
import datetime



async def sync_all_commands(client : typing.Union[discord.ext.commands.Bot, discord.ext.commands.AutoShardedBot, discord.Client, discord.AutoShardedClient], case_sensitive=True, loading_message="Loading", send_hidden=False, hidden_commands=[], choices={}, error_function=None):

    commands = []
    for x in client.intents:
        if x[0] == "members":
            if x[1] != True:
                print("You do not have the `Server Members Intent` on. Make sure the switch is on in the Discord Developer Portal and you gave the bot object an intents object with the 'members' attribute set to 'True'. Commands with checks and 'discord.Member' paramaters may fail without this enabled. Please create an issue at https://github.com/TricolorHen061/discordpy-slash/issues if you can't enable this or need help.")

    headers = {"Authorization" : f"Bot {client.http.token}"}

    for x in client.commands:
        description = x.description
        if description == "":
            description = "No description provided"

        options = []
        command_choices = None
        try:
            command_choices = choices[x.name]
        except KeyError:
            command_choices = []
        inspection = inspect.signature(x.callback)
        for k, v in inspection.parameters.items():
            if k == "ctx" or k == "self":
                continue
            required = True
            t = 3
            annotation = v.annotation
            if v.default is not inspect._empty:
                required = False
            if annotation is int:
                t = 4
            if annotation is bool:
                t = 3
            if annotation is discord.member.Member:
                t = 6
            if annotation is discord.TextChannel:
                t = 7
            if annotation is discord.Role:
                t = 8
            options.append({
                "name" : k,
                "description" : k,
                "type" : t,
                "required" : required,
                "choices" : command_choices,
                "kind" : v.kind
            })
        commands.append({
            "name" : x.name,
            "description" : description,
            "options" : options
        })
    
   

    async def get(url, json_dict=None, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=json_dict, headers=headers) as response:
                try:
                    return json.loads(await response.text())
                except json.decoder.JSONDecodeError:
                    return await response.text()

    async def post(url, json_dict=None, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_dict, headers=headers) as response:
                try:
                    return json.loads(await response.text())
                except json.decoder.JSONDecodeError:
                    return await response.text()
    
    async def patch(url, json_dict=None, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=json_dict, headers=headers) as response:
                try:
                    return json.loads(await response.text())
                except json.decoder.JSONDecodeError:
                    return await response.text()
    
    
    async def delete(url, json_dict=None, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=json_dict, headers=headers) as response:
                try:
                    return json.loads(await response.text())
                except json.decoder.JSONDecodeError:
                    return await response.text()

    flags = 64

    if not send_hidden:
        flags = None

    for x in commands:
        w = await post(f"https://discord.com/api/v8/applications/{client.user.id}/commands", json_dict=x, headers=headers)
        try:
            if w["name"] == x["name"]:
                print(f"Synced command {x['name']}")
        except KeyError:
            print(f"Error syncing command {x['name']}: {w}")
        await asyncio.sleep(10) 

    slash_commands = await get(f"https://discord.com/api/v8/applications/{client.user.id}/commands", headers=headers)
    name_list = []
    for x in commands:
        name_list.append(x["name"])
    for x in slash_commands:
        if x["name"] not in name_list or x["name"] in hidden_commands:
            t = await delete(f"https://discord.com/api/v8/applications/{client.user.id}/commands/{x['id']}", headers=headers)
            if t == "":
                print(f"Removed command {x['name']}")

    
    async def on_socket_response(msg):
        if msg["t"] == "INTERACTION_CREATE":  

            args = []
            kwargs = {}      
            

            ack = await post(f"https://discord.com/api/v8/interactions/{msg['d']['id']}/{msg['d']['token']}/callback", headers=headers, json_dict={"type" : 5, "data" : {"content" : loading_message, "flags" : flags}})
            class slash_context:
                def __init__(self, dictionary):
                    self.message = slash_message(dictionary["d"], dictionary["d"]["token"])
                    self.guild = client.get_guild(int(dictionary["d"]["guild_id"]))
                    self.channel = client.get_channel(int(dictionary["d"]["channel_id"]))
                    self.author = client.get_guild(int(dictionary["d"]["guild_id"])).get_member(int(dictionary["d"]["member"]["user"]["id"]))
                    self.bot = client
            class slash_message:
                def __init__(self, discord_dict, token):
                    self.token = token
                    self.id = int(discord_dict["id"])
                    self.channel = client.get_channel(int(discord_dict["channel_id"]))
                    self.author = client.get_channel(int(discord_dict["channel_id"])).guild.get_member(int(discord_dict["member"]["user"]["id"]))
                    try:
                        self.attachments = discord_dict["attachments"]
                    except KeyError:
                        self.attachments = None
                    try:
                        self.embeds = discord_dict["embeds"]
                    except KeyError:
                        self.embeds = None
                    try:
                        self.mentions = discord_dict["mentions"]
                    except KeyError:
                        self.mentions = None
                    try:
                        self.pinned = discord_dict["pinned"]
                    except KeyError:
                        self.pinned = None
                    try:
                        self.mention_everyone = discord_dict["mention_everyone"]
                    except KeyError:
                        self.mention_everyone = None
                    try:
                        self.tts = discord_dict["tts"]
                    except KeyError:
                        self.tts = None
                    self.created_at = datetime.datetime.now()    
                    try:
                        self.edited_timestamp = discord_dict["edited_timestamp"]
                    except KeyError:
                        self.edited_timestamp = None
                    try:
                        self.flags = discord_dict["flags"]
                    except KeyError:
                        self.flags = None
                async def edit(self, content):
                    await patch(f"https://discord.com/api/v8/webhooks/{client.user.id}/{self.token}/messages/@original", headers=headers, json_dict={"content" : content})
            
                async def delete(self):
                    await delete(f"https://discord.com/api/v8/webhooks/{client.user.id}/{self.token}/messages/@original", headers=headers)
    

            for x in client.commands:
                if x.name == msg["d"]["data"]["name"]:
                    for m in commands:
                        if m["name"] == msg["d"]["data"]["name"]:
                            context = slash_context(msg)
                            args.append(context)
                            for w in m["options"]:
                                if w["required"]:
                                    if w["type"] == 3:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                if w["kind"] is inspect._ParameterKind.KEYWORD_ONLY:
                                                    kwargs[n["name"]] = n["value"]
                                                if not w["kind"] is inspect._ParameterKind.KEYWORD_ONLY:
                                                    args.append(n["value"])
                                    
                                    if w["type"] == 4:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                args.append(n["value"])
                                    
                                    if w["type"] == 6:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                args.append(client.get_guild((int(msg["d"]["guild_id"]))).get_member(int(n["value"])))
                                    if w["type"] == 7:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                args.append(client.get_channel(int(n["value"])))
                                    if w["type"] == 8:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                args.append(client.get_guild(int(msg["d"]["guild_id"])).get_role(int(n["value"])))

                                if not w["required"]:
                                    try:
                                        msg["d"]["data"]["options"]
                                    except KeyError:
                                        continue
                                    if w["type"] == 3:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] = n["value"]
                                    if w["type"] == 6:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] = client.get_guild((int(msg["d"]["guild_id"]))).get_member(int(n["value"]))

                                    if w["type"] == 7:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] = client.get_channel(int(n["value"]))
                                    if w["type"] == 8:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] = client.get_guild(int(msg["d"]["guild_id"])).get_role(int(n["value"]))

                    async def send(message : str=None, *, embed : discord.Embed=None):
                        if not isinstance(embed, list):
                            if message == None:
                                if embed == None:
                                    raise ValueError("You must send either an embed or message")
                        if embed:
                            if not isinstance(embed, list):
                                embed = [embed.to_dict()]
                        dictionary = {
                            "content" : message,
                            "embeds" : embed
                        }
                        response = await patch(f"https://discord.com/api/v8/webhooks/{client.user.id}/{msg['d']['token']}/messages/@original", headers=headers, json_dict=dictionary)
                        try:
                            if response["message"] == "You are being rate limited.":
                                await asyncio.sleep(int(response["retry_after"]))
                                await patch(f"https://discord.com/api/v8/webhooks/{client.user.id}/{msg['d']['token']}/messages/@original", headers=headers, json_dict=dictionary)
                        except KeyError:
                            pass
                        return slash_message(msg["d"], msg["d"]["token"])

                    instance = args[0]
                    
                    instance.send = send


                    try:
                        if not case_sensitive:
                            for w in range(len(args)):
                                if not isinstance(args[w], str):
                                    continue
                                args[w] = args[w].lower()
                            for m in kwargs.keys():
                                kwargs[m] = kwargs[m].lower()

                        for m in x.checks:
                            if inspect.iscoroutinefunction(m):
                                await m(slash_context(msg))
                            if not inspect.iscoroutinefunction(m):
                                m(slash_context(msg))


                        await x(*args, **kwargs)

                    except Exception as error:
                        if error_function != None:
                            await error_function(instance, error)
                        if error_function == None:
                            await args[0].send(str(error))

        
    client.add_listener(on_socket_response)