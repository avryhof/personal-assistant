from personal_assistant.classes import AssistantSkill
from skills.subsonic.subsonic_class import Subsonic


class SubsonicSkill(AssistantSkill):
    name = "Subsonic Skill"
    utterances = [
        "play <str:song> by <str:artist>",
        "play <str:song>",
        "play <str:genre> music",
        "play the album <str:album> by <str:artist>",
        "play the album <str:album>",
    ]
    params = ["album", "artist", "genre", "song"]

    def handle(self):
        ss = Subsonic()

        album = self.get_param("album")
        artist = self.get_param("artist")
        genre = self.get_param("genre")
        song = self.get_param("song")

        if song and not artist and "by" in song.lower():
            parts = song.lower().split("by")
            artist = parts[-1]
            song = "by".join(parts[0:-1])

        songs = []
        if song and artist:
            songs = ss.search(song, artist)
        elif song:
            songs = ss.search(song)

        if len(songs) > 0:
            the_song = songs[0]
            stream_url = ss.stream_url(the_song.get("id"))
            try:
                self.media.load(stream_url)
                self.media.play()
            except Exception as e:
                return False
            else:
                return True
        else:
            return False


class PauseMediaSkill(AssistantSkill):
    name = "Pause Media Skill"
    utterances = ["pause", "pause song", "pause media", "pause music"]

    def handle(self):
        self.media.pause()


class StopMediaSkill(AssistantSkill):
    name = "Pause Media Skill"
    utterances = ["stop", "stop song", "stop media", "stop music"]

    def handle(self):
        self.media.stop()
