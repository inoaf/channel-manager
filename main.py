import time
from telethon import events, Button
from config import client, bot, main_bot_id, approved_users
import os
from petpetgif import petpet

msg = None
link_preview = False 

help_text = """
Commands avilabe:-

`+ping` - Just a confirmation that bot is working

`+fwd :<username of channel>:<start_id>:<end_id>` - Forward a bunch of files without forwarded from tag

`+edit :<username of group where corrected file is located>:<correct file message_id>` if you messed up sequence in channel (reply this command to the file you want to edit)

`+purge :<start_id>:<end_id>`: Nothing complex here just deletes bunch of messages

`+sort :start_id:end_id` sorts messages in given range

`+msgid` Gives message id

*Note if channel/group you are working with is private in place of username put invite link starting from `joinchat/.....`
"""

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+help")))
async def help_function(event):
    await event.reply(help_text)

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+ping")))
async def hi_function(event):
    await event.reply("pong")

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+fwd")))
async def fwd_function(event):
    try:
        await event.reply("okay, on it")
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

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+edit")))
async def edit_function(event):
    split = event.raw_text.split(":")
    username = split[1]
    msg_id = int(split[2])
    reply = await event.get_reply_message()
    entity = await client.get_entity(f"t.me/{username}")
    message = await client.get_messages(entity, ids=msg_id)
    await event.reply("Editing the message holup....")
    await client.edit_message(reply, file=message.media, force_document=True)
    await event.delete()

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+purge")))
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

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+sort")))
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

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+msgid")))
async def msg_id(event):
    reply = await event.get_reply_message()
    await event.reply(f"`{reply.id}`") 
    
