# Yoshi Discord Bot

This is, quite literally, the discord bot used in [my community discord server](https://discord.gg/PktAw7N) (Invites currently closed due to poor maintenance of it)

## Requirements

[Python 3.8+](https://www.python.org/downloads/)

[discord.py](https://pypi.org/project/discord.py/)

## Setup

```bash
pip install discord
./main.py
# At this point, edit the file secrets.json that was generated with the appropriate tokens
./main.py
```

As of right now, all fields are required. (See To-do)

## To-do

- Audit bot allowing purging of old logs through the server its on
- Commands
  - Allow use of custom prefixes
- ~~URL detection~~ Implemented 1/18/2023
- Allow bot secrets to be provided via `stdin` or as arguments
- Configuration wizard
- Allow bot secrets to be optional whenever possible
