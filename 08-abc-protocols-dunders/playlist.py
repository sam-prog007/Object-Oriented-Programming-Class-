"""Slides 32-33: special methods make our class behave like a built-in type.

A Playlist that works with len(), for loops, [], in, +, ==, print() and sorted().
"""

from dataclasses import dataclass, field


@dataclass(order=True, frozen=True)
class Song:
    """@dataclass writes __init__, __repr__ and __eq__; order=True adds < > <= >=
    (comparing fields in order: duration first), frozen=True makes it hashable."""

    duration: int                       # seconds
    title: str = field(compare=False)
    artist: str = field(compare=False)

    @property
    def minutes(self) -> str:           # read like an attribute: song.minutes
        return f"{self.duration // 60}:{self.duration % 60:02d}"

    @classmethod
    def from_string(cls, text: str) -> "Song":
        """Factory method: 'Title - Artist - 3:45' -> Song."""
        title, artist, mmss = (part.strip() for part in text.split(" - "))
        return cls(cls.parse_duration(mmss), title, artist)

    @staticmethod
    def parse_duration(mmss: str) -> int:
        """Helper that needs neither self nor cls."""
        minutes, seconds = mmss.split(":")
        return int(minutes) * 60 + int(seconds)


class Playlist:
    def __init__(self, name: str, songs=None):
        self.name = name
        self._songs = list(songs or [])

    def add(self, song: Song) -> None:
        self._songs.append(song)

    def __len__(self):                  # len(playlist)
        return len(self._songs)

    def __iter__(self):                 # for song in playlist
        return iter(self._songs)

    def __getitem__(self, index):       # playlist[0], playlist[1:3]
        if isinstance(index, slice):
            return Playlist(self.name, self._songs[index])
        return self._songs[index]

    def __contains__(self, song):       # song in playlist
        return song in self._songs

    def __add__(self, other):           # playlist1 + playlist2 -> a NEW playlist
        return Playlist(f"{self.name} + {other.name}", self._songs + other._songs)

    def __eq__(self, other):            # same songs in the same order
        return isinstance(other, Playlist) and self._songs == other._songs

    def __bool__(self):                 # if playlist:
        return len(self) > 0

    def __str__(self):                  # print(playlist): for users
        total = sum(s.duration for s in self._songs)
        return f"{self.name} ({len(self)} songs, {total // 60} min)"

    def __repr__(self):                 # console / debugging: for developers
        return f"Playlist({self.name!r}, {self._songs!r})"


if __name__ == "__main__":
    a = Song.from_string("Intro - The xx - 2:07")
    b = Song.from_string("Midnight City - M83 - 4:03")
    c = Song(180, "Short One", "Someone")
    p = Playlist("Focus", [a, b])
    q = Playlist("Chill", [c])
    both = p + q
    print(both)                          # __str__
    print(len(both), a in both)          # __len__, __contains__
    for song in both:                    # __iter__
        print(" ", song.title, song.minutes)
    print(both[0].title, len(both[1:]))  # __getitem__ with index and slice
    print([s.title for s in sorted(both)])  # sorted by duration thanks to order=True