@client.on(events.NewMessage(from_users=approved_users, pattern=("\+pet")))
async def pet(event):
    reply = await event.get_reply_message()
    await event.delete()
    pic = await client.download_profile_photo(reply.sender_id)
    petpet.make(pic, "res.gif")
    await reply.reply(file="res.gif")

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+copy")))
async def copy_message(event):
    try:
        global msg
        await event.reply("okay, on it")
        msg = await event.get_reply_message()
        await event.reply("Done.")
    except Exception as e:
        await event.reply(str(e))

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+linkp")))
async def _(event):
    global link_preview
    link_preview = False if link_preview == True else True
    await event.reply(f"Link preview set to: {link_preview}")

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+show")))
async def preveiw(event):
    try:
        global msg
        await event.reply("okay, on it")
        if msg is not None:
            media = await client.download_media(msg.media)
            await bot.send_message(event.chat_id,message=msg.text,buttons=msg.buttons,file=media,link_preview=link_preview)
            await event.delete()
            os.remove(media)
        else:
            await event.reply("No message copied")
    except Exception as e:
        await event.reply(str(e))

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+post")))
async def post(event):
    try:
        global msg
        await event.reply("okay, on it")
        if msg is not None:
            reply = await event.get_reply_message()
            if reply is None:
                await event.reply("reply to a message")
                return
            ids = reply.text.replace("@","t.me/")
            ids = ids.split("\n")
            media = await client.download_media(msg.media)
            ads = []
            for i in ids:
                ent = await bot.get_entity(i)
                a = await bot.send_message(ent,message=msg.text,buttons=msg.buttons,file=media,link_preview=link_preview)
                ads.append(i + "/" + str(a.id))
            await event.reply("\n".join(ads))
            try:
                os.remove(media)
            except:
                pass
        else:
            await event.reply("No message copied")
    except Exception as e:
        await event.reply(str(e))

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+del")))
async def delete(event):
    try:
        await event.reply("okay, on it")
        x = await event.get_reply_message()
        if x is None:
            event.reply("reply to message")
            return
        txt = x.text.split('\n')
        for i in txt:
            a = i.split("/")
            username = a[-2]
            msgid = a[-1]
            print(username)
            await bot.delete_messages("t.me/"+username, msgid)

        await event.reply("Done.")
    except Exception as e:
        await event.reply(str(e))

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+parse")))
async def parse(event):
    try:
        await event.reply("okay, on it")
        x = await event.get_reply_message()
        if x is None:
            event.reply("reply to message")
            return
        msg = []
        x = x.text.split("\n")
        for i in x:
            a = i.split()
            msg.append(a[0])

        await event.reply("\n".join(msg))
    except Exception as e:
        await event.reply(str(e))

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+promote")))
async def _(event):
    data = event.raw_text.split(" ")
    user = event.sender_id
    me = await bot.get_entity(main_bot_id)
    chat = await bot.get_entity(data[1])
    perms = await bot.get_permissions(chat, me)
    await bot.edit_admin(chat, user, change_info=perms.change_info, post_messages= perms.post_messages, edit_messages=perms.edit_messages, delete_messages=perms.delete_messages, invite_users=perms.invite_users, add_admins=perms.add_admins, manage_call=perms.manage_call)
    await event.reply(f"Promoted in {data[1]}")

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+oldmkpost")))
async def _(event):
    msg = await event.get_reply_message()
    try:
        media = await client.download_media(msg.media)
    except:
        media = None
    data = event.raw_text.split("\n")[1:]
    l1, l2, l3 = data
    await bot.send_message(
        event.chat_id,
        msg.raw_text,
        file=media,
        buttons=[Button.url("360p", l1), Button.url("720p", l2), Button.url("1080p", l3)]
    )

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+mkpost")))
async def _(event):
    msg = await event.get_reply_message()
    if msg == None:
        await event.reply("+mkpost <bot_username> <database_id>")
        return

    try:
        media = await client.download_media(msg.media)
    except:
        media = None

    bot_username = event.raw_text.split(" ")[1].replace("@", "")
    channel_id = event.raw_text.split(" ")[2]
    if not channel_id.startswith("-100"):
        channel_id = f"-100{channel_id}"
    channel_id = int(channel_id)

    id = msg.id
    l1 = await client.get_messages(event.chat_id, ids=id+1)
    l2 = await client.get_messages(event.chat_id, ids=id+2)
    l3 = await client.get_messages(event.chat_id, ids=id+3)

    m1 = await client.send_message(channel_id, l1)
    m2 = await client.send_message(channel_id, l2)
    m3 = await client.send_message(channel_id, l3)


    await bot.send_message(
        event.chat_id,
        msg.raw_text,
        file=media,
        buttons=[
            Button.url("360p", f"t.me/{bot_username}?start=single_{channel_id}_{m3.id}"),
            Button.url("720p", f"t.me/{bot_username}?start=single_{channel_id}_{m2.id}"), 
            Button.url("1080p", f"t.me/{bot_username}?start=single_{channel_id}_{m1.id}") 
        ]
    )
    
