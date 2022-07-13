from optparse import Values
import gspread
from nextcord import Embed
import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta
import datetime as dt
import asyncio
from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

"""
async def getReply(bot, ctx):
    output = 'N'

    msg = await ctx.send("question")

    def check(m):
        if m.channel == ctx.channel and m.author.id == ctx.author.id:
            if m.reference is not None:
                if m.reference.message_id == msg.id:
                    return m.content

    msg = await msg.channel.fetch_message(msg.id)
    try:
        msg = await bot.bot.wait_for('message', timeout=60.0, check=check)
        output = msg.content
    except asyncio.TimeoutError:
        output = 'N'
        await ctx.channel.send("You ran out of time")

    return output


async def ynReaction(ctx, botID, question):
    timeNow = dt.datetime.now()
    timeDelta = dt.timedelta(minutes=1)
    answered = False
    output = 'N'

    msg = await ctx.send(question)
    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await msg.add_reaction('\N{CROSS MARK}')

    while not answered and timeNow + timeDelta >= dt.datetime.now():
        msg = await msg.channel.fetch_message(msg.id)
        for reaction in msg.reactions:
            async for user in reaction.users():
                # Make sure the reaction is not from the bot
                if user.id == botID:
                    pass
                elif user.id != ctx.author.id:
                    pass
                elif reaction.emoji == '\N{WHITE HEAVY CHECK MARK}':
                    answered = True
                    output = 'Y'

                elif reaction.emoji == '\N{CROSS MARK}':
                    answered = True
                    output = 'N'
    if not answered:
        output = 'N'
        await msg.channel.send('You ran out of time.')
    return output


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


async def sort_commandsheet(ctx, commandSheet):
    # Sort table alphabetically by key
    try:
        commandSheet.sort((1, 'asc'))
    except:
        await ctx.send("An error occured when sorting the sheet alphabetically.")
"""


