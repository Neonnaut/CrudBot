import nextcord
from nextcord.ext import commands
import os
from dotenv.main import load_dotenv


def main():
    prefix = ["!!", "++"]
    intents = nextcord.Intents().all()
    intents.members = True
    description = "This is a CRUD bot."
    activity = None
    status = nextcord.Status.online
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or(*prefix), intents=intents, description=description, activity=activity, status=status, case_insensitive=True)
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            bot.load_extension("cogs." + f[:-3])
    load_dotenv()
    bot.run(os.getenv("TOKEN"))


if __name__ == '__main__':
    main()
