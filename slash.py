import discord
import aiohttp
import inspect
from discord.ext import commands
import asyncio
import json
import typing



async def sync_all_commands(client : typing.Union[discord.ext.commands.Bot, discord.ext.commands.AutoShardedBot, discord.Client, discord.AutoShardedClient], case_sensitive=False, loading_message="Loading", send_hidden=True):
    commands = []

    headers = {"Authorization" : f"Bot {client.http.token}"}

    for x in client.commands:
        description = x.description
        if description == "":
            description = "No description provided"

        options = []
        inspection = inspect.signature(x.callback)
        for k, v in inspection.parameters.items():
            if k == "ctx":
                continue
            required = False
            t = 3
            annotation = v.annotation
            if not isinstance(v.default, inspect._empty):
                required = True
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
                "choices" : [],
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

    
    
    async def on_socket_response(msg):
        if msg["t"] == "INTERACTION_CREATE":        
            
            print("Received interaction")
            async def wait(): 
                def check(m):
                    return m.author.id == int(msg["d"]["member"]["user"]["id"]) and m.channel.id == int(msg["d"]["channel_id"])
                return await client.wait_for("message", check=check, timeout=4.0)
                 

            task = asyncio.create_task(wait())

            await post(f"https://discord.com/api/v8/interactions/{msg['d']['id']}/{msg['d']['token']}/callback", headers=headers, json_dict={"type" : 5, "data" : {"content" : loading_message, "flags" : flags}})
            
            
            for x in client.commands:
                if x.name == msg["d"]["data"]["name"]:
                    args = []
                    kwargs = {}
                    for m in commands:
                        for n in range(10):
                            try:
                                message = task.result()
                            except:
                                await asyncio.sleep(0.1)
                        if m["name"] == msg["d"]["data"]["name"]:
                            context = await client.get_context(message)
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
                                    if w["type"] == 3:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] == n["value"]
                                    if w["type"] == 6:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] == client.get_guild((int(msg["d"]["guild_id"]))).get_member(int(n["value"]))

                                    if w["type"] == 7:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] = client.get_channel(int(n["value"]))
                                    if w["type"] == 8:
                                        for n in msg["d"]["data"]["options"]:
                                            if n["name"] == w["name"]:
                                                kwargs[n["name"]] = client.get_guild(int(msg["d"]["guild_id"])).get_role(int(n["value"]))
                    
                    
                    
                    class slash_message:
                        def __init__(self, discord_dict, token):
                            self.token = token
                            self.id = int(discord_dict["id"])
                            self.content = discord_dict["content"]
                            self.channel = client.get_channel(int(discord_dict["channel_id"]))
                            self.author = client.get_channel(int(discord_dict["channel_id"])).guild.get_member(int(discord_dict["author"]["id"]))
                            self.attachments = discord_dict["attachments"]
                            self.embeds = discord_dict["embeds"]
                            self.mentions = discord_dict["mentions"]
                            self.pinned = discord_dict["pinned"]
                            self.mention_everyone = discord_dict["mention_everyone"]
                            self.tts = discord_dict["tts"]
                            self.timestamp = discord_dict["timestamp"]
                            self.edited_timestamp = discord_dict["edited_timestamp"]
                            self.flags = discord_dict["flags"]
                        async def edit(self, content):
                            await patch(f"https://discord.com/api/v8/webhooks/{client.user.id}/{self.token}/messages/@original", headers=headers, json_dict={"content" : content})
                    
                        async def delete(self):
                            await delete(f"https://discord.com/api/v8/webhooks/{client.user.id}/{self.token}/messages/@original", headers=headers)
                    
                    try:
                        await x.can_run(context)
                        if not case_sensitive:
                            for w in range(len(args)):
                                if not isinstance(args[w], str):
                                    continue
                                print(args[w])
                                args[w] = args[w].lower()
                            for m in kwargs.keys():
                                kwargs[m] = kwargs[m].lower()
                            async def send(message : str=None, *, embed : discord.Embed=None, allowed_mentions=None, delete_after=None):
                                if not isinstance(embed, list):
                                    if not message:
                                        if not embed:
                                            raise ValueError("You must send either an embed or message")
                                if embed:
                                    embed = embed.to_dict()
                                dictionary = {
                                    "content" : message,
                                    "embeds" : [embed],
                                    "allowed_mentions" : allowed_mentions
                                }
                                t = await patch(f"https://discord.com/api/v8/webhooks/{client.user.id}/{msg['d']['token']}/messages/@original", headers=headers, json_dict=dictionary)
                                print(t)
                                return slash_message(t, msg["d"]["token"])
                        args[0].send = send
                        print(args)
                        print(kwargs)
                        await x(*args, **kwargs)

                    except Exception as error:
                        await context.channel.send(str(error))


    client.add_listener(on_socket_response)