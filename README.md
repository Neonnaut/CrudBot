# CrudBot

This is a WIP Discord Bot that manages a Google Spreadsheet workbook through discord commands.

## Setup

- In the [Discord developer portal](https://discord.com/developers/applications) create a new application. Under `Bot` select "add bot". Under `Bot` turn on PRESENCE INTENT, SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT
- Get an invite link for your bot under `QAuth2 > URL Generator`, with "bot" > "manage roles", "read messages/view channels", "send messages", "use external emojis" and "add reactions" permissions. Use the invite link and invite it to your server.
- Under `Bot`, copy the bot's token, you may have to reset it to do this. Save this token and don't share it with anyone. let's assume your token was `swordfish`.
- Create a file called ".env" in the main folder and set the contents of the file to `TOKEN=swordfish`. Save the file. Make sure the file is called ".env" and _not_ ".env.txt"
- Install python 3+. Make sure you have set Python to the system path.
- Install dependancies 
- Run the bot
- You might need to change `for f in os.listdir("./cogs"):` to an disfferent path
- You might need to change some setting in the developer portal

## TODO ?

- [ ] ...
- [ ] ...