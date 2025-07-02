import discord
from discord.ext import commands
import json
import os
from random import choice
from keep_alive import keep_alive
import time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

DATA_FILE = 'players.json'

MOBS = {
    1: [
        {"name": "Goblin", "stat_reward": {"Strength": 1, "Agility": 0, "Intelligence": 0}, "drops": ["Goblin Ear"]},
        {"name": "Goblin Archer", "stat_reward": {"Strength": 0, "Agility": 1, "Intelligence": 0}, "drops": ["Arrow"]},
    ],
    2: [
        {"name": "Orc", "stat_reward": {"Strength": 2, "Agility": 1, "Intelligence": 0}, "drops": ["Orc Tooth"]},
        {"name": "Orc Shaman", "stat_reward": {"Strength": 1, "Agility": 0, "Intelligence": 1}, "drops": ["Magic Dust"]},
    ],
    3: [
        {"name": "Skeleton Warrior", "stat_reward": {"Strength": 2, "Agility": 0, "Intelligence": 0}, "drops": ["Bone Fragment"]},
        {"name": "Skeleton Archer", "stat_reward": {"Strength": 1, "Agility": 2, "Intelligence": 0}, "drops": ["Rusty Arrow"]},
    ],
    4: [
        {"name": "Bandit", "stat_reward": {"Strength": 3, "Agility": 1, "Intelligence": 0}, "drops": ["Bandit Dagger"]},
        {"name": "Bandit Mage", "stat_reward": {"Strength": 1, "Agility": 0, "Intelligence": 2}, "drops": ["Fire Essence"]},
    ],
    5: [
        {"name": "Wolf", "stat_reward": {"Strength": 3, "Agility": 2, "Intelligence": 0}, "drops": ["Wolf Pelt"]},
        {"name": "Dire Wolf", "stat_reward": {"Strength": 4, "Agility": 3, "Intelligence": 0}, "drops": ["Dire Fang"]},
    ],
    6: [
        {"name": "Goblin Berserker", "stat_reward": {"Strength": 4, "Agility": 1, "Intelligence": 0}, "drops": ["Berserker Axe"]},
        {"name": "Goblin Shaman", "stat_reward": {"Strength": 1, "Agility": 0, "Intelligence": 3}, "drops": ["Shaman Staff"]},
    ],
    7: [
        {"name": "Troll", "stat_reward": {"Strength": 5, "Agility": 1, "Intelligence": 0}, "drops": ["Troll Hide"]},
        {"name": "Troll Shaman", "stat_reward": {"Strength": 2, "Agility": 0, "Intelligence": 3}, "drops": ["Mystic Totem"]},
    ],
    8: [
        {"name": "Harpy", "stat_reward": {"Strength": 3, "Agility": 4, "Intelligence": 0}, "drops": ["Feather"]},
        {"name": "Harpy Mage", "stat_reward": {"Strength": 2, "Agility": 2, "Intelligence": 2}, "drops": ["Wind Crystal"]},
    ],
    9: [
        {"name": "Dark Knight", "stat_reward": {"Strength": 6, "Agility": 1, "Intelligence": 1}, "drops": ["Dark Sword"]},
        {"name": "Dark Mage", "stat_reward": {"Strength": 2, "Agility": 1, "Intelligence": 5}, "drops": ["Dark Orb"]},
    ],
    10: [
        {"name": "Ogre", "stat_reward": {"Strength": 7, "Agility": 1, "Intelligence": 0}, "drops": ["Ogre Club"]},
        {"name": "Ogre Shaman", "stat_reward": {"Strength": 3, "Agility": 0, "Intelligence": 4}, "drops": ["Ogre Totem"]},
    ],
    11: [
        {"name": "Stone Golem", "stat_reward": {"Strength": 8, "Agility": 0, "Intelligence": 0}, "drops": ["Golem Core"]},
        {"name": "Earth Elemental", "stat_reward": {"Strength": 6, "Agility": 1, "Intelligence": 2}, "drops": ["Earth Shard"]},
    ],
    12: [
        {"name": "Bandit Captain", "stat_reward": {"Strength": 7, "Agility": 3, "Intelligence": 0}, "drops": ["Captain's Sword"]},
        {"name": "Bandit Sorcerer", "stat_reward": {"Strength": 3, "Agility": 1, "Intelligence": 5}, "drops": ["Sorcerer’s Scroll"]},
    ],
    13: [
        {"name": "Wyvern", "stat_reward": {"Strength": 8, "Agility": 5, "Intelligence": 0}, "drops": ["Wyvern Scale"]},
        {"name": "Wyvern Mage", "stat_reward": {"Strength": 5, "Agility": 3, "Intelligence": 4}, "drops": ["Wyvern Claw"]},
    ],
    14: [
        {"name": "Vampire", "stat_reward": {"Strength": 7, "Agility": 3, "Intelligence": 2}, "drops": ["Vampire Fang"]},
        {"name": "Vampire Lord", "stat_reward": {"Strength": 10, "Agility": 4, "Intelligence": 6}, "drops": ["Lord's Cloak"]},
    ],
    15: [
        {"name": "Lich", "stat_reward": {"Strength": 4, "Agility": 1, "Intelligence": 9}, "drops": ["Lich Phylactery"]},
        {"name": "Death Knight", "stat_reward": {"Strength": 11, "Agility": 3, "Intelligence": 3}, "drops": ["Death Blade"]},
    ],
    16: [
        {"name": "Fire Elemental", "stat_reward": {"Strength": 6, "Agility": 4, "Intelligence": 5}, "drops": ["Flame Core"]},
        {"name": "Fire Dragon Whelp", "stat_reward": {"Strength": 10, "Agility": 6, "Intelligence": 4}, "drops": ["Dragon Scale"]},
    ],
    17: [
        {"name": "Ice Elemental", "stat_reward": {"Strength": 5, "Agility": 3, "Intelligence": 7}, "drops": ["Frost Shard"]},
        {"name": "Ice Dragon Whelp", "stat_reward": {"Strength": 9, "Agility": 5, "Intelligence": 6}, "drops": ["Dragon Fang"]},
    ],
    18: [
        {"name": "Shadow Assassin", "stat_reward": {"Strength": 8, "Agility": 8, "Intelligence": 3}, "drops": ["Shadow Dagger"]},
        {"name": "Shadow Mage", "stat_reward": {"Strength": 4, "Agility": 4, "Intelligence": 8}, "drops": ["Shadow Orb"]},
    ],
    19: [
        {"name": "Demon Imp", "stat_reward": {"Strength": 6, "Agility": 4, "Intelligence": 5}, "drops": ["Imp Claw"]},
        {"name": "Demon Brute", "stat_reward": {"Strength": 12, "Agility": 3, "Intelligence": 2}, "drops": ["Demon Horn"]},
    ],
    20: [
        {"name": "Hydra Head", "stat_reward": {"Strength": 13, "Agility": 2, "Intelligence": 3}, "drops": ["Hydra Scale"]},
        {"name": "Hydra Tail", "stat_reward": {"Strength": 14, "Agility": 3, "Intelligence": 2}, "drops": ["Hydra Fang"]},
    ],
    21: [
        {"name": "Giant Spider", "stat_reward": {"Strength": 8, "Agility": 7, "Intelligence": 1}, "drops": ["Spider Silk"]},
        {"name": "Spider Queen", "stat_reward": {"Strength": 15, "Agility": 8, "Intelligence": 5}, "drops": ["Queen’s Fang"]},
    ],
    22: [
        {"name": "Dark Sorcerer", "stat_reward": {"Strength": 6, "Agility": 3, "Intelligence": 12}, "drops": ["Dark Tome"]},
        {"name": "Necromancer", "stat_reward": {"Strength": 7, "Agility": 2, "Intelligence": 14}, "drops": ["Necro Bone"]},
    ],
    23: [
        {"name": "Minotaur", "stat_reward": {"Strength": 14, "Agility": 4, "Intelligence": 1}, "drops": ["Minotaur Horn"]},
        {"name": "Minotaur Warrior", "stat_reward": {"Strength": 15, "Agility": 5, "Intelligence": 2}, "drops": ["Minotaur Axe"]},
    ],
    24: [
        {"name": "Gorgon", "stat_reward": {"Strength": 12, "Agility": 5, "Intelligence": 5}, "drops": ["Gorgon Scale"]},
        {"name": "Medusa", "stat_reward": {"Strength": 13, "Agility": 6, "Intelligence": 7}, "drops": ["Medusa Hair"]},
    ],
    25: [
        {"name": "Phoenix", "stat_reward": {"Strength": 16, "Agility": 8, "Intelligence": 8}, "drops": ["Phoenix Feather"]},
        {"name": "Flame Spirit", "stat_reward": {"Strength": 14, "Agility": 7, "Intelligence": 6}, "drops": ["Spirit Ash"]},
    ],
    26: [
        {"name": "Kraken Tentacle", "stat_reward": {"Strength": 18, "Agility": 4, "Intelligence": 3}, "drops": ["Kraken Ink"]},
        {"name": "Kraken Eye", "stat_reward": {"Strength": 16, "Agility": 5, "Intelligence": 5}, "drops": ["Kraken Eye"]},
    ],
    27: [
        {"name": "Cyclops", "stat_reward": {"Strength": 20, "Agility": 3, "Intelligence": 2}, "drops": ["Cyclops Eye"]},
        {"name": "Cyclops Warrior", "stat_reward": {"Strength": 22, "Agility": 4, "Intelligence": 1}, "drops": ["Cyclops Club"]},
    ],
    28: [
        {"name": "Elemental Lord", "stat_reward": {"Strength": 17, "Agility": 7, "Intelligence": 10}, "drops": ["Elemental Core"]},
        {"name": "Elemental Mage", "stat_reward": {"Strength": 15, "Agility": 5, "Intelligence": 12}, "drops": ["Elemental Staff"]},
    ],
    29: [
        {"name": "Dread Knight", "stat_reward": {"Strength": 21, "Agility": 5, "Intelligence": 6}, "drops": ["Dread Sword"]},
        {"name": "Dread Sorcerer", "stat_reward": {"Strength": 18, "Agility": 6, "Intelligence": 12}, "drops": ["Dread Orb"]},
    ],
    30: [
        {"name": "Ancient Dragon Whelp", "stat_reward": {"Strength": 25, "Agility": 10, "Intelligence": 10}, "drops": ["Dragon Heart"]},
        {"name": "Ancient Dragon Mage", "stat_reward": {"Strength": 20, "Agility": 8, "Intelligence": 15}, "drops": ["Dragon Crystal"]},
    ],
    31: [
        {"name": "Shadow Wraith", "stat_reward": {"Strength": 19, "Agility": 14, "Intelligence": 8}, "drops": ["Wraith Essence"]},
        {"name": "Shadow Phantom", "stat_reward": {"Strength": 22, "Agility": 15, "Intelligence": 10}, "drops": ["Phantom Shard"]},
    ],
    32: [
        {"name": "Demon Lord's Guard", "stat_reward": {"Strength": 23, "Agility": 10, "Intelligence": 9}, "drops": ["Demon Guard Blade"]},
        {"name": "Demon Lord's Mage", "stat_reward": {"Strength": 20, "Agility": 9, "Intelligence": 14}, "drops": ["Demon Staff"]},
    ],
    33: [
        {"name": "Titan", "stat_reward": {"Strength": 28, "Agility": 5, "Intelligence": 5}, "drops": ["Titan’s Core"]},
        {"name": "Titan Warrior", "stat_reward": {"Strength": 30, "Agility": 6, "Intelligence": 3}, "drops": ["Titan Axe"]},
    ],
    34: [
        {"name": "Spirit Guardian", "stat_reward": {"Strength": 22, "Agility": 15, "Intelligence": 14}, "drops": ["Guardian Amulet"]},
        {"name": "Spirit Mage", "stat_reward": {"Strength": 18, "Agility": 12, "Intelligence": 18}, "drops": ["Spirit Wand"]},
    ],
    35: [
        {"name": "Hellhound", "stat_reward": {"Strength": 24, "Agility": 14, "Intelligence": 4}, "drops": ["Hellhound Fang"]},
        {"name": "Hellhound Alpha", "stat_reward": {"Strength": 26, "Agility": 16, "Intelligence": 5}, "drops": ["Alpha Fang"]},
    ],
    36: [
        {"name": "Frost Giant", "stat_reward": {"Strength": 27, "Agility": 7, "Intelligence": 7}, "drops": ["Frost Core"]},
        {"name": "Frost Giant Warrior", "stat_reward": {"Strength": 29, "Agility": 8, "Intelligence": 6}, "drops": ["Frost Axe"]},
    ],
    37: [
        {"name": "Arcane Sentinel", "stat_reward": {"Strength": 20, "Agility": 13, "Intelligence": 22}, "drops": ["Arcane Crystal"]},
        {"name": "Arcane Mage", "stat_reward": {"Strength": 18, "Agility": 12, "Intelligence": 25}, "drops": ["Arcane Staff"]},
    ],
    38: [
        {"name": "Necrotic Horror", "stat_reward": {"Strength": 25, "Agility": 10, "Intelligence": 20}, "drops": ["Necrotic Essence"]},
        {"name": "Necrotic Lord", "stat_reward": {"Strength": 28, "Agility": 11, "Intelligence": 24}, "drops": ["Lord's Phylactery"]},
    ],
    39: [
        {"name": "Celestial Knight", "stat_reward": {"Strength": 30, "Agility": 15, "Intelligence": 15}, "drops": ["Celestial Blade"]},
        {"name": "Celestial Mage", "stat_reward": {"Strength": 25, "Agility": 12, "Intelligence": 22}, "drops": ["Celestial Orb"]},
    ],
    40: [
        {"name": "Elder Dragon", "stat_reward": {"Strength": 35, "Agility": 20, "Intelligence": 18}, "drops": ["Elder Dragon Scale"]},
        {"name": "Elder Dragon Mage", "stat_reward": {"Strength": 30, "Agility": 18, "Intelligence": 25}, "drops": ["Elder Dragon Heart"]},
    ],
    41: [
        {"name": "Void Reaper", "stat_reward": {"Strength": 32, "Agility": 20, "Intelligence": 22}, "drops": ["Reaper Scythe"]},
        {"name": "Void Sorcerer", "stat_reward": {"Strength": 28, "Agility": 17, "Intelligence": 28}, "drops": ["Void Crystal"]},
    ],
    42: [
        {"name": "Storm Giant", "stat_reward": {"Strength": 33, "Agility": 15, "Intelligence": 20}, "drops": ["Storm Core"]},
        {"name": "Storm Giant Shaman", "stat_reward": {"Strength": 30, "Agility": 14, "Intelligence": 25}, "drops": ["Storm Staff"]},
    ],
    43: [
        {"name": "Phantom Wraith", "stat_reward": {"Strength": 29, "Agility": 25, "Intelligence": 22}, "drops": ["Wraith Essence"]},
        {"name": "Phantom Lord", "stat_reward": {"Strength": 32, "Agility": 28, "Intelligence": 25}, "drops": ["Lord’s Shard"]},
    ],
    44: [
        {"name": "Dragon Knight", "stat_reward": {"Strength": 36, "Agility": 20, "Intelligence": 20}, "drops": ["Dragon Knight Sword"]},
        {"name": "Dragon Mage", "stat_reward": {"Strength": 33, "Agility": 18, "Intelligence": 28}, "drops": ["Dragon Mage Staff"]},
    ],
    45: [
        {"name": "Titan Lord", "stat_reward": {"Strength": 40, "Agility": 15, "Intelligence": 15}, "drops": ["Titan Lord Core"]},
        {"name": "Titan Mage", "stat_reward": {"Strength": 35, "Agility": 15, "Intelligence": 25}, "drops": ["Titan Mage Orb"]},
    ],
    46: [
        {"name": "Ancient Wyrm", "stat_reward": {"Strength": 38, "Agility": 22, "Intelligence": 22}, "drops": ["Wyrm Scale"]},
        {"name": "Ancient Wyrm Mage", "stat_reward": {"Strength": 35, "Agility": 20, "Intelligence": 30}, "drops": ["Wyrm Heart"]},
    ],
    47: [
        {"name": "Ethereal Phantom", "stat_reward": {"Strength": 34, "Agility": 28, "Intelligence": 28}, "drops": ["Phantom Essence"]},
        {"name": "Ethereal Lord", "stat_reward": {"Strength": 37, "Agility": 30, "Intelligence": 32}, "drops": ["Lord’s Essence"]},
    ],
    48: [
        {"name": "Dread Dragon", "stat_reward": {"Strength": 45, "Agility": 25, "Intelligence": 25}, "drops": ["Dread Dragon Scale"]},
        {"name": "Dread Dragon Mage", "stat_reward": {"Strength": 40, "Agility": 22, "Intelligence": 35}, "drops": ["Dread Dragon Heart"]},
    ],
    49: [
        {"name": "Shadow Titan", "stat_reward": {"Strength": 42, "Agility": 28, "Intelligence": 30}, "drops": ["Shadow Titan Core"]},
        {"name": "Shadow Titan Mage", "stat_reward": {"Strength": 38, "Agility": 25, "Intelligence": 35}, "drops": ["Shadow Titan Orb"]},
    ],
    50: [
        {"name": "Final Boss", "stat_reward": {"Strength": 50, "Agility": 30, "Intelligence": 40}, "drops": ["Legendary Sword", "Legendary Armor"]},
        {"name": "Final Boss Mage", "stat_reward": {"Strength": 40, "Agility": 30, "Intelligence": 50}, "drops": ["Legendary Staff", "Legendary Robes"]},
    ],
}

