# Overview

discordpy-slash is designed to make it easy to implement slash commands into your discord.py Discord bot. You have to do little to no rewriting of your existing commands for this to work. This library may have bugs, and if you find any, please make an issue. 



# How do I install this?

Run this command for Linux and Mac `pip3 install discordpy-slash`, or if you're on Windows, `pip install discordpy-slash`


# How do I implement slash commands into my bot?

All you have to do is use one function, `sync_all_commands`. This will sync all commands to discord and will start listening for interactions and respond to them. It is recommended to put this in an `on_ready` event. Here is an example:



```python
import discord
from discord.ext import commands
from discordpy_slash.slash import *

intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    await sync_all_commands(bot)

@bot.command()
async def say(ctx, message):
    await ctx.send(message)


bot.run()
```

The `sync_all_commands` function takes these parameters:

`client`: Your bot object needed. This can be a `discord.ext.commands.Bot` or `discord.ext.commands.AutoShardedBot` object. `discord.Client` and `discord.AutoShardedClient` have not been tested, but might work. This parameter is required.

`case_sensitive`: Whether uppercase and lowercase letters matter when running a command. Setting this to `False` will make all arguments lowercase. This parameter is optional and defaults to `True`. 


`loading_message`: This message probably won't be seen by the user, but its needed due to how the library works. This can say anything. This parameter is optional and defaults to "Loading".

`send_hidden`: Whether to make messages hidden. Hidden messages can only be seen by the user that runs the command. This parameter is optional and defaults to `False`. 

`hidden_commands`: A list of command names to hide from the slash command list. After all commands are synced, all commands in this list are removed. This parameter is optional and defaults to `[]`

`choices`: A dictionary of choices for the commands given. All keys must be command names, and all values must be a list containing a dictionary with  `name` and `value` keys. An example is: `{"say" : [{"name" : "Greet", "value" : "Hi!"}]}`. This parameter is optional and defaults to `{}`.

`error_function`: A function that will be called if an exception is raised. The function must have two parameters: `context`, and `error`. The `context` will be a `SlashContext` object, and the `error` will be the exception that is raised. This will override the default error system which means exceptions won't be raised unless you manually raise them with `raise error`. This parameter is optional and defaults to `None`. 


# How do I implement buttons into my bot?
With discordpy-slash, implementing buttons into your bot is easy.

#### Displaying buttons

The first thing you have to do is tell the library to give the message buttons. The `SlashContext.send()` function has a `buttons` parameter to do this. When calling the function, you need to give it a list of `Button` objects. Here is an example:


```python
await ctx.send("Hi", buttons=[Button(label="Hey there!"), Button(label="Hi!")])
```
Here are all of the parameters the `Button` object supports:

`click_function`: Function, The function that will be called when the button is clicked. 

`style`: Variable, style of the button. Can be: `BUTTON_PRIMARY`, `BUTTON_SECONDARY`, `BUTTON_SUCCESS`, `BUTTON_DANGER`, and `BUTTON_LINK`

`label`: String, what text on the button will be

`emoji`: String, emoji that will go on the button

`url`: String, URL that the person will be brought to, if the button has the `BUTTON_LINK` style

`disabled`: Boolean, makes button disabled

`parameters`: Dict, used when you want to pass string parameters to the `click_function`


#### Giving buttons functionality

To make a button do something when pressed, there is a parameter `click_function`. Simply give it a function and when the button is pressed, the library will call it. Minimal example:

```python
def test(context, components, parameter_info):
    await ctx.send("Hi!")


@bot.command()
async def ping(ctx):
    await ctx.send("Hi", buttons=[Button(label="Hey there!", click_function=test), Button(label="Hi!")])
```
In the above example, we gave the Button that says "Hey there!" a functionality. When pressed, the `test` function will be called with 3 parameters: 

`context` will be a `SlashContext` object- Used to get info about the context of the button. This includes the `send()`, `edit()`, and `delete()` functions.

`components` a list of `Button` objects- A list of components that the message has. Optionally, you can edit this and return it so that the message will be updated with the new button info.

`parameter_info` will be a `dict` object- The dictionary you passed to the `parameters` button object, if you did 

Example using all three of the given parameters:


```python
def test(context, components, parameter_info):
    await ctx.send("Hi!")
    
    for x in components:
        if x.label == "Hey there!":
            x.disabled = True
    print(parameter_info)
    return components


@bot.command()
async def ping(ctx):
    some_info = {
        "A key" : "A value"
    }
    await ctx.send("Hi", buttons=[Button(label="Hey there!", click_function=test, parameters=some_info), Button(label="Hi!")])

```

In the above example, when the button is pressed, the `test` function is called. The function sends "Hi!", prints the `parameter_info` (which is `{"A key" : "A value"}`, since we passed it into the button object) and then disables the "Hey there!" button. 

# Things to note


1. Make sure you replace all `await ctx.channel.send()` with `await ctx.send()`. This is because the library overrides the `ctx.send()` object so it works with slash commands. It will return a class that has most of the attributes a regular `discord.Message` object has. It also has `await edit()` and `await delete()` methods.


2. Checks like `@has_permissions()` work with this library. 

# Why aren't my slash commands showing up?

Make sure you have reinvited the bot to your server with the `applications.commands` scope and have waited 1 hour for slash commands to get to your server. 


# Why do I get "Invalid Interaction application command" error????
This is because it takes up to 1 hour for slash commands to fan out to all the guilds your bot is in. Just wait! 

# How does it work?

When you call the `sync_all_commands` function, this library iterates through all commands and automatically determines the paramaters every command needs. Then, it adds all commands to Discord. When someone runs a slash command, Discord sends an "INTERACTION_CREATE" event to your bot, which the library will detect and respond to by calling the command function.