@client.on(events.NewMessage(from_users=approved_users, pattern=("\+bulkmkpost")))
async def _(event):
    msg = await event.get_reply_message()
    if msg == None:
        await event.reply("bot_username|xyz\n\ndatabase_id|xyz\n\nstart|xyz\n\nend|xyz\n\ntarget|xyz\n\nstartep|xyz\n\nname|xyz\n\nbuttonrows,cols|x,y\n\nbuttontxt|x1,y1,z1,x2,y2,z2")
        await event.reply("Mention button rows and colunms, button text needs to be given row wise, with comma seperation")
        return
    try:
        media = await client.download_media(msg.media)
    except:
        media = None

    data = msg.raw_text.split("\n\n")
    fch = dict()

    for i in data:
        d1 = i.split("|")
        fch[d1[0]] = d1[1]

    database_id = fch['database_id']
    if not database_id.startswith("-100"):
        database_id = f"-100{database_id}"
    database_id = int(database_id)
    bot_username = fch['bot_username'].replace("@", "")
    target = fch['target']
    if not target.startswith("-100"):
        target = f"-100{target}"
    target = int(target)

    rows, cols = list(map(int, fch["buttonrows,cols"].split(",")))
    buttoncount = rows * cols
    buttontxt = list(map(lambda x: x.strip(), fch["buttontxt"].split(",")))


    a = int(fch["startep"])
    txt = ""
    for i in range(int(fch["start"].split("/")[-1]),int(fch["end"].split("/")[-1])+1, buttoncount):
        links = []
        for j in range(buttoncount):
            li = await client.get_messages(event.chat_id, ids=i+j)
            mi = await client.send_message(database_id, li)
            links.append(f"t.me/{bot_username}?start=single_{database_id}_{mi.id}")
        
        name = fch["name"]
        if a<10:
            temp = name.replace("OwO", f"00{a}")
            temp = temp.replace("UwU", f"0{a}")

        elif a<100:
            temp = name.replace("OwO", f"0{a}")
            temp = temp.replace("UwU", f"{a}")

        else:
            temp = name.replace("OwO", f"{a}")

        buttons = []
        count = cols
        for j in range(buttoncount):
            if count == cols:
                buttons.append([])
                count = 0 
            buttons[-1].append(Button.url(buttontxt[j], links[j]))
            count += 1

        final = await bot.send_message(
            target,
            temp,
            file=media,
            buttons=buttons
        )
        a += 1
        txt += f"t.me/c/{str(target).replace('-100', '')}/{final.id}"
        txt += "\n"
    await event.reply(txt)

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+subdubbulkpost")))
async def _(event):
    msg = await event.get_reply_message()
    if msg == None:
        await event.reply("bot_username|xyz\n\ndatabase_id|xzy\n\nsubstart|xyz\n\nsubend|xyz\n\ndubstart|xyz\n\ndubend|xyz\n\ntarget|xyz\n\nstartep|xyz\n\nname|xyz")
        return
    try:
        media = await client.download_media(msg.media)
    except:
        media = None

    data = msg.raw_text.split("\n\n")
    fch = dict()

    for i in data:
        d1 = i.split("|")
        fch[d1[0]] = d1[1]

    database_id = fch['database_id']
    if not database_id.startswith("-100"):
        database_id = f"-100{database_id}"
    database_id = int(database_id)
    bot_username = fch['bot_username'].replace("@", "")
    target = fch['target']
    if not target.startswith("-100"):
        target = f"-100{target}"
    target = int(target)

    a = int(fch["startep"])
    txt = ""
    for i in range(int(fch["substart"].split("/")[-1]),int(fch["subend"].split("/")[-1])+1, 3):
        #sub
        l1, l2, l3 = await client.get_messages(event.chat_id, ids=[i, i+1, i+2])
        
        m1 = await client.send_message(database_id, l1)
        m2 = await client.send_message(database_id, l2)
        m3 = await client.send_message(database_id, l3)

        #dub
        d_id = i + int(fch["dubstart"].split("/")[-1]) - int(fch["substart"].split("/")[-1])
        l4, l5, l6 = await client.get_messages(event.chat_id, ids=[d_id, d_id+1, d_id+2])

        m4 = await client.send_message(database_id, l4)
        m5 = await client.send_message(database_id, l5)
        m6 = await client.send_message(database_id, l6)

        lsub = f"t.me/{bot_username}?start=batch_{m1.id}_{m3.id}"
        ldub = f"t.me/{bot_username}?start=batch_{m4.id}_{m6.id}"
        
        name = fch["name"]

        if a<10:
            temp = name.replace("OwO", f"00{a}")
            temp = temp.replace("UwU", f"0{a}")

        elif a<100:
            temp = name.replace("OwO", f"0{a}")
            temp = temp.replace("UwU", f"{a}")

        else:
            temp = name.replace("OwO", f"{a}")

        final = await bot.send_message(
            target,
            temp,
            file=media,
            buttons=[Button.url("Sub", lsub), Button.url("Dub", ldub)]
        )
        a += 1
        txt += f"t.me/c/{str(target).replace('-100', '')}/{final.id}"
        txt += "\n"
    await event.reply(txt)

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+check")))
async def _(event):
    def extract_episode_resolution(filename):
        parts = filename.split(" ")
        episode = None
        resolution = None
        for part in parts:
            if part.isdigit():
                episode = int(part)
            elif part.lower() in ("hdrip", "hdrip.mkv"):
                resolution = "4000"
            elif part.endswith("p.mkv"):
                resolution = part[:-5]
            elif part.endswith("p"):
                resolution = part[:-1]
        return episode, resolution
    await event.reply("On it")
    data = event.raw_text.split("\n")
    if "HD" in event.raw_text:
        epreses = ("360", "720", "1080", "4000")
    else:
        epreses = ("360", "720", "1080")
    channel_id = int(f"-100{data[1].split('/')[-2]}")
    start_link = int(data[1].split("/")[-1])
    end_link = int(data[2].split("/")[-1])
    ids = [i for i in range(start_link, end_link + 1)]
    x = await client.get_messages(channel_id, ids=ids)
    files = []
    
    msgs = dict()
    for i in x:
        try:
            if "caption" in event.raw_text:
                files.append(f"{i.id}:{i.raw_text}")
            else:
                files.append(f"{i.id}:{i.media.document.attributes[0].file_name}")
            msgs[i.id] = i
        except:
            pass
    start_ep = extract_episode_resolution(files[0])[0]
    end_ep = extract_episode_resolution(files[-1])[0]
    episodes = {ep: set(epreses) for ep in range(start_ep, end_ep + 1)}

    for filename in files:
        episode, resolution = extract_episode_resolution(filename)
        if episode is not None and resolution is not None and episode in episodes:
            episodes[episode].discard(resolution)

    missing_episodes = [(ep, missing_resolutions) for ep, missing_resolutions in episodes.items() if missing_resolutions]
    txt = "Missing Episodes:\n"
    for i in missing_episodes:
        txt += f"{i[0]}: {','.join(i[1])}\n"
    await event.reply(txt)
    if "sort" in event.raw_text:
        files.sort(key=lambda filename: (extract_episode_resolution(filename)[0], epreses.index(extract_episode_resolution(filename)[1])))
        for i in files:
            id = int(i.split(":")[0])
            await client.send_message(event.chat_id, msgs[id])
            time.sleep(0.25)