BOSSES = {
    1: {"name": "Goblin King", "required_stats": {"Strength": 3, "Agility": 1, "Intelligence": 0}},
    2: {"name": "Orc Warlord", "required_stats": {"Strength": 5, "Agility": 3, "Intelligence": 1}},
    3: {"name": "Troll Brute", "required_stats": {"Strength": 7, "Agility": 4, "Intelligence": 1}},
    4: {"name": "Dark Elf Assassin", "required_stats": {"Strength": 6, "Agility": 7, "Intelligence": 3}},
    5: {"name": "Mountain Giant", "required_stats": {"Strength": 10, "Agility": 5, "Intelligence": 2}},
    6: {"name": "Necromancer Lord", "required_stats": {"Strength": 7, "Agility": 4, "Intelligence": 8}},
    7: {"name": "Fire Drake", "required_stats": {"Strength": 11, "Agility": 6, "Intelligence": 4}},
    8: {"name": "Shadow Phantom", "required_stats": {"Strength": 9, "Agility": 9, "Intelligence": 5}},
    9: {"name": "Stone Golem", "required_stats": {"Strength": 14, "Agility": 4, "Intelligence": 3}},
    10: {"name": "Vampire Count", "required_stats": {"Strength": 12, "Agility": 8, "Intelligence": 7}},
    11: {"name": "Sea Serpent", "required_stats": {"Strength": 15, "Agility": 10, "Intelligence": 5}},
    12: {"name": "Frost Wraith", "required_stats": {"Strength": 13, "Agility": 11, "Intelligence": 9}},
    13: {"name": "Warlock", "required_stats": {"Strength": 10, "Agility": 7, "Intelligence": 14}},
    14: {"name": "Ironclad Knight", "required_stats": {"Strength": 18, "Agility": 8, "Intelligence": 6}},
    15: {"name": "Sand Scorpion", "required_stats": {"Strength": 16, "Agility": 13, "Intelligence": 4}},
    16: {"name": "Storm Giant", "required_stats": {"Strength": 20, "Agility": 9, "Intelligence": 8}},
    17: {"name": "Dark Sorcerer", "required_stats": {"Strength": 15, "Agility": 10, "Intelligence": 15}},
    18: {"name": "Bloodhound", "required_stats": {"Strength": 17, "Agility": 16, "Intelligence": 7}},
    19: {"name": "Crystal Dragon", "required_stats": {"Strength": 22, "Agility": 14, "Intelligence": 10}},
    20: {"name": "Warlord Titan", "required_stats": {"Strength": 25, "Agility": 12, "Intelligence": 9}},
    21: {"name": "Spirit Guardian", "required_stats": {"Strength": 18, "Agility": 17, "Intelligence": 13}},
    22: {"name": "Venom Hydra", "required_stats": {"Strength": 23, "Agility": 18, "Intelligence": 11}},
    23: {"name": "Dread Knight", "required_stats": {"Strength": 27, "Agility": 14, "Intelligence": 14}},
    24: {"name": "Arcane Elemental", "required_stats": {"Strength": 16, "Agility": 15, "Intelligence": 22}},
    25: {"name": "Savage Beast", "required_stats": {"Strength": 28, "Agility": 20, "Intelligence": 8}},
    26: {"name": "Lich King", "required_stats": {"Strength": 22, "Agility": 13, "Intelligence": 25}},
    27: {"name": "Thunder Roc", "required_stats": {"Strength": 30, "Agility": 22, "Intelligence": 10}},
    28: {"name": "Feral Werewolf", "required_stats": {"Strength": 29, "Agility": 25, "Intelligence": 9}},
    29: {"name": "Soul Reaper", "required_stats": {"Strength": 24, "Agility": 19, "Intelligence": 26}},
    30: {"name": "Titan Colossus", "required_stats": {"Strength": 35, "Agility": 15, "Intelligence": 12}},
    31: {"name": "Inferno Phoenix", "required_stats": {"Strength": 33, "Agility": 26, "Intelligence": 15}},
    32: {"name": "Void Specter", "required_stats": {"Strength": 27, "Agility": 23, "Intelligence": 28}},
    33: {"name": "Blight Witch", "required_stats": {"Strength": 22, "Agility": 21, "Intelligence": 30}},
    34: {"name": "Iron Hydra", "required_stats": {"Strength": 38, "Agility": 17, "Intelligence": 18}},
    35: {"name": "Shadow Reaper", "required_stats": {"Strength": 31, "Agility": 28, "Intelligence": 21}},
    36: {"name": "Crystal Titan", "required_stats": {"Strength": 36, "Agility": 20, "Intelligence": 25}},
    37: {"name": "Abyssal Leviathan", "required_stats": {"Strength": 40, "Agility": 22, "Intelligence": 20}},
    38: {"name": "Stormcaller", "required_stats": {"Strength": 28, "Agility": 27, "Intelligence": 33}},
    39: {"name": "Doom Bringer", "required_stats": {"Strength": 37, "Agility": 24, "Intelligence": 29}},
    40: {"name": "Frost Giant King", "required_stats": {"Strength": 42, "Agility": 18, "Intelligence": 22}},
    41: {"name": "Dragon Emperor", "required_stats": {"Strength": 45, "Agility": 30, "Intelligence": 25}},
    42: {"name": "Necro Lord", "required_stats": {"Strength": 33, "Agility": 26, "Intelligence": 38}},
    43: {"name": "Celestial Paladin", "required_stats": {"Strength": 39, "Agility": 29, "Intelligence": 30}},
    44: {"name": "Dark Overlord", "required_stats": {"Strength": 44, "Agility": 28, "Intelligence": 34}},
    45: {"name": "Phoenix Lord", "required_stats": {"Strength": 47, "Agility": 32, "Intelligence": 28}},
    46: {"name": "Wraith King", "required_stats": {"Strength": 36, "Agility": 31, "Intelligence": 40}},
    47: {"name": "Titan Overlord", "required_stats": {"Strength": 50, "Agility": 25, "Intelligence": 27}},
    48: {"name": "Soul Tyrant", "required_stats": {"Strength": 42, "Agility": 35, "Intelligence": 37}},
    49: {"name": "Chaos Dragon", "required_stats": {"Strength": 53, "Agility": 33, "Intelligence": 31}},
    50: {"name": "Final Guardian", "required_stats": {"Strength": 60, "Agility": 40, "Intelligence": 40}},
}

