# billy-bot

Bot made for a private discord server

[Click here to add the bot to your server](https://discord.com/oauth2/authorize?client_id=1398970502843863130&scope=bot)

Made with python 3.12.12

## Features

- Replies with generated insults when mentioned, replied to, or randomly.
- Compare the current state of youtube playlist with a former saved state.

### Commands

- `!ping`
- `!save_playlist <playlist_name>` – Save the current state of a playlist (Erases previous state).
- `!playlist_diff <playlist_name>` – Show the diff between the current state of a playlist and the saved one.
- **Global Variables**:
  - `!get_variables` – Show current values.
  - `!set_variable_float <key> <value>` – Update floats.

## Planned features

- [x] Randomly insult people
  - [x] Proper reply to messages
  - [ ] Check for message stack only two messages (discord api limitation ?) (fetch the message from their ID)
  - [ ] Add multiple system prompt to introduce private jokes in the answers
  - [ ] Benchmark other LLMs to see if some of them are better (Now, it answer always the same thing to the same message)

## Usefull links

[nvida-nim API](https://build.nvidia.com/)

[Dicord.py documentation](https://discordpy.readthedocs.io/en/latest/index.html)
