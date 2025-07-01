import discord
from discord.ext import commands
import json
import os
import random
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = 'players.json'

# Initialize data file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Load and save data
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
        data[uid] = {
            "floor": 1,
            "boss_defeated": False,
            "stats": 0,
            "inventory": []
        }
        save_data(data)
    return data[uid]

def update_player(user_id, updated):
    data = load_data()
    data[str(user_id)] = updated
    save_data(data)

# 🗡️ Mob slaying command
@bot.command()
async def slay(ctx):
    player = get_player(ctx.author.id)
    floor = player["floor"]

    # Stat gain and possible item drops
    gained_stats = random.randint(1, 3)
    player["stats"] += gained_stats

    drop_chance = random.random()
    item_drop = None
    if drop_chance < 0.4:
        item_drop = f"Floor{floor} Essence"
        player["inventory"].append(item_drop)

    update_player(ctx.author.id, player)

    msg = f"⚔️ You slayed a Floor {floor} mob and gained **{gained_stats}** stats!"
    if item_drop:
        msg += f"\n🎁 You also found: `{item_drop}`"
    await ctx.send(msg)

# 🧪 Crafting command
@bot.command()
async def craft(ctx, *, item_name: str):
    player = get_player(ctx.author.id)
    inventory = player["inventory"]

    recipe = {
        "Iron Sword": ["Floor1 Essence", "Floor1 Essence"],
        "Healing Potion": ["Floor1 Essence"]
    }

    required = recipe.get(item_name)
    if not required:
        return await ctx.send("❌ Unknown recipe.")

    # Check if all required items are in inventory
    for ingredient in required:
        if inventory.count(ingredient) < required.count(ingredient):
            return await ctx.send("⚠️ You don’t have all the items needed to craft this.")

    # Remove used items
    for ingredient in required:
        inventory.remove(ingredient)

    inventory.append(item_name)
    player["inventory"] = inventory
    update_player(ctx.author.id, player)

    await ctx.send(f"🛠️ You crafted a **{item_name}**!")

# 🧍 Floor status
@bot.command()
async def floor(ctx):
    player = get_player(ctx.author.id)
    status = "🟢 Boss defeated" if player["boss_defeated"] else "🔴 Boss not yet defeated"
    await ctx.send(f"🗺️ {ctx.author.display_name}, you're on **Floor {player['floor']}** — {status} (Stats: {player['stats']})")

# 🧟 Boss battle — now requires enough stats
@bot.command()
async def defeatboss(ctx):
    player = get_player(ctx.author.id)
    floor = player["floor"]
    required_stats = floor * 5  # Example scaling

    if player["boss_defeated"]:
        await ctx.send("✅ You've already defeated this floor's boss. Use `!ascend` to move on.")
    elif player["stats"] < required_stats:
        await ctx.send(f"❌ You need at least **{required_stats}** stats to challenge the boss. Use `!slay` to build your strength.")
    else:
        player["boss_defeated"] = True
        update_player(ctx.author.id, player)
        await ctx.send(f"⚔️ {ctx.author.display_name} defeated the boss on Floor {floor}!")

# 🚀 Ascend to next floor
@bot.command()
async def ascend(ctx):
    player = get_player(ctx.author.id)
    if not player["boss_defeated"]:
        await ctx.send("❌ You must defeat the boss before ascending.")
    else:
        player["floor"] += 1
        player["boss_defeated"] = False
        player["stats"] = 0  # Reset stats on new floor
        update_player(ctx.author.id, player)
        await ctx.send(f"🚀 {ctx.author.display_name} ascended to **Floor {player['floor']}**!")

# 📦 View inventory
@bot.command()
async def inventory(ctx):
    player = get_player(ctx.author.id)
    items = player["inventory"]
    if not items:
        await ctx.send("📦 Your inventory is empty.")
    else:
        await ctx.send(f"📦 Inventory: `{', '.join(items)}`")

# Keep-alive for Replit hosting
keep_alive()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