# Player data helpers
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
        data[uid] = {
            "floor": 1,
            "boss_defeated": False,
            "stats": {"Strength": 0, "Agility": 0, "Intelligence": 0},
            "inventory": {},
            "skills": {},
            "level": 1,
            "xp": 0,
            "party": None
        }
        save_data(data)
    return data[uid]

def update_player(user_id, player_data):
    data = load_data()
    data[str(user_id)] = player_data
    save_data(data)

# Leveling helper
def xp_to_level(xp):
    # Simple example: level up every 100 xp
    return xp // 100 + 1

# PARTY SYSTEM
@bot.command()
async def createparty(ctx, *, name: str):
    data = load_data()
    # Check if user already in a party
    for uid, pdata in data.items():
        if pdata.get("party") == name:
            await ctx.send("You are already in a party.")
            return

    # Create party as a list in a separate file or keep as dict in data
    parties = data.get("parties", {})
    if name in parties:
        await ctx.send("Party name already exists.")
        return

    # Add party
    parties[name] = [str(ctx.author.id)]
    data["parties"] = parties
    # Add party to user
    data[str(ctx.author.id)]["party"] = name
    save_data(data)
    await ctx.send(f"Party '{name}' created and you joined it!")

@bot.command()
async def joinparty(ctx, *, name: str):
    data = load_data()
    parties = data.get("parties", {})
    if name not in parties:
        await ctx.send("That party does not exist.")
        return

    # Check if user already in a party
    for uid, pdata in data.items():
        if pdata.get("party") == name:
            await ctx.send("You are already in that party.")
            return

    # Remove user from old party if any
    old_party = data[str(ctx.author.id)].get("party")
    if old_party and old_party in parties:
        if str(ctx.author.id) in parties[old_party]:
            parties[old_party].remove(str(ctx.author.id))

    # Add to new party
    parties[name].append(str(ctx.author.id))
    data[str(ctx.author.id)]["party"] = name
    data["parties"] = parties
    save_data(data)
    await ctx.send(f"You joined party '{name}'!")

