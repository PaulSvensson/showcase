#!/usr/bin/env python3

"""
Usage:
    photo-album <album-id>
"""

import requests
from docopt import docopt

ALBUMS = "https://jsonplaceholder.typicode.com/photos"


class PhotoAlbum:
    def __init__(self, url):
        self.url = url

    def fetch(self, album_id):
        response = requests.get(f"{self.url}?albumId={album_id}")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def format(album):
        return f"[{album['id']}] {album['title']}"

    @staticmethod
    def album_id():
        album_id = docopt(__doc__)["<album-id>"]
        try:
            return int(album_id)
        except (TypeError, ValueError) as exc:
            raise SystemExit(__doc__) from exc

    def main(self):
        for line in sorted(
            self.fetch(self.album_id()),
            key=lambda x: x["id"],
        ):
            print(self.format(line))


def main():
    PhotoAlbum(ALBUMS).main()


if __name__ == "__main__":
    main()
