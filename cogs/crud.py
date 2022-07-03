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

        # Get the worksheet to write to as commandSheet and check if none
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)  # get the list of keys
        if key in keys:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** already exists.")
            return

        # Check if the columns requested are more than the columns in the header
        input = (key,) + args
        header = commandSheet.row_values(1)
        if len(input) <= len(header):
            pass
        else:
            await ctx.send("The columns in your new row exceed the columns in the header row.")
            return

        # Append a new row
        try:
            commandSheet.append_row(input)
        except:
            await ctx.send("Some error occured when appending the row.")
            return

        # Sort table alphabetically by key
        try:
            commandSheet.sort((1, 'asc'))
        except:
            await ctx.send(f"Some error occured when sorting the sheet alphabetically.")

        # Make a nice completion message
        dict = ""
        for i in range(0, len(input)):
            dict += " " + header[i] + ":" + "**" + input[i] + "**"
        await ctx.send(f"{ctx.message.author.name} created a new row;{dict}; in worksheet:**{commandSheet.title}**.")

    @commands.command(name='read')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def read(self, ctx: commands.Context, worksheet: str, key: str):
        """Read."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return
        else:
            pass

        # Check if the key requested doesn't exist in keys
        keys = commandSheet.col_values(1)
        output = []
        if key in keys:
            output = commandSheet.row_values(keys.index(key)+1)
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
            return

        #input = (key,) + args
        header = commandSheet.row_values(1)

        # Make a nice completion message
        dict = ""
        for i in range(0, len(output)):
            dict += " " + header[i] + ":" + "**" + output[i] + "**"
        await ctx.send(f"Found information on the requested data: {dict} in worksheet:**{commandSheet.title}**")

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
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
            return

        # Check if the columns requested are more than the columns in the header
        input = (key,) + args
        header = commandSheet.row_values(1)
        if len(input) <= len(header):
            pass
        else:
            await ctx.send("The columns in your new row exceed the columns in the header row.")
            return

        # Update the cells of row at key
        try:
            for i in range(0, len(args)):
                commandSheet.update_cell(output, i+2, args[i])
        except:
            await ctx.send(f"Some error occured when updating the row.")

        input = (key,) + args
        header = commandSheet.row_values(1)

        # Make a nice completion message
        dict = ""
        for i in range(1, len(input)):
            dict += " " + header[i] + ":" + "**" + input[i] + "**"
        await ctx.send(f'{ctx.message.author.name} updated the data of {header[0]}:**{key}** to{dict} in worksheet:**{commandSheet.title}**.')

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
            output = keys.index(key)+1
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
            return

        # Rename the cell of key with new key
        try:
            commandSheet.update_cell(output, 1, new_key)
        except:
            await ctx.send(f"Some error occured when updating the row.")

        # Sort table alphabetically by key
        try:
            commandSheet.sort((1, 'asc'))
        except:
            await ctx.send(f"Some error occured when sorting.")

        # Make a nice completion message
        header = commandSheet.cell(1, 1).value
        await ctx.send(f'{ctx.message.author.name} renamed {header}:**{key}** to **{new_key}** in worksheet:**{commandSheet.title}**.')

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
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
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
        await ctx.send(f'{ctx.message.author.name} deleted {header}:**{key}** in worksheet:**{commandSheet.title}**.')


def setup(bot: commands.bot):
    bot.add_cog(Crud(bot))