@bot.command()
async def leaveparty(ctx):
    data = load_data()
    party = data[str(ctx.author.id)].get("party")
    if not party:
        await ctx.send("You are not in a party.")
        return
    parties = data.get("parties", {})
    if party in parties:
        if str(ctx.author.id) in parties[party]:
            parties[party].remove(str(ctx.author.id))
    data[str(ctx.author.id)]["party"] = None
    data["parties"] = parties
    save_data(data)
    await ctx.send(f"You left party '{party}'.")

@bot.command()
async def partymembers(ctx):
    data = load_data()
    party = data[str(ctx.author.id)].get("party")
    if not party:
        await ctx.send("You are not in a party.")
        return
    parties = data.get("parties", {})
    members = parties.get(party, [])
    member_names = []
    for member_id in members:
        user = await bot.fetch_user(int(member_id))
        member_names.append(user.name)
    await ctx.send(f"Party '{party}' members: {', '.join(member_names)}")

# STAT COMMAND
@bot.command()
async def stats(ctx):
    player = get_player(ctx.author.id)
    embed = discord.Embed(title=f"{ctx.author.name}'s Stats", color=0x00ffcc)
    for stat, val in player['stats'].items():
        embed.add_field(name=stat, value=str(val), inline=True)
    embed.add_field(name="Level", value=player.get("level", 1), inline=True)
    embed.add_field(name="XP", value=player.get("xp", 0), inline=True)
    embed.add_field(name="Floor", value=player.get("floor", 1), inline=True)
    embed.add_field(name="Boss Defeated", value=str(player.get("boss_defeated", False)), inline=True)
    await ctx.send(embed=embed)

