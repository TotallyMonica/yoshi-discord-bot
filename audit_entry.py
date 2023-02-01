import bots
import sys
import json
import os
import discord

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

    audit = bots.Audit(intents=intents)
    audit.run(token)

if __name__ == "__main__":
    main()