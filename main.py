import time
from telethon import events
from config import client as client
from config import bot
from FastTelethon import upload_file
import os
import downloader
from petpetgif import petpet

msg = None

genres_template = {
    'Action':'👊 Action',
    'Comedy':'🤣 Comedy',
    'Sport':'🏀 Sport',
    'Sports':'🏀 Sports',
    'Adventure':'👒 Adventure',
    'Drama':'🎭 Drama',
    'Sci-Fi':'🔬 Sci-Fi',
    'Ecchi':'💋 Ecchi',
    'Horror':'🎃 Horror',
    'Romance':'💕 Romance',
    'Fantasy':'🧞 Fantasy',
    'Mystery':'🕵️ Mystery',
    'Slice of Life':'🏫 Slice of Life',
    'Thriller':'🤯 Thriller',
    'Mecha':'🤖 Mecha',
    'Music':'🎵 Music',
    'Psychological':'♟️ Psychological',
    'Mahou Shoujo':'💔 Mahou Shoujo',
    'Supernatural':'🔮 Supernatural'
}

template_main = '''**{title} ({year}) • TVSeries**
__{duration}min__ ⭐️**{score}** [Anilist]({link})

Genres: {genres_str}

@Anime_Gallery

📌 720p {audiostatus}

Link - [{link_title}]({channel_link})
'''

template_desc = '''**{title} ({year}) • TVSeries**
__{duration}min__ ⭐️**{score}** Anilist

Genres: {genres_str}

📌 720p {audiostatus}

Anime: @Anime_Gallery
Group: @Anime_Discussion_Cafe
'''

class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

@client.on(events.NewMessage(outgoing=True, pattern=("\+help")))
async def help_function(event):
    await event.edit("Commands avilabe:-\n\n`+ping` - Just a confirmation that bot is working\n\n`+fwd/media :<username of channel>:<start_id>:<end_id>` - Forward a bunch of files without forwarded from tag\n\n`+edit :<username of group where corrected file is located>:<correct file message_id>` if you messed up sequence in channel (reply this command to the file you want to edit)\n\n`+purge :<start_id>:<end_id>`: Nothing complex here just deletes bunch of messages\n\n\n\n`+rename` :Instructions\nWrite the rename command and in place of number write OwO/UwU..... **Reply to the rename command** with `+rename:Start_id:End_id:ep number of first episode/chapter`\n\n`+sort :start_id:end_id` sorts messages in given range\n\n`+msgid` Gives message id\n\n`+kang <url> | name of file, and reply to pic for thumbnail (url uploader)\n\n`+ anilist <year> <channel link> <Audio shit>`: Reply to Anifluid message and give command as caption of pic\n\n`+description <year> <audio shit>`: reply to anifluid message\n\n\n*Note if channel/group you are working with is private in place of username put invite link starting from `joinchat/.....`")

@client.on(events.NewMessage(outgoing=True, pattern=("\+ping")))
async def hi_function(event):
    await event.edit("pong")

@client.on(events.NewMessage(outgoing=True, pattern=("\+fwd")))
async def fwd_function(event):
    try:
        await event.edit("okay, on it")
        split = event.raw_text.split(":")
        username_of_channel = split[1]
        start_id = int(split[2])
        end_id = int(split[3])+1
        channel = await client.get_entity(f"t.me/{username_of_channel}")
        for i in range(start_id, end_id):
            try:
                message = await client.get_messages(channel, ids=i)
                await client.send_message(event.chat_id, message)
            except:
                pass
            time.sleep(0.25)
    except:
        pass

    x = await client.send_message(event.chat_id, "done")
    time.sleep(1)
    await x.delete()
    await event.delete()

@client.on(events.NewMessage(outgoing=True, pattern=("\+edit")))
async def edit_function(event):
    split = event.raw_text.split(":")
    username = split[1]
    msg_id = int(split[2])
    reply = await event.get_reply_message()
    entity = await client.get_entity(f"t.me/{username}")
    message = await client.get_messages(entity, ids=msg_id)
    await event.edit("Editing the message holup....")
    await client.edit_message(reply, file=message.media, force_document=True)
    await event.delete()

@client.on(events.NewMessage(outgoing=True, pattern=("\+purge")))
async def purge(event):
    split = event.raw_text.split(":")
    start = int(split[1])
    end = int(split[2]) + 1
    for i in range(start, end):
        try:
            message = await client.get_messages(event.chat_id, ids=i)
            await message.delete()
        except:
            pass
        time.sleep(0.25)
    await event.delete()

