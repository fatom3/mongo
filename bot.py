from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
MONGO = "mongodb+srv://boda:boda@cluster0.ehpfqek.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(MONGO)
mongodb = mongo.bot
usersdb = mongodb.users

async def is_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True
    
async def get_users() -> list:
 	users_list = []
 	async for user in usersdb.find({"user_id": {"$gt": 0}}):
 	  users_list.append(user)
 	return users_list
    
async def add_user(user_id: int):
    is_served = await is_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})   

groupsdb = mongodb.groups

async def is_group(chat_id: int) -> bool:
    group = await groupsdb.find_one({"chat_id": chat_id})
    if not group:
        return False
    return True

async def get_groups() -> list:
    groups_list = []
    async for group in groupsdb.find({"chat_id": {"$gt": 0}}):
        groups_list.append(group)
    return groups_list
    
async def add_group(chat_id: int):
    is_served = await is_group(chat_id)
    if is_served:
        return
    return await groupsdb.insert_one({"chat_id": chat_id})       
    
    
from pyrogram import Client , filters
api_id = 20993785
api_hash = "a5378e174b86b9fc3cf1ef284e2767b4"
token = "6041810038:AAH6JSVUQFVMzMJFYbs84Iu0RSb6MkSRQvY"
OWNER = 5836041718
app = Client(
api_id=api_id,
api_hash=api_hash,
bot_token=token
)

TEXT = """
**-> New User start your bot !

- Name : {}

- Id : {}

- Users stats : {}

➖**
"""

START = "مرحبا بك انا بوت بسيط لتجربه التخزين @UG_U4"

@app.on_message(filters.command('start'))
async def st(client,message):
	user_id = message.from_user.id
	if not await is_user(user_id):
		await add_user(user_id)
		a = message.from_user.mention
		b = message.from_user.id
		c = len(await get_users())
		await app.send_message(
		OWNER,
		TEXT.format(a,b,c))
		await app.send_message(
		message.chat.id,
		START.format(a),
		reply_to_message_id=message.id)
		
NEW_GROUP = """
-> New Group !

-> Group Title : {}

-> Stats now : {}

➖
"""

@app.on_message(filters.new_chat_members)
async def New_group(client,message):
	chat_id = message.chat.id
	await add_group(chat_id)
	bot_id = int(token.split(":")[0])
	for member in message.new_chat_members:
		if member.id == bot_id:
			await message.reply(
            " ** Thanks for add me to your group ! **")
            a = message.chat.title
            b = len(await get_groups())
            await app.send_message(
                 OWNER,
                 NEW_GROUP.format(a,b)
            )
                 
STATS_TEXT = """**
Hello !

Bot stats :

Users : {}
Groups : {}

➖**
"""

STATS = filters.command("stats") & filters.user(OWNER)
STATS2 = filters.regex("^الاحصائيات$") & filters.user(OWNER)
@app.on_message(STATS)
@app.on_message(STATS2)
@app.on_edited_message(STATS)
@app.on_edited_message(STATS2)
async def stats(client, message):
      id = message.chat.id
      stats = len(await get_users())
      group_stats = len(await get_groups())
      await app.send_message(
          id,
          STATS_TEXT.foramat(stats,group_stats),
          reply_to_message_id = message.id
      )
      
import os
COPY = filters.command("getcopy") & filters.user(OWNER)
COPY2 = filters.regex("^نسخة احتياطية$") & filters.user(OWNER)
@app.on_message(COPY)
@app.on_message(COPY2)
@app.on_edited_message(COPY)
@app.on_edited_message(COPY2)
async def getcopy(client, message):
       id = message.chat.id
       d = message.id    
       m = await message.reply("**-» Processing ..**")
       filename = "@UG_U4 - Users .txt"
       with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(await get_users()))
       stats = len(await get_users())
       await message.reply_document(
            document=filename,
            caption=f"-» Users : {stats} ",
            quote=False
       )
       os.remove(filename)
       filename2 = "@UG_U4 - Groups .txt"
       with open(filename2, "w+", encoding="utf8") as out_file:
            out_file.write(str(await get_groups()))
       stats2 = len(await get_groups())
       await message.reply_document(
            document=filename2,
            caption=f"-» Groups : {stats2} ",
            quote=False
       )
       await m.delete()
       os.remove(filename2)
       
       
USERS_BROADCAST = filters.command("broadcast_users") & filters.user(OWNER)
USERS_BROADCAST2 = filters.regex("اذاعة بالخاص") & filters.user(OWNER)
@app.on_message(USERS_BROADCAST)
@app.on_message(USERS_BROADCAST2)
async def broadcast(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.id
        y = message.chat.id
        sent = 0
        users = []
        hah = await get_users()
        for user in hah:
            users.append(int(user["user_id"]))
        for i in users:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"تمت الاذاعه الي  {sent} User ! ")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**استخدم الامر بجوار الرساله التي تريد اذاعتها او قم بالرد علي رساله**"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    users = []
    hah = await get_users()
    for user in hah:
        users.append(int(user["user_id"]))
    for i in users:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"تمت الاذاعه الي  {sent} User !")
    

GROUPS_BROADCAST = filters.command("broadcast_groups") & filters.user(OWNER)
GROUPA_BROADCAST2 = filters.regex("اذاعة بالجروبات") & filters.user(OWNER)
@app.on_message(GROUPS_BROADCAST)
@app.on_message(GROUPS_BROADCAST2)
async def broadcasttt(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.id
        y = message.chat.id
        sent = 0
        groups = []
        hah = await get_groups()
        for group in hah:
            groups.append(int(user["chat_id"]))
        for i in groups:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"تمت الاذاعه الي  {sent} Group ! ")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**استخدم الامر مع الرساله التي تريد.اذاعتها او قم بالرد علي رساله **"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    groups = []
    hah = await get_users()
    for group in hah:
        groups.append(int(user["chat_id"]))
    for i in groups:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"تمت الاذاعه الي  {sent} Group !")    
    

##################### Run Client #####################
print("«- Your Client has been started ✓ -»")
app.run()
