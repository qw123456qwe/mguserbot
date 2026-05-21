# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                    MEGA USERBOT v3.1 - FIXED VERSION                      ║
# ╚════════════════════════════════════════════════════════════════════════════╝

import asyncio
import logging
import random
import time
from datetime import datetime, timedelta
from collections import defaultdict
from io import BytesIO

import qrcode

from telethon import TelegramClient, events
from telethon.tl.types import InputMediaDice

# ====================== CONFIG ======================
from config import (
    API_ID,
    API_HASH,
    SESSION_NAME,
    OWNER_ID,
    PREFIX,
    AUTO_REPLY_MSG,
    LOG_CHANNEL
)

# ====================== LOGGING ======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("userbot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)

# ====================== CLIENT ======================
client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)

start_time = time.time()

# ====================== XOTIRA ======================
afk_mode = {
    "aktiv": False,
    "sabab": "",
    "vaqt": None
}

auto_reply_on = {
    "aktiv": True
}

blocked_words = set()
notes = {}
warned_users = defaultdict(int)

# ====================== FUNKSIYALAR ======================

def is_owner(event):
    return event.sender_id == OWNER_ID

async def safe_edit(event, text):
    try:
        await event.edit(text)
    except Exception as e:
        log.error(f"Edit error: {e}")

async def safe_reply(event, text):
    try:
        await event.reply(text)
    except Exception as e:
        log.error(f"Reply error: {e}")

# ╔════════════════════════════════════════════════════╗
# ║                     ASOSIY                         ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}start$", outgoing=True))
async def start_cmd(event):
    await safe_edit(
        event,
        "🚀 MEGA USERBOT v3.1 ishga tushdi!"
    )

@client.on(events.NewMessage(pattern=rf"\{PREFIX}help$", outgoing=True))
async def help_cmd(event):

    text = """
🔥 MEGA USERBOT BUYRUQLARI

⚡ Asosiy:
.ping
.alive
.help

🎮 O'yin:
.dice
.coin
.rps tosh/qaychi/qogoz
.slot

🛠 Utilit:
.calc 5+5
.qr matn
.joke

💤 AFK:
.afk sabab
.unafk

📝 Notes:
.save nom matn
.get nom

🚫 Spam:
.addword so'z
.delword so'z

👥 Group:
.tagall
.warn
.purge
"""

    await safe_edit(event, text)

# ╔════════════════════════════════════════════════════╗
# ║                    PING                           ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}ping$", outgoing=True))
async def ping_cmd(event):

    start = time.time()

    msg = await event.edit("🏓 Ping...")

    ms = round((time.time() - start) * 1000, 2)

    await msg.edit(f"🏓 Pong! `{ms} ms`")

# ╔════════════════════════════════════════════════════╗
# ║                    ALIVE                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}alive$", outgoing=True))
async def alive_cmd(event):

    uptime = str(
        timedelta(
            seconds=int(time.time() - start_time)
        )
    )

    text = (
        "✅ Userbot ishlayapti!\n"
        f"⏱ Uptime: `{uptime}`"
    )

    await safe_edit(event, text)

# ╔════════════════════════════════════════════════════╗
# ║                     DICE                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}dice$", outgoing=True))
async def dice_cmd(event):

    try:
        await client.send_message(
            event.chat_id,
            file=InputMediaDice("🎲")
        )

        await event.delete()

    except Exception as e:
        log.error(e)

# ╔════════════════════════════════════════════════════╗
# ║                     COIN                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}coin$", outgoing=True))
async def coin_cmd(event):

    result = random.choice([
        "🪙 Tura",
        "🪙 Yuz"
    ])

    await safe_edit(event, result)

# ╔════════════════════════════════════════════════════╗
# ║                     RPS                           ║
# ╚════════════════════════════════════════════════════╝

