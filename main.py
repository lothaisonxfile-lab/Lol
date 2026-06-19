import sys, time, asyncio, random
from telethon import TelegramClient, events

API_ID = 25099107
API_HASH = "ef890f66dff1bbb7b54125cfd7d71592"
OWNER_ID = 8481461120

autorai_status = False
autorai_content = None
autorai_time = 5
autorai_task = None
autorai_count = 0

# Danh sách icon để random
ICONS = ["🔥", "❄️", "🌟", "✨", "⚡", "🌈", "🍀", "💎", "🎯", "🚀", "🛸", "👾", "👑", "🛡️", "🔔", "📢", "💰", "🧨", "🧿", "🎈"]

def get_random_icons():
    # Lấy 2 icon ngẫu nhiên không trùng nhau
    selected = random.sample(ICONS, 2)
    return selected[0], selected[1]

def slow_print(text, delay=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

banner = """\033[38;5;199m                                              
             .............               
         ....:---======---:.....         
     ....:-==================-:...       
   ....:========================-...     
  ...:=============================:...   
  ..============+*####*+============....
  .===========+*****###+============:..
..==========+**********###*===========..
.-====++++=+************#####++++++=====..
:=====++++************#######*=+++======:.
-=====++++*#***##******#####*++++=====-.
-=====++++**##+---....:--+*###*+++======.
-========+**#*=..... ...:=*##*++++=====-.
-=========+****-........-***#+=========-.
.=====-----=**++=......=++**==----=====:.
.-=======++++*++++===+++*++++++======-..
..======++++++++++-:-=++++++++++++======..
  .===+++*=====================+*++===...
  ..-=+#++:::::::-=--=-::::::-=**+=-..   
   ..:*#+*::::::-=:-:---::::--++**-...   
     .****::::::-=-::---:::---***#:.     
     .**##::::::-+++=++-::----*#*%:.     
     .**##-:::::=*+++**=------*##*:.     
     ..+#*=:::::=*=--+*+-----=*#+:..     
       .:*********************#-..       
.---++++*++++++++++++++************++++--+=:
.....::::::::::::::::::::::::::::::::::::....
\033[1;36m╔══════════════════════════════════════════╗
║  Chào mừng đến với tool của tôi          ║
║  Tool được nâng cấp: Anti-Limit & Icon   ║
║  Admin: Gs ║
╚══════════════════════════════════════════╝\033[0m
"""

async def autorai_loop(client):
    global autorai_status, autorai_content, autorai_time, autorai_count
    while autorai_status and autorai_content:
        async for dialog in client.iter_dialogs():
            if not autorai_status: break
            
            if dialog.is_group:
                try:
                    i1, i2 = get_random_icons()
                    text_with_icons = f"{i1} {autorai_content['text']} {i2}"
                    
                    if autorai_content["media"]:
                        await client.send_file(
                            dialog.id,
                            autorai_content["media"],
                            caption=text_with_icons,
                            formatting_entities=autorai_content["entities"]
                        )
                    else:
                        await client.send_message(
                            dialog.id,
                            text_with_icons,
                            formatting_entities=autorai_content["entities"]
                        )
                    
                    # ANTI HẠN CHẾ: Nghỉ ngắn giữa các group để tránh bị Telegram gậy spam
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                except Exception:
                    continue
        
        autorai_count += 1

        # Nghỉ theo thời gian set (tính bằng phút)
        total_sleep = autorai_time * 60
        for _ in range(int(total_sleep)):
            if not autorai_status:
                break
            await asyncio.sleep(1)

def main():
    slow_print(banner)
    client = TelegramClient("RAILINK", API_ID, API_HASH)

    @client.on(events.NewMessage(pattern=r'^/autoraiall'))
    async def autoraiall_handler(event):
        global autorai_content, autorai_status, autorai_task
        if event.sender_id != OWNER_ID: return
        
        parts = event.raw_text.split(" ", 1)
        if len(parts) > 1:
            autorai_content = {"text": parts[1], "media": None, "entities": None}
        elif event.is_reply:
            reply_msg = await event.get_reply_message()
            autorai_content = {
                "text": reply_msg.text or "",
                "media": reply_msg.media,
                "entities": reply_msg.entities
            }
        else:
            await event.reply("⚠️ Dùng `/autoraiall {text}` hoặc reply rồi `/autoraiall`.")
            return
        
        await event.reply("✅ Đã set nội dung rải (Kèm Icon ngẫu nhiên).")

    @client.on(events.NewMessage(pattern=r'^/autorai$'))
    async def autorai_handler(event):
        global autorai_content, autorai_status, autorai_task
        if event.sender_id != OWNER_ID: return
        
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            autorai_content = {
                "text": reply_msg.text or "",
                "media": reply_msg.media,
                "entities": reply_msg.entities
            }
            await event.reply("✅ Đã set tin nhắn reply để rải.")
        else:
            await event.reply("⚠️ Hãy reply vào tin nhắn cần rải.")

    @client.on(events.NewMessage(pattern=r'^/autorai (on|off)$'))
    async def autorai_onoff(event):
        global autorai_status, autorai_task
        if event.sender_id != OWNER_ID: return
        
        if event.pattern_match.group(1) == "on":
            if autorai_status:
                return await event.reply("⚠️ Bot đang chạy rồi.")
            autorai_status = True
            autorai_task = asyncio.create_task(autorai_loop(client))
            await event.reply("▶️ Auto rải + Chống Limit đã BẬT.")
        else:
            autorai_status = False
            autorai_task = None
            await event.reply("⏹️ Auto rải đã TẮT.")

    @client.on(events.NewMessage(pattern=r'^/stoprai$'))
    async def stoprai(event):
        global autorai_task, autorai_status
        if event.sender_id != OWNER_ID: return
        autorai_status = False
        if autorai_task:
            autorai_task.cancel()
            autorai_task = None
        await event.reply("⏹️ Đã dừng ngay lập tức.")

    @client.on(events.NewMessage(pattern=r'^/settime (\d+)$'))
    async def set_time(event):
        global autorai_time
        if event.sender_id != OWNER_ID: return
        autorai_time = int(event.pattern_match.group(1))
        await event.reply(f"⏱️ Thời gian giữa các đợt: {autorai_time} phút.")

    @client.on(events.NewMessage(pattern=r'^/status$'))
    async def status(event):
        global autorai_status, autorai_count, autorai_time
        if event.sender_id != OWNER_ID: return
        status_text = (
            f"📊 **TRẠNG THÁI TOOL**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔹 Chế độ: {'🟢 Đang chạy' if autorai_status else '🔴 Đang dừng'}\n"
            f"🔄 Hoàn thành: {autorai_count} lần rải\n"
            f"⏱️ Giãn cách: {autorai_time} phút\n"
            f"🛡️ Anti-Limit: Đang hoạt động"
        )
        await event.reply(status_text)

    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    main()