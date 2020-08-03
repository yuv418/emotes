# emotes

Ever want to easily insert commonly used emojis that don't exist in Unicode ![:thonk:](assets/thonk.png)? Or animated emojis? Or stickers on chat platforms
that don't support them?

Well, `emotes` will do that for you (when we finish programming it). It will be an API so you can insert these emojis easily without having to tediously search for them. Just `GET /thonk` instead of searching Google (or Bing or your favourite search engine). Or upload your own emojis. Or `emotes` will fetch your emote for you from one of our supported providers.


## Developing

You can develop it in a Python venv. To get started, run these commands.
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

You also need a valid MySQL/MariaDB database to develop emotes. Installing that
is out of the scope of this readme. In addition, you will need a valid Twitch client ID if you want to develop the Twitch integration.
Next, copy the `.flaskenv.sample` to `.flaskenv`.
```bash
cp .flaskenv.sample .flaskenv
```

With your flaskenv, fill in the variables with their appropriate values. You should also probably set FLASK_DEBUG to 1 if you are developing the application,
otherwise Flask will not reload every time you make a change in the files. Then, you can run the application with `flask run`.

The application "installer" should print out an admin API key that you can use later. You can now develop the program as normal.

## Installing

It is fairly easy to install emotes because it has a Dockerfile. If you aren't using Docker, you will have to do these things manually, and that is not in the scope of this README for now.

Run `docker build . -t <your tag here>` with your tag. In my case it's for a private Docker registry, so I use `my.domain.here/emotes:latest`. You can then push it to your registry,
(with `docker push <your tag here>`) and run the image as you would any other Docker image. Make sure to set your environment variables accordingly if you're using Kubernetes or Docker-compose or the like.

## Features

Things `emotes` can do right now:

- [x] Display local emotes from the `emotes` directory
- [x] Display emotes from an external source like ~~Discord~~ or Twitch
- [x] Display user-uploaded emotes
- [ ] Simple user interface to wrap over the API
- [x] Deployment and publicly accessible instance

Created by [Lord Steggy](https://github.com/rfblock) and [cdknight](https://github.com/cdknight).
