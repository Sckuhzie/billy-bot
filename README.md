# billy-bot

Bot for BillyLand discord server

[Click here to add the bot to your server](https://discord.com/oauth2/authorize?client_id=1398970502843863130&scope=bot)

Use python 3.12

## Features

- Replies with generated insults when mentioned, replied to, or randomly.
- Randomly post "When the witcher ?".

### Commands

- `!ping` replies with "pong", username, and timestamp.
- `!insult <message>` generates a custom insult.
- `!enable_witcher <true|false>` – Toggle periodic `"When the witcher ?"` posts.
- **Global Variables**:
  - `!get_variables` – Show current values.
  - `!set_variable_float <key> <value>` – Update floats.

## Planned feature

- [x] Class to handle global variables
- [x] Randomly insult people
  - [ ] Add multiple system prompt to introduce private jokes in the answers
  - [ ] Benchmark other LLMs to see if some of them are better (Now, it answer always the same thing to the same message)
- [ ] Check modification in youtube playlist
- [x] When the witcher ???
  - [ ] Random when the witcher messages (images, maybe LLM generated ?)
  - [ ] Create polls to know when is the next witcher session

## Usefull links

[nvida-nim API](https://build.nvidia.com/)

[Dicord.py documentation](https://discordpy.readthedocs.io/en/latest/index.html)
