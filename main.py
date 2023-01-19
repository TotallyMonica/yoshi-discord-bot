#!/usr/bin/env python3

import discord
import json
import os
import sys

def main():
    secrets_template = {
        "token":           "",
        "application_id":  "",
        "public_key":      ""
    }
    
    if not os.path.exists('secrets.json'):
        print('Please input your secrets in secrets.json')
        with open('secrets.json', 'w') as filp:
            filp.write( json.dumps( secrets_template, indent=4 ) )
        sys.exit(0)
    
    with open('secrets.json') as filp:
        secrets = json.load(filp)

    print(secrets)

if __name__ == '__main__':
    main()