@client.on(
    events.NewMessage(
        pattern=rf"\{PREFIX}rps (tosh|qaychi|qogoz)$",
        outgoing=True
    )
)
async def rps_cmd(event):

    player = event.pattern_match.group(1)

    bot = random.choice([
        "tosh",
        "qaychi",
        "qogoz"
    ])

    if player == bot:
        result = "⚖️ Durrang"

    elif (
        (player == "tosh" and bot == "qaychi") or
        (player == "qaychi" and bot == "qogoz") or
        (player == "qogoz" and bot == "tosh")
    ):
        result = "🎉 Siz yutdingiz"

    else:
        result = "😔 Bot yutdi"

    text = (
        f"👤 Siz: {player}\n"
        f"🤖 Bot: {bot}\n\n"
        f"{result}"
    )

    await safe_edit(event, text)

# ╔════════════════════════════════════════════════════╗
# ║                     SLOT                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}slot$", outgoing=True))
async def slot_cmd(event):

    emojis = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]

    a, b, c = random.choices(emojis, k=3)

    if a == b == c:
        text = f"🎰 JACKPOT!\n{a}{b}{c}"

    else:
        text = f"🎰 {a}{b}{c}"

    await safe_edit(event, text)

# ╔════════════════════════════════════════════════════╗
# ║                     QR                            ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}qr (.+)", outgoing=True))
async def qr_cmd(event):

    data = event.pattern_match.group(1)

    qr_img = qrcode.make(data)

    bio = BytesIO()

    qr_img.save(bio, "PNG")

    bio.seek(0)

    await client.send_file(
        event.chat_id,
        bio,
        caption="✅ QR kod tayyor"
    )

    await event.delete()

# ╔════════════════════════════════════════════════════╗
# ║                    CALC                           ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}calc (.+)", outgoing=True))
async def calc_cmd(event):

    expr = event.pattern_match.group(1)

    try:

        allowed = {
            "__builtins__": None,
            "abs": abs,
            "round": round,
            "pow": pow
        }

        result = eval(expr, allowed)

        await safe_edit(
            event,
            f"🧮 Natija: `{result}`"
        )

    except Exception:
        await safe_edit(
            event,
            "❌ Xato ifoda"
        )

# ╔════════════════════════════════════════════════════╗
# ║                    JOKE                           ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}joke$", outgoing=True))
async def joke_cmd(event):

    jokes = [
        "🤣 Dasturchi nega suv ichmaydi? Chunki bug chiqadi.",
        "🐍 Python indent bilan yashaydi.",
        "💀 Kod ishlasa tegma."
    ]

    await safe_edit(
        event,
        random.choice(jokes)
    )

# ╔════════════════════════════════════════════════════╗
# ║                     AFK                           ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}afk(?: (.+))?$", outgoing=True))
async def afk_cmd(event):

    reason = event.pattern_match.group(1)

    if not reason:
        reason = "Sabab yo'q"

    afk_mode["aktiv"] = True
    afk_mode["sabab"] = reason
    afk_mode["vaqt"] = datetime.now()

    await safe_edit(
        event,
        f"💤 AFK yoqildi\n📌 Sabab: {reason}"
    )

@client.on(events.NewMessage(pattern=rf"\{PREFIX}unafk$", outgoing=True))
async def unafk_cmd(event):

    afk_mode["aktiv"] = False

    await safe_edit(
        event,
        "✅ AFK o'chirildi"
    )

# ╔════════════════════════════════════════════════════╗
# ║                 AUTO AFK JAVOB                    ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(incoming=True))
async def afk_auto_reply(event):

    if not afk_mode["aktiv"]:
        return

    if event.sender_id == OWNER_ID:
        return

    since = datetime.now() - afk_mode["vaqt"]

    text = (
        f"💤 Men AFK holatdaman\n"
        f"📌 Sabab: {afk_mode['sabab']}\n"
        f"⏱ {since.seconds // 60} minut bo'ldi"
    )

    try:
        await event.reply(text)
    except:
        pass

