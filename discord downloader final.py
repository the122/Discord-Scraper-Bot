import discord
import asyncio
import os
import sys

client = discord.Client()


guild_id = Server ID goes here  #int(input("Server id: "))     #Server ID 
bot_token = "Bot Token Goes Here"                   #Secret token of the bot
chunk_size = 65536                  #Message history will be split into chunks of this size. Make sure chunks are big enough or weird stuff can happen


def save_chunk(text, path, filename):
    try: os.mkdir(path)
    except: pass
    with open(path + filename, "wb") as f:
        f.write(text.encode())
    print("Chunk saved".format(path, filename))
    
async def save_attachment(attachment, path):
    try: os.mkdir(path)
    except: pass
    with open(path + attachment.filename, "wb") as f:
        await attachment.save(f)
    print(attachment.filename + " saved")
    
        

@client.event
async def on_ready():
    print("Download started")
    guild = client.get_guild(guild_id)
    gfolder = guild.name.replace(" ", "_")
    try: os.mkdir(gfolder) 
    except: pass
    for channel in guild.channels:
        if not isinstance(channel, discord.TextChannel):
            continue
        print("Downloading #{0}...".format(channel.name))
        formatted = ""
        try:
            empty = True
            async for message in channel.history(limit=None, oldest_first=True):
                empty = False
                formatted += "{0} {1}: {2}".format(message.created_at.strftime("%Y-%m-%d %H-%M-%S"), str(message.author), message.clean_content)
                if len(message.attachments) > 0:
                    formatted += " | Attachment links: {0}".format(" ".join([a.url for a in message.attachments]))
                    for a in message.attachments:
                        a.filename = str(a.id) + "-" + a.filename
                        await save_attachment(a, "{0}/{1}/".format(gfolder, channel.name))
                formatted += "\n"
                
                if len(formatted) >= chunk_size:
                    save_chunk(formatted, "{0}/{1}".format(gfolder, channel.name), message.created_at.strftime("%Y-%m-%d_%H-%M-%S") + ".txt")
                    formatted = ""
                    
            if not empty:
                save_chunk(formatted, "{0}/{1}/".format(gfolder, channel.name), message.created_at.strftime("%Y-%m-%d_%H-%M-%S") + ".txt")
                print("#{0} was downloaded and saved!".format(channel.name))
            else:
                print("Warning! Channel #{0} cannot be archived (try enabling 'Read Message History' in this channel".format(channel.name))
        except discord.errors.Forbidden:
            print("Warning! Channel #{0} cannot be archived (bot can not read messages in that channel)".format(channel.name))
            
    print("Download complete!")
    await client.close()
print("Starting...") 
client.run("Bot Token Goes Here")
