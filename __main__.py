import settings
from mute_alsa import mute_alsa
from personal_assistant.classes import Bot


def main():
    mute_alsa()

    homebot = Bot(deaf=settings.DEAF, dumb=settings.DUMB, load_skills=True, log_level="console", wake_word="Speaker")
    # homebot = Bot(deaf=False, dumb=True, log_level="console")

    homebot.speak("Welcome to home bot. Your robotic voice companion.")

    while True:
        homebot.listen("Please command me ")

        if homebot.responded:
            homebot.speak("I heard: {}".format(homebot.heard))


if __name__ == "__main__":
    main()
