import pprint
import random
import string

import requests

from model_helpers import md5
from settings import SUBSONIC_URL, SUBSONIC_USER, SUBSONIC_PASSWORD
from subsonic.exceptions import InvalidCriteria


class Subsonic(object):
    app_name = "Subsonic Class"
    api_version = "1.16.1"
    debug = False

    endpoint = None
    username = None
    password = None

    salt = None
    encoded_password = None

    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", False)

        self.endpoint = kwargs.get("url", SUBSONIC_URL)
        self.username = kwargs.get("user", SUBSONIC_USER)
        self.password = kwargs.get("password", SUBSONIC_PASSWORD)

        salt_length = random.randint(6, 12)
        self.salt = "".join(
            random.choice(string.ascii_letters + "1234567890_")
            for i in range(salt_length)
        )

        salted_password = self.password + self.salt
        self.encoded_password = md5(salted_password)

    def _api_call(self, resource, data=False):
        api_data = dict(
            u=self.username,
            t=self.encoded_password,
            s=self.salt,
            v=self.api_version,
            c=self.app_name,
            f="json",
        )

        if isinstance(data, dict):
            for k, v in data.items():
                api_data[k] = v

        url = "{}/rest/{}.view".format(self.endpoint, resource)

        if self.debug:
            print(url)
            pprint.pprint(api_data)

        resp = requests.get(url, params=api_data)

        if self.debug:
            print(resp)

        return resp.json()

    def stream(self, song_id):
        return self._api_call("download", dict(id=song_id))

    def get_random_songs(self):
        search_result = self._api_call("getRandomSongs")

        return search_result.get("subsonic-response", {}).get("randomSongs", {}).get("song", [])

    def ping(self):
        return self._api_call("ping")

    def now_playing(self):
        return self._api_call("getNowPlaying")

    def search(self, query, **kwargs):
        # Default to searching everything
        resource = "search2"
        result_key = "searchResult2"
        result_type = False

        data = dict(query=query)

        if "id3" in kwargs:
            # If id3=True is passed as a keyword argument, we search in id3 tags rather than all inferred data
            if kwargs.pop("id3", False):
                resource = "search3"
                result_key = "searchResult3"

        if "result_type" in kwargs:
            # We can limit result type to: album, artist, or song
            result_type = kwargs.pop("result_type")

            if result_type not in ["album", "artist", "song"]:
                raise InvalidCriteria("result_type must be album, artist, or song")

        if kwargs:
            data.update(kwargs)

        result = self._api_call(resource, data)
        search_results = result.get("subsonic-response", {}).get(result_key)

        if isinstance(result_type, str):
            search_results = search_results.get(result_type)

        return search_results

    def stream(self, **data):
        return self._api_call("stream", data)


# ss = Subsonic(debug=True)
ss = Subsonic()

# result = ss.ping()
# result = ss.search("Disturbed", result_type="artist", id3=True)
# result = ss.now_playing()
result = ss.get_random_songs()

pprint.pprint(result)