@client.on(events.NewMessage(from_users=approved_users, pattern=("\+linkedit")))
async def _(event):
    msg = await event.get_reply_message()
    if msg == None:
        await event.reply("channel_id|-100xyz\n\nmsglink|xyz\n\nnewlink360|xyz\n\nnewlink720|xyz\n\nnewlink1080|xyz")
        return
    else:
        data = msg.raw_text.split("\n\n")
        d = dict() 
        for i in data:
            d1 = i.split("|")
            d[d1[0]] = d1[1]
    channel_id = int(d["channel_id"])
    msg_id = int(d["msglink"].split("/")[-1])
    x = await bot.get_messages(channel_id, ids=msg_id)
    await x.edit(buttons=[Button.url("360p", d["newlink360"]), Button.url("720p", d["newlink720"]), Button.url("1080p", d["newlink1080"])])
    await event.reply("done")

# @client.on(events.NewMessage(from_users=approved_users, pattern=("\+swapusername")))
# async def _(event):
#     msg = await event.get_reply_message()
#     if msg == None:
#         await event.reply("channel_id|-100xyz\n\nstart_link|xyz\n\nend_link|xyz\n\nnew_bot_username|@xyz")
#         return
#     else:
#         data = msg.raw_text.split("\n\n")
#         d = dict() 
#         for i in data:
#             d1 = i.split("|")
#             d[d1[0]] = d1[1]


client.start()

client.run_until_disconnected()