# FLOOR COMMAND
@bot.command()
async def floor(ctx):
    player = get_player(ctx.author.id)
    await ctx.send(f"You are currently on floor {player['floor']}.")

# SLAY COMMAND
@bot.command()
async def slay(ctx):
    player = get_player(ctx.author.id)
    floor = player['floor']
    mobs = MOBS.get(floor)
    if not mobs:
        await ctx.send("No mobs available on this floor.")
        return
    mob = choice(mobs)

    # Reward stats
    stat_reward = mob["stat_reward"]
    for stat, val in stat_reward.items():
        player['stats'][stat] = player['stats'].get(stat, 0) + val

    # Reward drops
    drops = mob.get("drops", [])
    for drop in drops:
        player['inventory'][drop] = player['inventory'].get(drop, 0) + 1

    # XP gain example (sum of stat rewards * 10)
    gained_xp = sum(stat_reward.values()) * 10
    player['xp'] += gained_xp
    old_level = player.get("level", 1)
    new_level = xp_to_level(player['xp'])
    player['level'] = new_level

    update_player(ctx.author.id, player)

    msg = f"You slayed a {mob['name']}! Gained stats: "
    msg += ", ".join(f"{k} +{v}" for k,v in stat_reward.items() if v > 0)
    msg += f". You also gained {gained_xp} XP."
    if new_level > old_level:
        msg += f" You leveled up to level {new_level}!"

    await ctx.send(msg)

