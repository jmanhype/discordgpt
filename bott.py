import discord
from discord.ext import commands
import openai
import random
from openai import ChatCompletion

class DiscordBot(commands.Bot):
    def __init__(self, token: str, openai_token: str):
        intents = discord.Intents.all()
        intents.messages = True
        super().__init__(command_prefix="!", intents=intents)
        self.token = token
        self.openai_token = openai_token
        self.welcome_messages = ["Welcome aboard, {member_name}!",
                                 "Glad you've joined us, {member_name}!",
                                 "Hey there, {member_name}! Welcome!"]

        openai.api_key = self.openai_token

        # Define the commands
        @self.command(help="Guess a random number between 1 and 10.")
        async def guess(ctx, number: int):
            random_number = random.randint(1, 10)
            if number == random_number:
                await ctx.send(f"Congratulations, {ctx.author.name}! You guessed the number! It was {random_number}!")
            else:
                await ctx.send(f"Sorry, {ctx.author.name}. The correct number was {random_number}. Better luck next time!")

        @self.command(help="Warn a user.")
        async def warn(ctx, member: discord.Member, *, reason=None):
            warning_message = f"You have been warned by {ctx.message.author.name}: {reason}"
            await member.send(warning_message)

        @self.command(help="Announce a message.")
        async def announce(ctx, *, announcement):
            channel = discord.utils.get(ctx.guild.channels, name = 'general') 
            await channel.send(announcement)

        @self.command(help="Resolve an issue.")
        async def resolve(ctx, *, issue):
            resolution = f"The issue: '{issue}' is now resolved. Please contact the moderators for further clarification."
            await ctx.send(resolution)

        @self.command(name="airesponse", help="Get a response from OpenAI based on conversation context.")
        async def airesponse(ctx):
            print("airesponse command was called")  # ADDED: Debug print
            model = "gpt-3.5-turbo"
            conversation_history = []
            async for message in ctx.channel.history(limit=25):
                conversation_history.append({
                    'role': 'system' if message.content.startswith('!') else ('user' if message.author == ctx.author else 'assistant'),
                    'content': message.content
                })

            response = ChatCompletion.create(
                model=model,
                messages=conversation_history,
            )
            ai_message = response['choices'][0]['message']['content']
            await ctx.reply(ai_message)

    def run(self):
        super().run(self.token)

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_member_join(self, member: discord.Member):
        await self.greetUser(member)

    async def on_message(self, message):
        print(f"Received message: {message.content}")  # ADDED: Debug print
        if "bot" in message.content.lower() and not message.author.bot:
            await self.spontaneous_ctx_reply(message)

        await self.process_commands(message)

    async def spontaneous_ctx_reply(self, message):
        model = "gpt-3.5-turbo"
        conversation_history = []
        async for msg in message.channel.history(limit=25):
            conversation_history.append({
                'role': 'system' if msg.content.startswith('!') else 'assistant' if msg.author == self.user else 'user',
                'content': msg.content
            })

        response = ChatCompletion.create(
            model=model,
            messages=conversation_history,
        )
        ai_message = response['choices'][0]['message']['content']
        await message.channel.send(ai_message)

    async def greetUser(self, member: discord.Member):
        welcome_message = random.choice(self.welcome_messages).format(member_name=member.name)
        await member.send(welcome_message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"Error occurred: {error}")  # ADDED: Debug print
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(f"Command not found. Use !help to see a list of available commands.")
        else:
            await ctx.send(f"There was an error with your request: {str(error)}")  # CHANGED: More detailed error message

bot = DiscordBot("MTEzMDI1Mjk4MzMyMjU0NjI2Nw.Gvfd0Y.M_lNeC00_GFH93ySGZiskkPRMuY-E4865lWh2s", "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")
bot.run()
