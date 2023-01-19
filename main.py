#!/usr/bin/env python3

import discord
import json
import os
import sys
import datetime

class Audit(discord.Client):
    async def on_ready(self):
        print(f"Auditor logged on as {self.user}!")
    
    # Log when a message was sent
    async def on_message(self, message):
        print(f"Message from {message.author}@{message.channel}: {message.content}")

        filename = f"{message.guild}.json"
        write_out = {}

        # Build the dict for the message
        logged_message = {
            "sender":   str(message.author),
            "channel":  str(message.channel),
            "time":     message.created_at.strftime("%Y-%m-%d_%H:%M:%S"),
            "edits":    0,
            "contents": str(message.content)
        }

        # Check if the file exists and, if it does, work off of that.
        if os.path.exists(filename):
            with open(filename) as filp:
                write_out = json.load(filp)

        # Append the message to the log, then write it out.
        write_out[str(message.id)] = logged_message
        with open(filename, "w") as filp:
            filp.write(json.dumps(write_out))
    
    # Log when a message was edited.
    async def on_message_edit(self, before, after):
        print(f"Message from {before.author}@{before.channel} (ID {before.id}" +\
                    f" now says {after.content}")
        
        filename = f"{before.guild}.json"
        write_out = {}

        # Build format for edited message
        edited_message = {
            "edit_date":        after.edited_at.strftime("%Y-%m-%d_%H:%M:%S"),
            "new_body":         str(after.content)
        }

        # Check if there is an existing log to work off of.
        if os.path.exists(filename):
            with open(filename) as filp:
                write_out = json.load(filp)

        edit_count = write_out[str(before.id)]["edits"] + 1

        # Adjust the log appropriately for the edited message, then write out
        write_out[str(before.id)]["edits"]              = edit_count
        write_out[str(before.id)][f"edit_{edit_count}"] = edited_message
        with open(filename, "w") as filp:
            filp.write(json.dumps(write_out))
    
    # Log when a message was deleted
    # NOTE: Due to limitations of discord.py (might be the Discord API as a whole), the bot is unable to log who deleted a message
    async def on_message_delete(self, message):
        print(f"Message from {message.author}@{message.channel} (ID {message.id})" +\
                    f" was deleted")
        
        filename = f"{message.guild}.json"
        write_out = {}

        # Homebrew method for checking when a message was deleted. May not be entirely accurate.
        deleted_time = datetime.datetime.now()

        # Check if there is an existing log to work off of.
        if os.path.exists(filename):
            with open(filename) as filp:
                write_out = json.load(filp)

        # Modify log to note when a message was deleted, then write out.
        write_out[str(message.id)]["deleted_time"] = deleted_time.strftime("%Y-%m-%d_%H:%M:%S")
        with open(filename, "w") as filp:
            filp.write(json.dumps(write_out))

# Chat bot that members interact with
class Chat(discord.Client):
    async def on_ready(self):
        print(f"Chatbot logged on as {self.user}!")

    async def on_message(self, message):
        # Check if the sender is itself
        if message.author == self.user:
            return
        
        # Check if the message is a command
        elif message.content[1] == "!":
            with open("command.json") as filp:
                message.content.split(" ")
                commands = json.load(filp)
        
        # Check if the message contains a URL
        # If it does, delete it and ping the user
        # NOTE: There are significantly more schemas than HTTP or HTTPS.
        # In it's current method there's a chance there might be a false positive.
        # Look into a more robust while still clean method for checking for URLs
        elif "https://" in message.content.lower() or "http://" in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} you can't post URLs")

def load_secrets(path):
    secrets_template = {
        "token":           "",
        "application_id":  "",
        "public_key":      "",
        "client_id":       "",
        "client_secret":   ""
    }
    
    if not os.path.exists(path):
        with open(path, "w") as filp:
            filp.write( json.dumps( secrets_template, indent=4 ) )
        return None
    
    with open(path) as filp:
        secrets = json.load(filp)
    
    return secrets

def main():
    permissions = 2147494976
    secrets = load_secrets("secrets.json")

    if secrets == None:
        print("Please input your secrets in secrets.json")
        sys.exit(0)
    
    # Import the secrets
    # TODO: Allow these to be possibly taken as arguments
    # TODO: Allow all but the strictly necessary to be optional
    token          = secrets["token"]
    application_id = secrets["application_id"]
    public_key     = secrets["public_key"]
    client_id      = secrets["client_id"]
    client_secret  = secrets["client_secret"]

    print("If you haven't already, invite me to your server using the following link:")
    print(f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot")

    intents = discord.Intents.default()
    intents.message_content = True

    audit = Audit(intents=intents)
    audit.run(token)

if __name__ == "__main__":
    main()