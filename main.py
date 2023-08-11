import time
from telethon import events, Button
from config import client, bot, main_bot_id
import os
from telethon.tl.functions.channels import JoinChannelRequest
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

@client.on(events.NewMessage(outgoing=True, pattern=("\+help")))
async def help_function(event):
    await event.edit(help_text)

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
    
@client.on(events.NewMessage(outgoing=True, pattern=("\+pet")))
async def pet(event):
    reply = await event.get_reply_message()
    await event.delete()
    pic = await client.download_profile_photo(reply.sender_id)
    petpet.make(pic, "res.gif")
    await reply.reply(file="res.gif")

@client.on(events.NewMessage(outgoing=True, pattern=("\+copy")))
async def copy_message(event):
    try:
        global msg
        await event.edit("okay, on it")
        msg = await event.get_reply_message()
        await event.edit("Done.")
    except Exception as e:
        await event.edit(str(e))

@client.on(events.NewMessage(outgoing=True, pattern=("\+linkp")))
async def _(event):
    global link_preview
    link_preview = False if link_preview == True else True
    await event.edit(f"Link preview set to: {link_preview}")

@client.on(events.NewMessage(outgoing=True, pattern=("\+show")))
async def preveiw(event):
    try:
        global msg
        await event.edit("okay, on it")
        if msg is not None:
            media = await client.download_media(msg.media)
            await bot.send_message(event.chat_id,message=msg.text,buttons=msg.buttons,file=media,link_preview=link_preview)
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
                a = await bot.send_message(ent,message=msg.text,buttons=msg.buttons,file=media,link_preview=link_preview)
                ads.append(i + "/" + str(a.id))
            await event.edit("\n".join(ads))
            try:
                os.remove(media)
            except:
                pass
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

@client.on(events.NewMessage(outgoing=True, pattern=("\+promote")))
async def _(event):
    data = event.raw_text.split(" ")
    user = event.sender_id
    me = await bot.get_entity(main_bot_id)
    chat = await bot.get_entity(data[1])
    perms = await bot.get_permissions(chat, me)
    await client(JoinChannelRequest(data[1]))
    await bot.edit_admin(chat, user, change_info=perms.change_info, post_messages= perms.post_messages, edit_messages=perms.edit_messages, delete_messages=perms.delete_messages, invite_users=perms.invite_users, add_admins=perms.add_admins, manage_call=perms.manage_call)
    await event.edit(f"Promoted in {data[1]}")

@client.on(events.NewMessage(outgoing=True, pattern=("\+mkpost")))
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
            Button.url("1080p", f"t.me/{bot_username}?start=single_{channel_id}_{m1.id}client{event.sender_id}"), 
            Button.url("720p", f"t.me/{bot_username}?start=single_{channel_id}_{m2.id}client{event.sender_id}"), 
            Button.url("360p", f"t.me/{bot_username}?start=single_{channel_id}_{m3.id}client{event.sender_id}")
        ]
    )
    
@client.on(events.NewMessage(outgoing=True, pattern=("\+bulkmkpost")))
async def _(event):
    msg = await event.get_reply_message()
    if msg == None:
        await event.reply("bot_username|xyz\n\ndatabase_id|xyz\n\nstart|xyz\n\nend|xyz\n\ntarget|xyz\n\nstartep|xyz\n\nname|xyz")
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
    if not target.startswith("-100"):
        target = f"-100{target}"
    target = int(target)


    a = int(fch["startep"])
    txt = ""
    for i in range(int(fch["start"]),int(fch["end"])+1, 3):
        l1 = await client.get_messages(event.chat_id, ids=i)
        l2 = await client.get_messages(event.chat_id, ids=i+1)
        l3 = await client.get_messages(event.chat_id, ids=i+2)
        
        m1 = await client.send_message(database_id, l1)
        m2 = await client.send_message(database_id, l2)
        m3 = await client.send_message(database_id, l3)

        name = fch["name"]
        l1080 = f"t.me/{bot_username}?start=single_{database_id}_{m1.id}client{event.sender_id}"
        l720 = f"t.me/{bot_username}?start=single_{database_id}_{m2.id}client{event.sender_id}"
        l360 = f"t.me/{bot_username}?start=single_{database_id}_{m3.id}client{event.sender_id}"
        
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
            buttons=[Button.url("360p", l360), Button.url("720p", l720), Button.url("1080p", l1080)]
        )
        a += 1
        txt += f"t.me/c/{target.replace('-100', '')}/{final.id}"
        txt += "\n"
    await event.reply(txt)

@client.on(events.NewMessage(outgoing=True, pattern=("\+subdubbulkpost")))
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
    for i in range(int(fch["substart"]),int(fch["subend"])+1, 3):
        #sub
        l1, l2, l3 = await client.get_messages(event.chat_id, ids=[i, i+1, i+2])
        
        m1 = await client.send_message(database_id, l1)
        m2 = await client.send_message(database_id, l2)
        m3 = await client.send_message(database_id, l3)

        #dub
        d_id = i + int(fch["dubstart"]) - int(fch["substart"])
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

client.start()

client.run_until_disconnected()
