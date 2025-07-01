import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = 'players.json'

# Load or create player data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_player_data(user_id):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {"floor": 1, "boss_defeated": False}
        save_data(data)
    return data[str(user_id)]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def floor(ctx):
    user_id = ctx.author.id
    player = get_player_data(user_id)
    await ctx.send(f"🗺️ {ctx.author.display_name} is currently on **Floor {player['floor']}**. "
                   f"{'🟢 Boss defeated' if player['boss_defeated'] else '🔴 Boss not yet defeated'}")

@bot.command()
async def defeatboss(ctx):
    user_id = ctx.author.id
    data = load_data()
    player = get_player_data(user_id)

    if player["boss_defeated"]:
        await ctx.send("✅ You’ve already defeated this floor’s boss. Use `!ascend` to move to the next floor.")
        return

    player["boss_defeated"] = True
    data[str(user_id)] = player
    save_data(data)
    await ctx.send(f"⚔️ {ctx.author.display_name} has defeated the boss of Floor {player['floor']}!")

@bot.command()
async def ascend(ctx):
    user_id = ctx.author.id
    data = load_data()
    player = get_player_data(user_id)

    if not player["boss_defeated"]:
        await ctx.send("❌ You must defeat the current floor's boss first with `!defeatboss`.")
        return

    player["floor"] += 1
    player["boss_defeated"] = False
    data[str(user_id)] = player
    save_data(data)

    await ctx.send(f"🚀 {ctx.author.display_name} has ascended to **Floor {player['floor']}**!")

bot.run(os.getenv("TOKEN"))