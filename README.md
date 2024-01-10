# [Church4u Youtube Uploader Bot](@church4u_upload_bot)

> Simple [Telegram Bot](https://core.telegram.org/bots "Telegram Bots") to Upload videos to [Youtube](https://youtube.com "YouTube") written in Python3.11.

### Contents

- [Info](#info)
- [Libraries Used](#libraries-used)
- [Setup](#setup)
- [Status](#status)
- [Special Notes](#special-notes)
- [Screenshots](#screenshots)
- [Video Tutorial](#video-tutorial)
- [Contact](#contact)
- [License](#license)

### Info

This is a simple hobby project which I was really curious about to implement. This is a Telegram bot which uses [Youtube Data API v3](https://developers.google.com/youtube/v3/ "Youtube Data API v3") to upload videos to Youtube.
Inspared by [odysseusmax/utube](https://github.com/odysseusmax/utube)

### Libraries Used

- [Pyrogram](https://github.com/pyrogram/pyrogram "Pyrogram")
- [Google Client API](https://github.com/googleapis/google-api-python-client "Google Client API")

**Environment Variables**

- `BOT_TOKEN`(Required) - Get your bot token from [Bot Father](https://tx.me/BotFather "Bot Father").
- `API_ID`(Required) - Your telegram api id, get from [Manage Apps](https://my.telegram.org).
- `API_HASH`(Required) - Your telegram api hash, get from [Manage Apps](https://my.telegram.org).
- `BOT_OWNER`(Required) - Telegram id of bot owner.
- `DEBUG` (optional) - Whether to set logging level to DEBUG. If set logging will be set to DEBUG level, else INFO level.

**Run bot**

Lets run our bot for the first time!

```bash
$ python3 -m bot
```

If you did everything correctly, the bot should be running. Go do `/start` to see if the bot is live or not. Follow the instructions provided by bot to setup authorisation and to start uploading.

### Special notes

- With the Youtube Data API you are awarded with 10,000 points of requests. For one video upload it costs 1605 points, regardless of file size, which calculates to about 6 uploads daily. Once you have exhausted your daily points, you have to wait till daily reset. Resets happens at 0:00 PST, i.e. 12:30 IST. So make your uploads count.

- Uploading copyright contents will leads to immediate blocking of the video.

### License

Code released under [GNU General Public License v3.0](LICENSE).