# ╔════════════════════════════════════════════════════╗
# ║                 SPAM FILTER                       ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(incoming=True))
async def spam_filter(event):

    if not blocked_words:
        return

    text = (event.raw_text or "").lower()

    for word in blocked_words:

        if word in text:

            try:
                await event.delete()
            except Exception as e:
                log.error(e)

            break

# ╔════════════════════════════════════════════════════╗
# ║                  ADD WORD                         ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}addword (.+)", outgoing=True))
async def addword_cmd(event):

    word = event.pattern_match.group(1).lower()

    blocked_words.add(word)

    await safe_edit(
        event,
        f"✅ Qo'shildi: `{word}`"
    )

@client.on(events.NewMessage(pattern=rf"\{PREFIX}delword (.+)", outgoing=True))
async def delword_cmd(event):

    word = event.pattern_match.group(1).lower()

    blocked_words.discard(word)

    await safe_edit(
        event,
        f"🗑 O'chirildi: `{word}`"
    )

# ╔════════════════════════════════════════════════════╗
# ║                    NOTES                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}save (\w+) (.+)", outgoing=True))
async def save_note(event):

    name = event.pattern_match.group(1)

    text = event.pattern_match.group(2)

    notes[name] = text

    await safe_edit(
        event,
        f"💾 Saqlandi: `{name}`"
    )

@client.on(events.NewMessage(pattern=rf"\{PREFIX}get (\w+)", outgoing=True))
async def get_note(event):

    name = event.pattern_match.group(1)

    if name not in notes:

        await safe_edit(
            event,
            "❌ Note topilmadi"
        )

        return

    await safe_edit(
        event,
        f"📝 {name}\n\n{notes[name]}"
    )

# ╔════════════════════════════════════════════════════╗
# ║                     WARN                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}warn$", outgoing=True))
async def warn_cmd(event):

    reply = await event.get_reply_message()

    if not reply:

        await safe_edit(
            event,
            "❌ Reply qiling"
        )

        return

    uid = reply.sender_id

    warned_users[uid] += 1

    await safe_edit(
        event,
        f"⚠️ Warn: {warned_users[uid]}/3"
    )

# ╔════════════════════════════════════════════════════╗
# ║                    TAGALL                         ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}tagall$", outgoing=True))
async def tagall_cmd(event):

    text = "📢 Barchaga xabar\n\n"

    async for user in client.iter_participants(event.chat_id):

        if user.bot:
            continue

        text += f"[‌](tg://user?id={user.id})"

        if len(text) > 3500:

            await client.send_message(
                event.chat_id,
                text
            )

            text = ""

    if text:
        await client.send_message(
            event.chat_id,
            text
        )

    await event.delete()

# ╔════════════════════════════════════════════════════╗
# ║                    PURGE                          ║
# ╚════════════════════════════════════════════════════╝

@client.on(events.NewMessage(pattern=rf"\{PREFIX}purge$", outgoing=True))
async def purge_cmd(event):

    reply = await event.get_reply_message()

    if not reply:

        await safe_edit(
            event,
            "❌ Reply qiling"
        )

        return

    ids = []

    async for msg in client.iter_messages(
        event.chat_id,
        min_id=reply.id,
        max_id=event.id
    ):
        ids.append(msg.id)

    try:

        await client.delete_messages(
            event.chat_id,
            ids
        )

    except Exception as e:
        log.error(e)

# ╔════════════════════════════════════════════════════╗
# ║                     MAIN                          ║
# ╚════════════════════════════════════════════════════╝

async def main():

    await client.start()

    me = await client.get_me()

    log.info(
        f"✅ Userbot ishga tushdi -> {me.first_name} ({me.id})"
    )

    print("\n🚀 MEGA USERBOT v3.1 ISHGA TUSHDI\n")

    await client.run_until_disconnected()

if __name__ == "__main__":

    asyncio.run(main())
