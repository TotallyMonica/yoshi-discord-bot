#!/usr/bin/env python3

import discord
import json
import os
from datetime import datetime

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
        print(f"Message from {before.author}@{before.channel} (ID {before.id}) now says {after.content}")

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
        deleted_time = datetime.now()

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
    
    # async def on_reaction_add(self, reaction, user):
    #     print(user.name + " reated with", reaction.emoji.id)

    async def on_message(self, message):
        print(message.content)
        # Check if the sender is itself
        if message.author == self.user:
            return

        # Check if the message is a command
        elif message.content[0] == "!":
            split_message = message.content[1:].split(" ")

            # Get the roles of the sender

            with open("commands.json") as filp:
                commands = json.load(filp)

            for command in commands:
                if command == split_message[0]:
                    reply = commands[command]['response']

                    # TODO: Check for if the specified command has a section that needs to be replaced
                    #       e.g. <time> should be the time for Yoshi
                    
                    if '<' in reply and '>' in reply:
                        # TODO: Allow user to modify between 12h and 24h
                        if '<time>' in reply:
                            reply = reply.replace('<time>', datetime.now().strftime("%I:%M %p"))

                        # TODO: Allow user to modify date format, right now it's YYYY MON DD
                        if '<date>' in reply:
                            reply = reply.replace('<date>', datetime.now().strftime("%Y %h %d"))
                        
                        if '<args>' in reply:
                            reply = reply.replace("<args>", " ".join(split_message[1:]))
                        
                        if '<userlog>' in reply:
                            filename = f"{message.guild}.json"
                            with open(filename) as filp:
                                log = json.load(filp)
                            
                            for entry in log:
                                if log[entry]["sender"] == " ".join(split_message[1:]):
                                    reply += f"time: {log[entry]['time']}\nChannel: {log[entry]['channel']}\nmessage: {log[entry]['contents']}\n\n"

                    # Attept to check to see if the command requires a certain role.
                    try:
                        if commands[command]['allowed_roles']:
                            allowed = False
                            roles = [role.name.lower() for role in message.author.roles]

                            for role in roles:
                                if role in commands[command]['allowed_roles']:
                                    allowed = True
                                    break
                            
                            if not allowed:
                                reply = "Error: You cannot run this command"
                    
                    # It doesn't so escape out of it
                    except KeyError:
                        pass
                    
                    await message.channel.send(reply)
                    break

            print("Command detected!")

        # Check if the message contains a URL
        # If it does, delete it and ping the user
        # NOTE: There are significantly more schemas than HTTP or HTTPS.
        # In it's current method there's a chance there might be a false positive.
        # Look into a more robust while still clean method for checking for URLs
        elif "https://" in message.content.lower() or "http://" in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} you can't post URLs")
