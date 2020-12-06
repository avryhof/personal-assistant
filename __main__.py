from bot_class import Bot
from mute_alsa import mute_alsa


def main():
    mute_alsa()

    homebot = Bot(deaf=True, dumb=True, log_level="console")
    # homebot = Bot(deaf=False, dumb=True, log_level="console")

    homebot.speak("Welcome to home bot. Your robotic voice companion.")

    while True:
        homebot.listen("Please command me ")

        if homebot.responded:
            homebot.speak("I heard: {}".format(homebot.heard))


if __name__ == "__main__":
    main()