# BOSS COMMAND
@bot.command()
async def boss(ctx):
    player = get_player(ctx.author.id)
    floor = player['floor']
    if floor not in BOSSES:
        await ctx.send("No boss on this floor.")
        return
    boss = BOSSES[floor]

    # Check if player meets required stats
    can_defeat = True
    for stat, required_val in boss["required_stats"].items():
        if player['stats'].get(stat, 0) < required_val:
            can_defeat = False
            break

    if not can_defeat:
        await ctx.send(f"You do not meet the required stats to defeat {boss['name']}. Required stats:\n" +
                       "\n".join(f"{k}: {v}" for k,v in boss["required_stats"].items()))
        return

    if player.get("boss_defeated", False):
        await ctx.send(f"You already defeated the boss on floor {floor}. Use !floorup to advance.")
        return

    # Defeat boss
    player["boss_defeated"] = True
    update_player(ctx.author.id, player)
    await ctx.send(f"Congrats! You defeated the boss {boss['name']} on floor {floor}!")

# FLOORUP COMMAND
@bot.command()
async def floorup(ctx):
    player = get_player(ctx.author.id)
    if not player.get("boss_defeated", False):
        await ctx.send("You must defeat the floor boss first!")
        return
    player['floor'] += 1
    player['boss_defeated'] = False
    update_player(ctx.author.id, player)
    await ctx.send(f"You have advanced to floor {player['floor']}!")