class Scheme():
    def __init__(self, worksheet, key=None, fields=None):

        # Set workbook and commandsheet
        self.workbook = self.get_workbook()
        self.commandSheet = self.get_command_sheet(worksheet, self.workbook)

        # Set key array (key_value, key_row, key_header)
        if key != None and self.commandSheet != None:
            self.key = self.get_key(self.commandSheet, key)
        else:
            self.key = None

        # Set field array (field_values, field_rows, field_headers)
        if key != None:
            self.fields = self.get_fields(
                self.commandSheet, self.key, fields)  # list
        else:
            self.fields = None

        print(f'{self.workbook}\n{self.commandSheet}\n{self.key}\n{self.fields}')

        # self.key_row = 0
        # self.key_header = ""

        # self.field_values = ""
        # self.field_columns = ""
        # self.field_headers = ""

        # Check that the key requested does not already exist in keys

        # Check if the column input isn’t larger than the column header

        # Get new_key_value if exists

    def get_workbook(self):
        try:
            google_client = gspread.service_account_from_dict({
                "private_key": os.getenv("PRIVATE_KEY"),
                "client_email": os.getenv("CLIENT_EMAIL"),
                "token_uri": os.getenv("TOKEN_URI"),
            })
            workbook = google_client.open_by_key(
                os.getenv("SPREADSHEET_ID")
            )
        except:
            message = f"Could not access the workbook."
            workbook = None
            # await ctx.send(message)
        # await self.ctx.send('message')
        return workbook

    def get_command_sheet(self, worksheet, workbook):
        message = ""
        try:
            commandSheet = workbook.worksheet(worksheet)
        except:
            try:
                message += f"Could not access worksheet **{worksheet}** from workbook **{workbook.title}**.\n"
                vsheets = []
                for worksheet in workbook:
                    vsheets.append("**" + worksheet.title + "**")
                vsheets = ", ".join(vsheets)
                message += f"Let me fetch a list of worksheets you can access: {vsheets}."
            except:
                message += f"Could not access workbook."
            commandSheet = None
        # await ctx.send(message)
        return commandSheet

    def get_key(self, commandSheet, key):
        # Check if the key requested already exists in keys
        key_header = commandSheet.cell(1, 1).value
        keys = commandSheet.col_values(1)  # get the list of keys
        key_value = ''

        if key.casefold() in map(str.casefold, keys):
            key_row = keys.index(key.casefold())+1
            key_value = commandSheet.cell(key_row, 1).value
        else:
            key_row = None

        output = [key_value, key_header, key_row]
        return output

    def get_fields(self, commandSheet, key, fields):
        # Check if the key requested already exists in keys
        real_field_headers = commandSheet.row_values(1)
        real_field_headers.pop(0)
        if fields == None or len(fields) == 0:
            print(real_field_headers)
        else:
            for key in real_field_headers:
                for field in fields:
                    if key.casefold() == field.casefold():
                        print(key, field, real_field_headers.index(key)+2, "!!!")

        return "output"

    def sort_commandsheet(self):
        # Sort table alphabetically by key
        try:
            self.commandSheet.sort((1, 'asc'))
        except:
            pass
            # await ctx.send("An error occured when sorting the sheet alphabetically.")

    def create():
        pass

    def read():
        pass

    def update():
        pass

    def delete():
        pass

    def readRandom():
        pass

    def rename():
        pass


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

    @ commands.command()
    async def tester(self, ctx: commands.Context, worksheet: str, key: str, *fields: Optional[str]):
        """Create."""

        # dothing, worksheet, key, fields, new_key

        fields = list(fields)

        myScheme = Scheme(worksheet, key, fields)

        # print(myScheme.dothing, myScheme.worksheet,
        #      myScheme.key, myScheme.fields, myScheme.new_key)
        del myScheme

        # question = "This"

        # confirmation = await ynReaction(ctx, self.bot.user.id, question)
        # await ctx.send(confirmation)

        # myReply = await getReply(self, ctx)
        # await ctx.send(myReply)

    @ commands.command(name='create')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def create(self, ctx: commands.Context, worksheet: str, key: str, *fields):
        """Create."""

        # Get the worksheet to write to as commandSheet and check if none
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.row_values(1)
        # Get the input row
        input = (key,) + fields

        # check if at least one field entered
        if len(fields) == 0:
            await ctx.send(f"You have not entered any fields to update.")
            return

        # Check if the key requested already exists in keys
        keys = commandSheet.col_values(1)  # get the list of keys
        if key in keys:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** already exists.")
            return

        # Check if the columns requested are more than the columns in the header
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

        # Sort table alphabetically
        await sort_commandsheet(ctx, commandSheet)

        # Make a nice completion message
        dict = ""
        for i in range(0, len(input)):
            dict += " " + header[i] + ":" + "**" + input[i] + "**"
        await ctx.send(f"{ctx.message.author.name} created a new row;{dict}; in worksheet:**{commandSheet.title}**.")

    @ commands.command(name='read')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def read(self, ctx: commands.Context, worksheet: str, key: str):
        """Read."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.row_values(1)

        # Check if the key requested doesn't exist in keys and check if header
        keys = commandSheet.col_values(1)
        output = []
        if key in keys:
            output = commandSheet.row_values(keys.index(key)+1)
            if (keys.index(key)) == 0:
                dict = ""
                for i in range(0, len(header)):
                    dict += " " + header[i] + " "
                await ctx.send(f"This is the header row{dict}")
                return
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** wasn't found.")
            return

        # Make a nice completion message
        dict = ""
        for i in range(0, len(output)):
            dict += " " + header[i] + ":" + "**" + output[i] + "**"
        await ctx.send(f"Found information on the requested data: {dict} in worksheet:**{commandSheet.title}**")

    @ commands.command(name='update')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def update(self, ctx: commands.Context, worksheet: str, key: str, *fields):
        """Update."""

        print(fields)

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.row_values(1)
        # Get the input row
        input = (key,) + fields

        # check if at least one field entered
        if len(fields) == 0:
            await ctx.send(f"You have not entered any fields to update.")
            return

        # Check if the key requested doesn't exist in keys and check if header
        keys = commandSheet.col_values(1)
        output = 0
        if key in keys:
            # We need to say +1 because googlesheets idexes start at 1, not 0
            output = keys.index(key)+1
            if (keys.index(key)) == 0:
                dict = ""
                for i in range(0, len(header)):
                    dict += " " + header[i] + " "
                await ctx.send(f"This is the header row{dict}")
                return
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
            return

        # Check if the columns requested are more than the columns in the header
        if len(input) <= len(header):
            pass
        else:
            await ctx.send("The columns in your new row exceed the columns in the header row.")
            return

        # Update the cells of row at key
        try:
            for i in range(0, len(fields)):
                commandSheet.update_cell(output, i+2, fields[i])
        except:
            await ctx.send(f"Some error occured when updating the row.")

        # Make a nice completion message
        dict = ""
        for i in range(1, len(input)):
            dict += " " + header[i] + ":" + "**" + input[i] + "**"
        await ctx.send(f'{ctx.message.author.name} updated the data of {header[0]}:**{key}** to{dict} in worksheet:**{commandSheet.title}**.')

    @ commands.command(name='rename')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def rename(self, ctx: commands.Context, worksheet: str, key: str, new_key: str):
        """Rename."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.cell(1, 1).value

        # Check if the key exists in keys
        keys = commandSheet.col_values(1)
        output = 0
        if key in keys:
            output = keys.index(key)+1
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
            return

        # Check if the new key exists in keys
        keys = commandSheet.col_values(1)
        if new_key in keys:
            await ctx.send(f"**{new_key}** already exists.")
            return

        # Rename the cell of key with new key
        try:
            commandSheet.update_cell(output, 1, new_key)
        except:
            await ctx.send(f"Some error occured when updating the row.")
            return

        await sort_commandsheet(ctx, commandSheet)  # Sort table alphabetically

        # Make a nice completion message
        await ctx.send(f'{ctx.message.author.name} renamed {header}:**{key}** to **{new_key}** in worksheet:**{commandSheet.title}**.')

    @ commands.command(name='delete')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def delete(self, ctx: commands.Context, worksheet: str, key: str):
        """Delete."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.cell(1, 1).value

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

        await sort_commandsheet(ctx, commandSheet)  # Sort table alphabetically

        # Make a nice completion message
        await ctx.send(f'{ctx.message.author.name} deleted {header}:**{key}** in worksheet:**{commandSheet.title}**.')

    @ commands.command(name='update_fields')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def update_fields(self, ctx: commands.Context, worksheet: str, key: str, *fields):
        """Update fields."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.row_values(1)
        # Get the input row
        input = (key,) + fields

        for field in fields:
            pass

        # Check if the key requested doesn't exist in keys and check if header
        keys = commandSheet.col_values(1)
        output = 0
        if key in keys:
            # We need to say +1 because googlesheets idexes start at 1, not 0
            output = keys.index(key)+1
            if (keys.index(key)) == 0:
                dict = ""
                for i in range(0, len(header)):
                    dict += " " + header[i] + " "
                await ctx.send(f"This is the header row{dict}")
                return
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** doesn't exist.")
            return

        # Check if the columns requested are more than the columns in the header
        if len(input) <= len(header):
            pass
        else:
            await ctx.send("The columns in your new row exceed the columns in the header row.")
            return

        # Update the cells of row at key
        try:
            for i in range(0, len(fields)):
                commandSheet.update_cell(output, i+2, fields[i])
        except:
            await ctx.send(f"Some error occured when updating the row.")

        # Make a nice completion message
        dict = ""
        for i in range(1, len(input)):
            dict += " " + header[i] + ":" + "**" + input[i] + "**"
        await ctx.send(f'{ctx.message.author.name} updated the data of {header[0]}:**{key}** to{dict} in worksheet:**{commandSheet.title}**.')

    @ commands.command(name='read_fields')
    @ commands.cooldown(1, 5, commands.BucketType.user)
    async def read_fields(self, ctx: commands.Context, worksheet: str, key: str):
        """Read fields."""

        # Try and get the worksheet to write to as commandSheet
        commandSheet = await get_commandsheet(ctx, self.workbook, worksheet)
        if commandSheet == None:
            return

        # Get the header row
        header = commandSheet.row_values(1)

        # Check if the key requested doesn't exist in keys and check if header
        keys = commandSheet.col_values(1)
        output = []
        if key in keys:
            output = commandSheet.row_values(keys.index(key)+1)
            if (keys.index(key)) == 0:
                dict = ""
                for i in range(0, len(header)):
                    dict += " " + header[i] + " "
                await ctx.send(f"This is the header row{dict}")
                return
        else:
            await ctx.send(f"{commandSheet.cell(1,1).value}: **{key}** wasn't found.")
            return

        # Make a nice completion message
        dict = ""
        for i in range(0, len(output)):
            dict += " " + header[i] + ":" + "**" + output[i] + "**"
        await ctx.send(f"Found information on the requested data: {dict} in worksheet:**{commandSheet.title}**")


def setup(bot: commands.bot):
    bot.add_cog(Crud(bot))
