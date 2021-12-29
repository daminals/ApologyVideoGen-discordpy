![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue)  ![github repo badge: Language](https://img.shields.io/badge/Language-Bash-181717?color=green)  ![github repo badge: Powered By](https://img.shields.io/badge/Powered%20by-FFMPEG-181717?color=Green)  ![github repo badge: Powered By](https://img.shields.io/badge/Powered%20by-gTTS-181717?color=red) ![github repo badge: Powered by](https://img.shields.io/badge/Powered%20by-Discord-181717?color=purple)
# ApologyVideoGenerator

_This repo is the discord bot version, which is self hosted, the GUI app version can be found [here](https://github.com/daminals/ApologyVideoGenerator/tree/MacApp) and the React app version can be found [here](https://github.com/daminals/ApologyVideoGenerator_Web)_

The greatest problem generation faces is the need to apologize for the horrible things we have done.
Youtube sensations do so many horrible things, and apologize in such a generic and uniform way, the apology video has become its own 'unique' genre (I say 'unique' because these videos are all practically the same)

In order to maximize efficiency, a combination of sad videos with a text to speech function could easily generate these videos, saving precious time.

To that end, this program aims to automate the creation of Apology videos, and it achieves its purpose!

[![](https://res.cloudinary.com/marcomontalbano/image/upload/v1594592001/video_to_markdown/images/youtube--Cjb45G58kk8-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://youtu.be/Cjb45G58kk8 "")

# Discord Bot

The generator is self-hosted, and asynchronously processes all requests to build apology videos. It utilizes google's text to speech API, FFmpeg, and discord's API to put together an effective and functional bot.

# Features

Because this bot is self-hosted, it has the capacity for dynamic improvements, utilizing as many videos and audios as the server has storage for, and no script needs to be edited to accommodate for changes.

The bot works asynchronously rather than engaging in blocking (as it used to) due to self-hosting

# Next Steps

<details>
<summary>API Integration</summary>

Rather than have each separate instance of the script.py function, I would like to host the React app and use the flask backend as an API that can accept script-building requests, minimizing repeated code and allowing for script updates that immediately affect all Apology Video Generator ports
</details>
<details>
<summary>Store Assets Centrally</summary>

Store Assets in centralized folder accessible to all Apology Video ports hosted on the server
</details>
<details>
<summary>More RAM</summary>

More RAM would allow the the bot to be more scalable and process way more apology videos at once
</details>

# What I Learned

<details>
<summary> Heroku Integration </summary>

Before self-hosting this project, the apology video generator was hosted on heroku for over year and a half. Here I learned how to add external buildpacks to make the project compatible with FFmpeg, had to work around heroku's 500mb memory limit while maintaining a functional app, and not using concurrency as I only had access to one worker. I learned a lot about external hosts from this experience, and working with Heroku's slugs, environment keys, and accessing my code from an external service, and this knowledge was later put to use when I created my own hosting server

</details>

<details>
<summary> FFmpeg </summary>

Through this project I discovered FFmpeg, which I have been using ever since. Previously all my small video editing would have to be done through Adobe Premiere Pro, and video compression done by online websites with limits. After learning and becoming experienced with FFmpeg, it changed the way I did video processing forever. Every small cut or music addition and compression can be done through the command line, which is simply incredible.

</details>

# Installation
```
$ git clone https://github.com/daminals/ApologyVideoGen-discordpy.git
$ cd ApologyVideoGen-discordpy
$ touch .env
$ echo TOKEN=\'YOUR_DISCORD_BOT_TOKEN\' >> .env
$ ./build
```