<h1 align="center">
  <img src="static/cover.png" alt="subhound" width="200px">
  <br>
</h1>
 <p align="center"> Monitor and notify new subdomains found for a domain on Discord or/and Telegram. </p>

<p align="center">
<a href="https://twitter.com/sl4x0"><img src="https://img.shields.io/twitter/follow/sl4x0.svg?logo=twitter"></a>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
<a href="https://github.com/sl4x0/SubHound/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
<img src="https://img.shields.io/badge/Python-3.7-blue">
<img src="https://travis-ci.com/sl4x0/SubHound.svg?branch=master">
<img src="https://img.shields.io/librariesio/github/sl4x0/SubHound">
</p>

<p align="center">
  <a href="#installation">Installation</a> |
  <a href="#configuration">Configuration</a> |
  <a href="#usage">Usage</a> |
  <a href="#running-in-the-background">Running in the Background</a> |
  <a href="#references">References</a>
</p>

# Installation

```console
$ git clone https://github.com/exampleuser/subhound.git
$ cd subhound
$ pip install -r requirements.txt
```

# Configuration

```console
[discord]
webhook_url =https://discord.com/api/webhooks/12345678910/qwertyuiopasdfghjklzxcvbnm
channel_name = #channel-name
[telegram]
bot_token =123456789:qwertyuiopasdfghjklzxcvbnm
chat_id =123456789
```

- Open `config.ini` file with any Text-Editor and Replace your own Values
- Remember to see the <a href="#references">References</a> Section for Configure you own Webhook and API keys.



# Usage

To monitor a domain for new subdomains:

```console
$ python subhound.py -d example.com
```

This will retrieve the current subdomains for `example.com` and save them to two files in a subdirectory named `example.com_files`. It will then continuously monitor for new subdomains and send notifications to the Discord or/and Telegram channel when new subdomains are found.

By default, SubHound checks for new subdomains every 60 minutes. You can adjust this interval with the `-i` option:

```console
python subhound.py -d example.com -i 30
```
This will check for new subdomains every 30 minutes.

## Running in the Background
> This part for Bug Hunters and Security Reseachers

To run SubHound in the background so that it continues to run even if you close your VPS's SSH session, you can use the `tmux` command. `tmux` allows you to create and manage terminal sessions, and you can detach from a session to leave it running in the background.

To start a new `tmux` session:

```console
$ tmux new-session -s subhound
```

This will create a new `tmux` session named "subhound". You can now run the SubHound command as usual:

```console
$ python subhound.py -d example.com
```

To detach from the `tmux` session and leave it running in the background, press `Ctrl-b` and then `d`.

To reattach to the `tmux` session later:

```console
$ tmux attach -t subhound
```

This will reattach to the "subhound" session and allow you to view the output of the SubHound command.

## References

- [Creating Discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- [Creating Telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

# Credits
- Inspired by: [GitHound](https://github.com/tillson/git-hound) and [Sublert](https://github.com/yassineaboukir/sublert)