# INVENTORY COMMAND
@bot.command()
async def inventory(ctx):
    player = get_player(ctx.author.id)
    inv = player.get("inventory", {})
    if not inv:
        await ctx.send("Your inventory is empty.")
        return
    embed = discord.Embed(title=f"{ctx.author.name}'s Inventory", color=0x00ffcc)
    for item, qty in inv.items():
        embed.add_field(name=item, value=f"Quantity: {qty}", inline=True)
    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="SAO Bot Commands Help",
        description="Here are the commands you can use:",
        color=discord.Color.blue()
    )

    embed.add_field(name="!createparty <name>", value="Create a new party with the given name and join it.", inline=False)
    embed.add_field(name="!joinparty <name>", value="Join an existing party by name.", inline=False)
    embed.add_field(name="!leaveparty", value="Leave your current party.", inline=False)
    embed.add_field(name="!partymembers", value="List all members in your current party.", inline=False)
    embed.add_field(name="!stats", value="Show your current stats, level, XP, floor, and boss defeated status.", inline=False)
    embed.add_field(name="!floor", value="Show which floor you are currently on.", inline=False)
    embed.add_field(name="!slay", value="Slay a random mob on your current floor, gain stats, XP, and loot.", inline=False)
    embed.add_field(name="!boss", value="Attempt to fight the floor boss if you meet the stat requirements.", inline=False)
    embed.add_field(name="!floorup", value="Advance to the next floor if you defeated the current floor’s boss.", inline=False)
    embed.add_field(name="!inventory", value="Show your current inventory items and their quantities.", inline=False)
    embed.add_field(name="!menu", value="Show the general menu.", inline=False)
    embed.add_field(name="!help", value="Show this help message.", inline=False)

    await ctx.send(embed=embed)