@client.on(events.NewMessage(outgoing=True, pattern=("\+rename")))
async def rename(event):
    split = event.raw_text.split(":")
    start_id = int(split[1])
    end_id = int(split[2])
    a = int(split[3])
    reply = await event.get_reply_message()
    name = reply.raw_text
    temp = ""
    for i in range(start_id, end_id+1):
        if a<10:
            temp = name.replace("OwO", f"00{a}")
            temp = temp.replace("UwU", f"0{a}")

        elif a<100:
            temp = name.replace("OwO", f"0{a}")
            temp = temp.replace("UwU", f"{a}")

        else:
            temp = name.replace("OwO", f"{a}")
        try:
            message = await client.get_messages(event.chat_id, ids= i)
            await message.reply(temp)
            a = a+1
        except:
            pass
        
        time.sleep(1)

@client.on(events.NewMessage(outgoing=True, pattern=("\+sort")))
async def sort(event):
    split = event.raw_text.split(":")
    files = []
    for i in range(int(split[1]),int(split[2])+1):
        try:
            x = await client.get_messages(event.chat_id, ids=i)
            files.append(f"{x.media.document.attributes[0].file_name}:{x.id}")
        except:
            pass
    files.sort()
    for shit in files:
        split = shit.split(":")
        x = await client.get_messages(event.chat_id, ids=int(split[1]))
        await client.send_message(event.chat_id, x)
        time.sleep(0.25)

@client.on(events.NewMessage(outgoing=True, pattern=("\+msgid")))
async def msg_id(event):
    reply = await event.get_reply_message()
    await event.edit(f"`{reply.id}`") 

@client.on(events.NewMessage(outgoing=True, pattern=("\+kang")))
async def kang(event): 
    try:
        x = await event.get_reply_message()
        thumb = await client.download_media(x.photo)
    except:
        thumb = None

    split = event.raw_text[6:]
    reply = await event.reply("Downloading")
    for_name = split.split("|")
    url = for_name[0]
    url = url.replace(' ','')
    try:
        name = for_name[1]
    except:
        name = url.split("/")[-1]
    await downloader.DownLoadFile(url, 1024*10, reply, file_name=name)
    await Upload(event,reply, name, thumb)
    os.remove(name)
    os.remove(thumb)

async def Upload(event,reply, out, thumbnail):
    timer = Timer()
    async def progress_bar(downloaded_bytes, total_bytes):
        if timer.can_send():
            await reply.edit(f"Uploading... {human_readable_size(downloaded_bytes)}/{human_readable_size(total_bytes)}")

    with open(out, "rb") as f:
        ok = await upload_file(
                client=client,
                file=f,
                name=out,
                progress_callback= progress_bar
            )
    await client.send_message(
        event.chat_id, file=ok, 
        force_document=True, 
        thumb=thumbnail
    )   

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"
    
@client.on(events.NewMessage(outgoing=True, pattern=("\+pet")))
async def pet(event):
    reply = await event.get_reply_message()
    await event.delete()
    pic = await client.download_profile_photo(reply.sender_id)
    petpet.make(pic, "res.gif")
    await reply.reply(file="res.gif")

@client.on(events.NewMessage(outgoing=True, pattern="\+anilist"))
async def anilist(event):
    if event.is_reply:
        data = event.raw_text.split(" ", 3)
        channel_link = data[2]
        ani = await event.get_reply_message()
        link = ani.reply_markup.rows[0].buttons[0].url
        ks = ani.text.split("**")
        title = ks[1]
        duration = ks[10].replace(":","")
        duration = duration.replace("`","")
        duration = duration.replace(" Per Ep.", "")
        duration = duration.replace("\n", "")
        try:
            score = ks[12].replace(":","")
            score.replace("`","")
            score = int(score)/10
        except:
            score = 8.0
        genres = ks[14].replace(":","")
        genres = genres.replace("`","")
        genres = genres.replace("\n","")
        list_g = genres.split(", ")
        genre_str = ""
        for g in list_g:
            t = genres_template[g.strip()]
            genre_str = f"{genre_str} {t}"
        await event.edit(template_main.format(title=title, duration=duration, score=score, link=link,genres_str=genre_str, link_title=title, channel_link=channel_link, year=data[1], audiostatus=data[-1]))


