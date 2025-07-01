import discord
from discord.ext import commands
import json
import os
from keep_alive import keep_alive  # Import the keep_alive server

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = 'players.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_player(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"floor": 1, "boss_defeated": False}
        save_data(data)
    return data[uid]

def update_player(user_id, updated):
    data = load_data()
    data[str(user_id)] = updated
    save_data(data)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")

@bot.command()
async def floor(ctx):
    player = get_player(ctx.author.id)
    status = "🟢 Boss defeated" if player["boss_defeated"] else "🔴 Boss not yet defeated"
    await ctx.send(f"🗺️ {ctx.author.display_name}, you're on **Floor {player['floor']}** — {status}")

@bot.command()
async def defeatboss(ctx):
    player = get_player(ctx.author.id)
    if player["boss_defeated"]:
        await ctx.send("✅ You've already defeated this floor's boss. Use `!ascend` to move on.")
    else:
        player["boss_defeated"] = True
        update_player(ctx.author.id, player)
        await ctx.send(f"⚔️ {ctx.author.display_name} defeated the boss on Floor {player['floor']}!")

@bot.command()
async def ascend(ctx):
    player = get_player(ctx.author.id)
    if not player["boss_defeated"]:
        await ctx.send("❌ You must defeat the floor's boss first using `!defeatboss`.")
    else:
        player["floor"] += 1
        player["boss_defeated"] = False
        update_player(ctx.author.id, player)
        await ctx.send(f"🚀 {ctx.author.display_name} ascended to **Floor {player['floor']}**!")

# --- Keep the bot alive ---
keep_alive()

# --- Run the bot ---
bot.run("PASTE_YOUR_DISCORD_BOT_TOKEN_HERE")
