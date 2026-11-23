import pytest

from playlist import Playlist, Song

A = Song(127, "Intro", "The xx")
B = Song(243, "Midnight City", "M83")
C = Song(180, "Short One", "Someone")


@pytest.fixture
def playlist():
    return Playlist("Focus", [A, B])


class TestSongDecorators:
    def test_dataclass_eq_and_repr(self):
        assert Song(10, "x", "y") == Song(10, "other", "fields")   # compare=False on title/artist
        assert "duration=10" in repr(Song(10, "x", "y"))

    def test_property_no_parentheses(self):
        assert A.minutes == "2:07"

    def test_classmethod_factory(self):
        assert Song.from_string("Intro - The xx - 2:07") == A

    def test_staticmethod_helper(self):
        assert Song.parse_duration("4:03") == 243

    def test_frozen(self):
        with pytest.raises(AttributeError):
            A.duration = 1


class TestPlaylistDunders:
    def test_len(self, playlist):
        assert len(playlist) == 2

    def test_iter(self, playlist):
        assert [s.title for s in playlist] == ["Intro", "Midnight City"]

    def test_getitem_index_and_slice(self, playlist):
        assert playlist[0] is A
        assert playlist[1:] == Playlist("x", [B])

    def test_contains(self, playlist):
        assert A in playlist and C not in playlist

    def test_add_returns_new_playlist(self, playlist):
        merged = playlist + Playlist("Chill", [C])
        assert len(merged) == 3 and len(playlist) == 2
        assert merged.name == "Focus + Chill"

    def test_eq(self, playlist):
        assert playlist == Playlist("Other name", [A, B])
        assert playlist != Playlist("Focus", [B, A])

    def test_bool(self):
        assert not Playlist("Empty")
        assert Playlist("One", [A])

    def test_str_and_repr(self, playlist):
        assert str(playlist) == "Focus (2 songs, 6 min)"
        assert repr(playlist).startswith("Playlist('Focus'")

    def test_sorted_uses_dataclass_order(self, playlist):
        merged = playlist + Playlist("Chill", [C])
        assert [s.title for s in sorted(merged)] == ["Intro", "Short One", "Midnight City"]