# SAO STYLE INTERACTIVE MENU
from discord.ui import View, button

class SAOMenuView(View):
    def __init__(self, user_id):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.current_page = 'main'

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return False
        return True

    def get_embed(self):
        player = get_player(self.user_id)

        if self.current_page == 'main':
            embed = discord.Embed(
                title="SAO Menu",
                description="Welcome to your in-game menu. Choose an option below.",
                color=0x00ffcc,
            )
            embed.add_field(name="Floor", value=str(player['floor']), inline=True)
            embed.add_field(name="Level", value=str(player['level']), inline=True)
            embed.add_field(name="XP", value=str(player['xp']), inline=True)
            embed.set_footer(text="Use the buttons below to navigate")
            return embed

        elif self.current_page == 'stats':
            embed = discord.Embed(title=f"Stats for {self.user_id}", color=0x00ffcc)
            for stat, val in player['stats'].items():
                embed.add_field(name=stat, value=str(val), inline=True)
            embed.add_field(name="Level", value=player.get("level", 1), inline=True)
            embed.add_field(name="XP", value=player.get("xp", 0), inline=True)
            embed.add_field(name="Boss Defeated", value=str(player.get("boss_defeated", False)), inline=True)
            return embed

        elif self.current_page == 'inventory':
            embed = discord.Embed(title=f"Inventory of {self.user_id}", color=0x00ffcc)
            inventory = player.get("inventory", {})
            if not inventory:
                embed.description = "Your inventory is empty."
            else:
                for item, qty in inventory.items():
                    embed.add_field(name=item, value=f"Quantity: {qty}", inline=True)
            return embed

        elif self.current_page == 'progression':
            embed = discord.Embed(title=f"Progression of {self.user_id}", color=0x00ffcc)
            floor = player.get("floor", 1)
            boss_defeated = player.get("boss_defeated", False)
            embed.add_field(name="Current Floor", value=str(floor), inline=True)
            embed.add_field(name="Boss Defeated?", value=str(boss_defeated), inline=True)
            if floor in BOSSES:
                boss = BOSSES[floor]
                embed.add_field(name="Current Boss", value=boss["name"], inline=True)
                embed.add_field(name="Required Stats", value=", ".join(f"{k}: {v}" for k, v in boss["required_stats"].items()), inline=False)
            else:
                embed.description = "No boss on this floor."
            return embed

    @button(label="Main", style=discord.ButtonStyle.primary)
    async def main_button(self, interaction: discord.Interaction, button):
        self.current_page = 'main'
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @button(label="Stats", style=discord.ButtonStyle.secondary)
    async def stats_button(self, interaction: discord.Interaction, button):
        self.current_page = 'stats'
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @button(label="Inventory", style=discord.ButtonStyle.secondary)
    async def inventory_button(self, interaction: discord.Interaction, button):
        self.current_page = 'inventory'
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @button(label="Progression", style=discord.ButtonStyle.secondary)
    async def progression_button(self, interaction: discord.Interaction, button):
        self.current_page = 'progression'
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

@bot.command()
async def menu(ctx):
    view = SAOMenuView(ctx.author.id)
    await ctx.send(embed=view.get_embed(), view=view)

# Run the bot
keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
