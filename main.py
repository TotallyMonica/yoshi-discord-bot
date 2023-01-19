#!/usr/bin/env python3

import discord
import json
import os
import sys
import datetime

class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        print(f'Message from {message.author}@{message.channel}: {message.content}')

        filename = f'{message.guild}.json'
        write_out = {}

        logged_message = {
            "sender":   str(message.author),
            "channel":  str(message.channel),
            "time":     message.created_at.strftime("%Y-%m-%d_%H:%M:%S"),
            "edits":    0,
            "contents": str(message.content)
        }

        if os.path.exists(filename):
            with open(filename) as filp:
                write_out = json.load(filp)

        write_out[str(message.id)] = logged_message
        print(write_out)

        with open(filename, 'w') as filp:
            filp.write(json.dumps(write_out))
    
    async def on_message_edit(self, before, after):
        print(f'Message from {before.author}@{before.channel} (ID {before.id}' +\
                    f' now says {after.content}')
        
        filename = f'{before.guild}.json'
        write_out = {}
        edited_message = {
            "edit_date":        after.edited_at.strftime("%Y-%m-%d_%H:%M:%S"),
            "new_body":         str(after.content)
        }

        if os.path.exists(filename):
            with open(filename) as filp:
                write_out = json.load(filp)

        edit_count = write_out[str(before.id)]['edits'] + 1

        write_out[str(before.id)]['edits']              = edit_count
        write_out[str(before.id)][f'edit_{edit_count}'] = edited_message
        print(write_out)

        with open(filename, 'w') as filp:
            filp.write(json.dumps(write_out))
    
    async def on_message_delete(self, message):
        print(f'Message from {message.author}@{message.channel} (ID {message.id}' +\
                    f' was deleted')
        
        filename = f'{message.guild}.json'
        write_out = {}
        deleted_time = datetime.datetime.now()

        if os.path.exists(filename):
            with open(filename) as filp:
                write_out = json.load(filp)

        write_out[str(message.id)]['deleted_time'] = deleted_time.strftime("%Y-%m-%d_%H:%M:%S")
        print(write_out)

        with open(filename, 'w') as filp:
            filp.write(json.dumps(write_out))

def load_secrets(path):
    secrets_template = {
        "token":           "",
        "application_id":  "",
        "public_key":      "",
        "client_id":       "",
        "client_secret":   ""
    }
    
    if not os.path.exists(path):
        with open(path, 'w') as filp:
            filp.write( json.dumps( secrets_template, indent=4 ) )
        return None
    
    with open(path) as filp:
        secrets = json.load(filp)
    
    return secrets

def main():
    secrets = load_secrets('secrets.json')

    if secrets == None:
        print('Please input your secrets in secrets.json')
        sys.exit(0)
    
    token          = secrets['token']
    application_id = secrets['application_id']
    public_key     = secrets['public_key']
    client_id      = secrets['client_id']
    client_secret  = secrets['client_secret']
    
    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot(intents=intents)
    bot.run(token)

if __name__ == '__main__':
    main()