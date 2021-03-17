# Overview

discordpy-slash is designed to make it easy to implement slash commands into your discord.py Discord bot. You have to do little to no rewriting of your existing commands for this to work. This library may have bugs, and if you find any, please make an issue. 



# How do I install this?

Run this command for Linux and Mac `pip3 install discordpy-slash`, or if you're on Windows, `pip install discordpy`


# How do I implement it into my bot?

All you have to do is use one function, sync_all_commands`. This will sync all commands to discord and will start listening for interactions and respond to them. It is recommended to put this in an `on_ready` event. Here is an example:



```python
import discord
from discord.ext import commands
from discordpy_slash import slash

intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help")


@bot.event
async def on_ready():
    await slash.sync_all_commands(bot)

@bot.command()
async def say(ctx, message):
    await ctx.send(message)


bot.run()
```
The `sync_all_commands` function takes these parameters:

`client`: Your bot object needed. This can be a `discord.ext.commands.Bot` or `discord.ext.commands.AutoShardedBot` object. `discord.Client` and `discord.AutoShardedClient` have not been tested, but might work. This parameter is required.

`case_sensitive`: Whether uppercase and lowercase letters matter when running a command. Setting this to 
`False` will make all arguments lowercase. This parameter is optional and defaults to `True`. 


`loading_message`: This message is what the user will see until the custom `await ctx.send()` method this library uses is called. The user usually only sees this for up to a second. This parameter is optional and defaults to "Loading".

`send_hidden`: Whether to make messages hidden. Hidden messages can only be seen by the user that runs the command. This parameter is optional and defaults to `True`. 

# Things to note


1. Notice that you need the `Server Members Intent`. This is because this library uses the `discord.Guild.get_member()` function for parameters that have the `discord.Member` annotation. If you don't have these intents enabled, the library will still work, but parameters with `discord.Member` will return `None`.


2. Embeds are not supported.


3. Make sure you replace all `await ctx.channel.send()` with `await ctx.send()`. This is because the library overrides the `ctx.send()` object so it works with slash commands. It will return a class that has most of the attributes a regular `discord.Message` object has. It also has `await edit()` and `await delete()` methods.


4. The library will not start listening for commands until it finishes syncing commands.

5. Checks like `@has_permission()` work with this library. 

# Why aren't my slash commands showing up?

Make sure you have reinvited the bot to your server with the `applications.commands` scope and have waited 1 hour for slash commands to get to your server. 

# How does it work?

When you call the `sync_all_commands` function, this library iterates through all commands and automatically determines the paramaters every command needs. Then, it adds all commands to Discord. When someone runs a slash command, Discord sends an "INTERACTION_CREATE" event to your bot, which the library will detect and respond to by calling the command function.