import gspread
from nextcord import Embed
import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
import asyncio

import os
from dotenv import load_dotenv
load_dotenv()


async def get_commandsheet(ctx, workbook, worksheet):
    message = ""
    try:
        commandSheet = workbook.worksheet(worksheet)
    except:
        message += f"Could not access worksheet **{worksheet}** from workbook **{workbook.title}**.\n"
        try:
            vsheets = []
            for worksheet in workbook:
                vsheets.append("**" + worksheet.title + "**")
            vsheets = ", ".join(vsheets)
            message += f"Let me fetch a list of worksheets you can access: {vsheets}."
        except:
            message = f"Could not access workbook: **{workbook.title}** either."
        await ctx.send(message)
        commandSheet = None
    return commandSheet


class Crud(commands.Cog, name="Crud"):
    """Database."""

    COG_EMOJI = "🗃️"

    def __init__(self, bot):
        self.bot = bot

        google_client = gspread.service_account_from_dict({
            "private_key": os.getenv("PRIVATE_KEY"),
            "client_email": os.getenv("CLIENT_EMAIL"),
            "token_uri": os.getenv("TOKEN_URI"),
        })

        self.workbook = google_client.open_by_key(
            os.getenv("SPREADSHEET_ID")
        )
        print("loaded", self.__cog_name__)

    @commands.command(name='create')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def create(self, ctx: commands.Context, worksheet: str, key: str, *args):
        """Create."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)  # get the list of keys
        if key in keys:
            await ctx.send("It already exists.")
            return

        input = (key,) + args
        header = commandSheet.row_values(1)

        # Check if the columns requested are more than the header
        if len(input) <= len(header):
            pass
        else:
            await ctx.send("There are too many cols.")
            return

        # Append a new row
        try:
            commandSheet.append_row(input)
        except:
            await ctx.send(f"Some error occured when appending the row.")
            return

        # Sort table alphabetically by key
        try:
            commandSheet.sort((1, 'asc'))
        except:
            await ctx.send(f"Some error occured when sorting.")

        # Make a nice completion message
        dict = ""
        for i in range(0, len(input)):
            dict += ", " + header[i] + ":" + "\"" + input[i] + "\""
        await ctx.send(f"Row values{dict} have been added.")

    @commands.command(name='read')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def read(self, ctx: commands.Context, worksheet: str, key: str):
        """Read."""

        print(self.workbook.title)

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)
        output = []
        if key in keys:
            # We need to say +1 because googlesheets idexes start at 1, not 0
            output = commandSheet.row_values(keys.index(key)+1)
        else:
            await ctx.send(f"Thingy wasn't foundy")
            return

        #input = (key,) + args
        header = commandSheet.row_values(1)

        # Make a nice completion message
        dict = ""
        for i in range(0, len(output)):
            dict += ", " + header[i] + ":" + "\"" + output[i] + "\""
        await ctx.send(f"Something: {dict}")

    @commands.command(name='update')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def update(self, ctx: commands.Context, worksheet: str, key: str, *args):
        """Update."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)
        output = 0
        if key in keys:
            # We need to say +1 because googlesheets idexes start at 1, not 0
            output = keys.index(key)+1
        else:
            await ctx.send(f"Thingy wasn't foundy")
            return

        # Update the cells of row at key
        #commandSheet.update_cell(1, 1, 'Perro')

        input = (key,) + args
        header = commandSheet.row_values(1)

        # Make a nice completion message
        dict = ""
        for i in range(1, len(input)):
            dict += " " + header[i] + ": " + "**" + input[i] + "**"
        await ctx.send(f'**{ctx.message.author.name}** updated the column\'s of {header[0]}: **{key}** *to*{dict}.')

    @commands.command(name='rename')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rename(self, ctx: commands.Context, worksheet: str, key: str, new_key: str):
        """Rename."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)
        output = 0
        if key in keys:
            # We need to say +1 because googlesheets idexes start at 1, not 0
            output = keys.index(key)+1
        else:
            await ctx.send(f"Thingy wasn't foundy")
            return

        # Update the cell of key with new key
        commandSheet.update_cell(output, 1, new_key)

        # Sort table alphabetically by key
        try:
            commandSheet.sort((1, 'asc'))
        except:
            await ctx.send(f"Some error occured when sorting.")

        # Make a nice completion message
        header = commandSheet.cell(1, 1).value
        await ctx.send(f'**{ctx.message.author.name}** renamed {header} "{key}" to "{new_key}".')

    @commands.command(name='delete')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def delete(self, ctx: commands.Context, worksheet: str, key: str):
        """Delete."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)
        output = 0
        if key in keys:
            # We need to say +1 because googlesheets idexes start at 1, not 0
            output = keys.index(key)+1
        else:
            await ctx.send(f"Thingy wasn't foundy")
            return

        # Delete the row
        try:
            commandSheet.delete_row(output)
        except:
            await ctx.send(f"Some error occured when deleting the row.")

        # Sort table alphabetically by key
        try:
            commandSheet.sort((1, 'asc'))
        except:
            await ctx.send(f"Some error occured when sorting.")

        # Make a nice completion message
        header = commandSheet.cell(1, 1).value
        await ctx.send(f'**{ctx.message.author.name}** deleted {header} "{key}".')


def setup(bot: commands.bot):
    bot.add_cog(Crud(bot))