@client.on(events.NewMessage(outgoing=True, pattern="\+description"))
async def anilist(event):
    if event.is_reply:
        ani = await event.get_reply_message()
        data = event.raw_text.split(" ", 2)
        ks = ani.text.split("**")
        title = ks[1]
        duration = ks[10].replace(":","")
        duration = duration.replace("`","")
        duration = duration.replace(" Per Ep.", "")
        duration = duration.replace("\n", "")
        try:
            score = ks[12].replace(":","")
            score.replace("`","")
            score = int(score)/10
        except:
            score = 8.0
        genres = ks[14].replace(":","")
        genres = genres.replace("`","")
        genres = genres.replace("\n","")
        list_g = genres.split(", ")
        genre_str = ""
        for g in list_g:
            t = genres_template[g.strip()]
            genre_str = f"{genre_str} {t}"
        await event.edit(template_desc.format(title=title, duration=duration, score=score,genres_str=genre_str, year=data[1], audiostatus=data[-1]))

@client.on(events.NewMessage(outgoing=True, pattern=("\+media")))
async def fwd_function(event):
    try:
        await event.edit("okay, on it")
        split = event.raw_text.split(":")
        username_of_channel = split[1]
        start_id = int(split[2])
        end_id = int(split[3])+1
        channel = await client.get_entity(f"t.me/{username_of_channel}")
        for i in range(start_id, end_id):
            try:
                message = await client.get_messages(channel, ids=i)
                if message.media != None:
                    await client.send_message(event.chat_id, message)
            except:
                pass
            time.sleep(0.25)
    except:
        pass

    x = await client.send_message(event.chat_id, "done")
    time.sleep(1)
    await x.delete()
    await event.delete()

@client.on(events.NewMessage(outgoing=True, pattern=("\+copy")))
async def copy_message(event):
    try:
        global msg
        await event.edit("okay, on it")
        msg = await event.get_reply_message()
        await event.edit("Done.")
    except Exception as e:
        await event.edit(str(e))

@client.on(events.NewMessage(outgoing=True, pattern=("\+show")))
async def preveiw(event):
    try:
        global msg
        await event.edit("okay, on it")
        if msg is not None:
            media = await client.download_media(msg.media)
            await bot.send_message(event.chat_id,message=msg.text,buttons=msg.buttons,file=media)
            await event.delete()
            os.remove(media)
        else:
            await event.edit("No message copied")
    except Exception as e:
        await event.edit(str(e))

@client.on(events.NewMessage(outgoing=True, pattern=("\+post")))
async def post(event):
    try:
        global msg
        await event.edit("okay, on it")
        if msg is not None:
            reply = await event.get_reply_message()
            if reply is None:
                await event.edit("reply to a message")
                return
            ids = reply.text.replace("@","t.me/")
            ids = ids.split("\n")
            media = await client.download_media(msg.media)
            ads = []
            for i in ids:
                ent = await bot.get_entity(i)
                a = await bot.send_message(ent,message=msg.text,buttons=msg.buttons,file=media)
                ads.append(i + "/" + str(a.id))
            await event.edit("\n".join(ads))
            os.remove(media)
        else:
            await event.edit("No message copied")
    except Exception as e:
        await event.edit(str(e))


@client.on(events.NewMessage(outgoing=True, pattern=("\+del")))
async def delete(event):
    try:
        await event.edit("okay, on it")
        x = await event.get_reply_message()
        if x is None:
            event.edit("reply to message")
            return
        id_list = []
        txt = x.text.split('\n')
        for i in txt:
            a = i.split("/")
            username = a[-2]
            msgid = a[-1]
            print(username)
            await bot.delete_messages("t.me/"+username, msgid)

        await event.edit("Done.")
    except Exception as e:
        await event.edit(str(e))

@client.on(events.NewMessage(outgoing=True, pattern=("\+parse")))
async def parse(event):
    try:
        await event.edit("okay, on it")
        x = await event.get_reply_message()
        if x is None:
            event.edit("reply to message")
            return
        msg = []
        x = x.text.split("\n")
        for i in x:
            a = i.split()
            msg.append(a[0])

        await event.edit("\n".join(msg))
    except Exception as e:
        await event.edit(str(e))


client.start()

client.run_until_disconnected()
