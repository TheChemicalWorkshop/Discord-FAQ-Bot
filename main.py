from discord.ext.commands import Bot
from discord_components import (Button, ButtonStyle, DiscordComponents,
                                InteractionType)

import random
import json

def write_json(data, filename="faq.json"): 
	with open(filename,'w') as f: 
		json.dump(data, f, indent=4) 


bot = Bot(command_prefix = "!")


colors_dict = \
    {
        "red":"red",
        "green":"green",
        "blue":"blue",
        "grey":"grey",
        "gray":"grey",
        "r":"red",
        "g":"green",
        "b":"blue"
    }

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")



# ! Addfaq <color> <name> (generates id, adds it to db)
@bot.command()
async def addfaq(ctx, color_in, *content):
    color = colors_dict.get(color_in)
    if color is None:   
        return
    if len(" ".join(content)) > 80:
        await ctx.send(f"too long, must be 80 chars or lower {len(' '.join(content))}")

    # * assign ID
    rdint = random.randint(0, 99999)

    with open("faq.json") as json_file: 
        data = json.load(json_file) 
        

        data.update({rdint:"empty"})

        write_json(data) 


# ! restorefaq <color> <id> <name>
@bot.command()
async def restorefaq(ctx, color_in, id, *content):
    color = colors_dict.get(color_in)
    if color is None:   
        return
    if len(" ".join(content)) > 80:
        await ctx.send(f"too long, must be 80 chars or lower {len(' '.join(content))}")

    await ctx.send(
        "​", # zero width
        components=[
        Button(style=eval(f"ButtonStyle." + color), label=" ".join(content), id=id),
        ],
    )
    await ctx.message.delete()



@bot.event
async def on_button_click(interaction):
    # await interaction.channel.send("dsa")
    if interaction.responded:
        return
    with open("faq.json") as json_file: 
        data = json.load(json_file)
        resp = data.get(interaction.component.id)
    await interaction.respond(content = resp, type=4)

# ! Listfaq (lists with id)
@bot.command()
async def listfaq(ctx):
    with open("faq.json") as json_file: 
        data = json.load(json_file)
    await ctx.send(str(data).replace("', '", "'\n'"))

# ! changefaq <id> (new output)
@bot.command()
async def changefaq(ctx, id, *output):
    with open("faq.json") as json_file: 
        data = json.load(json_file) 
        

        data.update({int(id):" ".join(output)})

        write_json(data)

        await ctx.send("done")

bot.run("NzA2NzIyMjE0MzMzOTA2OTk1.XsaN_g.hWQTdwP5FF-Fg97-6fmzrTjIa5A")
