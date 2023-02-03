from keep_alive import keep_alive
import openai
import discord
from discord.ext import commands
from discord import app_commands
import requests
import io
import os
import asyncio
from os import system
TOKEN = os.getenv("TOKEN")
openai_token = os.getenv("OPENAITOKEN")
openai.api_key = openai_token

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='#', intents=intents, activity = discord.Game(name="#howtouse for help"))


@bot.event
async def on_ready():
  print("Bot is up and Ready!")
  try:
    synced = await bot.tree.sync()
    print(f"Syned {len(synced)} command(s)")
  except Exception as e:
    print(e)


@bot.command()
async def howtouse(ctx):
  embed = discord.Embed(title = "This is how you use the bot", description = "Hi there! I am PGC's slave. Here are the available commands:\n"
  "#image: OpenAI's ChatGPT model image-alpha-001 will generate an image from your prompt.\n"
  "#gpt: OpenAI's ChatGPT will answer your prompts.\n"
  "#imagegen: Will generate images in a slightly different algorithm use this for research purposes only")
  await ctx.reply(embed = embed)


  
@bot.command()
async def gpt3(ctx, query):
  print(query)
  response = openai.Completion.create(
  		model="text-davinci-003",
  		prompt=query,
  		temperature=0.3,
  		max_tokens=4000,
  		top_p=1,
  		frequency_penalty=1,
  		presence_penalty=1,
  		stop=[" Human:", " AI:"]
		)
  text = response['choices'][0]['text']
  embed = discord.Embed(title = "Here is your answer", description = text)
  print (text)
  await ctx.reply(embed = embed)


@bot.command()
async def image(ctx, input1):
  print(input1)
  loading_message = await ctx.reply("***Generating image, please wait...***")
  response = openai.Image.create(
      prompt=input1,
      n= 1,
      size="1024x1024"
    )
  image_url = response['data'][0]['url']
  print(image_url)
  await ctx.reply(" " + image_url)



@bot.command()
async def imagegen(ctx, input2):
  print(input2)
  prompt = input2[7:]
  loading_message = await ctx.reply("***Generating image, please wait...***")
  api_url = "https://api.openai.com/v1/images/generations"
  api_key = {"Authorization": f"Bearer {openai.api_key}"}
  data = {"model": "image-alpha-001", "prompt": prompt, "num_images": 1, "size": "1024x1024", "response_format": "url"}
  response = requests.post(api_url, headers=api_key, json=data).json()
  if 'error' in response:
    error_message = response['error']['message']
    await ctx.reply(f"An error occurred: {error_message}")
  else:
    image_url = response['data'][0]['url']
    response = requests.get(image_url)
    image = response.content
    print(image_url)
    await ctx.reply(file=discord.File(io.BytesIO(image), 'image.jpg'))


@bot.command()
async def gpt(ctx, query1):
  print(query1)
  response = openai.Completion.create(
  		model="text-davinci-003",
  		prompt=query1,
  		temperature=0.3,
  		max_tokens=4000,
  		top_p=1,
  		frequency_penalty=1,
  		presence_penalty=1,
  		stop=[" Human:", " AI:"]
		)
  text = response['choices'][0]['text']
  max_length=450
  words = text.split()
  if len(words) > max_length:
    limited_text = " ".join(words[:max_length])
    rest_text = " ".join(words[max_length:])
    counter = rest_text.split()
    embed1 = discord.Embed(title = "First Part of answer", description = limited_text)
    print (text)
    embed = discord.Embed(title = "Second Part of answer", description = rest_text)
    print (text)
    print("this is the first part", limited_text)
    print("this is the first part", rest_text)
    first_message = await ctx.reply(embed = embed1)
    await ctx.reply(embed = embed)
  else:
    embed = discord.Embed(title = "Here is your answer", description = text)
    print (text)
    await ctx.reply(embed = embed)

@bot.tree.command(name = "gpt")
@app_commands.describe(ask_me_a_question = "Your question")
async def gpt(interaction: discord.Interaction, ask_me_a_question: str):
  print(ask_me_a_question)
  await interaction.response.defer()
  await asyncio.sleep(5)
  response = openai.Completion.create(
  		model="text-davinci-003",
  		prompt=ask_me_a_question,
  		temperature=0.3,
  		max_tokens=4000,
  		top_p=1,
  		frequency_penalty=1,
  		presence_penalty=1,
  		stop=[" Human:", " AI:"]
		)
  text = response['choices'][0]['text']
  max_length=450
  words = text.split()
  if len(words) > max_length:
    limited_text = " ".join(words[:max_length])
    rest_text = " ".join(words[max_length:])
    embed1 = discord.Embed(title = "First Part of answer", description = limited_text)
    print (text)
    embed = discord.Embed(title = "Second Part of answer", description = rest_text)
    print (text)
    print("this is the first part", limited_text)
    print("this is the first part", rest_text)
    first_message = await interaction.followup.send(embed = embed1)
    await interaction.followup.send(embed = embed)
  else:
    embed = discord.Embed(title = "Here is your answer", description = text)
    print (text)
    await interaction.followup.send(embed = embed)

@bot.tree.command(name = "image")
@app_commands.describe(generate_image = "Your image prompt")
async def image(interaction: discord.Interaction, generate_image: str):
  print(generate_image)
  await interaction.response.defer()
  await asyncio.sleep(5)
  response = openai.Image.create(
      prompt=generate_image,
      n= 1,
      size="1024x1024"
    )
  image_url = response['data'][0]['url']
  print(image_url)
  await interaction.followup.send(" " + image_url)

@bot.tree.command(name = "help")
async def help(interaction: discord.Interaction):
  embed = discord.Embed(title = "This is how you use the bot", description = "Hi there! I am PGC's slave. Here are the available commands:\n"
  "/image: OpenAI's ChatGPT model image-alpha-001 will generate an image from your prompt.\n"
  "/gpt: OpenAI's ChatGPT will answer your prompts.\n")
  await interaction.response.send_message(embed = embed)

keep_alive()
try:
  bot.run(TOKEN)
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
    system('kill 1')
