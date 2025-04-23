import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="tms ", intents=intents)

# CONFIGURATION
selected_channel_id = 123456789012345678  # Replace with your selected channel ID
bypass_role_name = "bypass.exe"

# In-memory databases
balances = {}
unlimited_users = set()

# Check for correct channel
async def is_valid_channel(ctx):
    return ctx.channel.id == selected_channel_id

# Check if user has bypass role
def has_bypass_role(ctx):
    return any(role.name == bypass_role_name for role in ctx.author.roles)

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

@bot.command()
async def send(ctx, amount: int, member: discord.Member):
    if not await is_valid_channel(ctx): return
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)

    if sender_id in unlimited_users:
        balances[receiver_id] = balances.get(receiver_id, 0) + amount
        await ctx.send(f"{ctx.author.mention} ne {member.mention} ko {amount} TMS POINTS diye.")
        return

    if balances.get(sender_id, 0) >= amount and amount > 0:
        balances[sender_id] -= amount
        balances[receiver_id] = balances.get(receiver_id, 0) + amount
        await ctx.send(f"{ctx.author.mention} ne {member.mention} ko {amount} TMS POINTS diye.")
    else:
        await ctx.send("Insufficient balance ya invalid amount.")

@bot.command()
async def balance(ctx):
    if not await is_valid_channel(ctx): return
    user_id = str(ctx.author.id)
    if user_id in unlimited_users:
        await ctx.send(f"{ctx.author.mention} ka balance: Unlimited TMS POINTS")
    else:
        await ctx.send(f"{ctx.author.mention} ka balance: {balances.get(user_id, 0)} TMS POINTS")

@bot.command()
async def bet(ctx, amount: int):
    if not await is_valid_channel(ctx): return
    user_id = str(ctx.author.id)

    if amount < 1 or amount > 100:
        await ctx.send("Bet amount should be between 1 and 100.")
        return

    if user_id in unlimited_users:
        if random.random() < 0.1:
            await ctx.send(f"{ctx.author.mention} jeet gaye! Aapko {int(amount * 1.5)} TMS POINTS mile.")
        else:
            await ctx.send(f"{ctx.author.mention} haar gaye. Better luck next time!")
        return

    if balances.get(user_id, 0) < amount:
        await ctx.send("Insufficient balance for betting.")
        return

    balances[user_id] -= amount
    if random.random() < 0.1:
        winnings = int(amount * 1.5)
        balances[user_id] += winnings
        await ctx.send(f"{ctx.author.mention} jeet gaye! Aapko {winnings} TMS POINTS mile.")
    else:
        await ctx.send(f"{ctx.author.mention} haar gaye. Better luck next time!")

@bot.command()
@commands.has_role(bypass_role_name)
async def unlimited(ctx):
    if not await is_valid_channel(ctx): return
    unlimited_users.add(str(ctx.author.id))
    await ctx.send(f"{ctx.author.mention} ko ab Unlimited TMS POINTS mil gaye hai!")

# Run the bot
bot.run("YOUR_BOT_TOKEN")  # Replace with your actual bot token
