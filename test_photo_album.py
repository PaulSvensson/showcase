import pytest
import requests

from photo_album import PhotoAlbum

# pylint: disable=redefined-outer-name


@pytest.fixture
def sample_albums():
    return [
        {"id": 2, "title": "album two"},
        {"id": 1, "title": "album one"},
        {"id": 3, "title": "album three"},
    ]


@pytest.fixture
def tested_albums():
    return PhotoAlbum("MOCK")


@pytest.fixture
def get_mock(mocker, response_mock):
    get = mocker.patch("requests.get")
    get.return_value = response_mock
    return get


@pytest.fixture
def response_mock(mocker):
    response = mocker.Mock()
    response.raise_for_status = lambda: requests.Response.raise_for_status(response)
    return response


@pytest.fixture
def fetch_mock(mocker, sample_albums):
    fetch = mocker.patch("photo_album.PhotoAlbum.fetch")
    fetch.return_value = sample_albums
    return fetch


def test_fetch_ok(get_mock, response_mock, tested_albums, sample_albums):
    response_mock.json = lambda: sample_albums
    response_mock.status_code = 200

    actual_albums = tested_albums.fetch(0)

    assert actual_albums == sample_albums
    assert get_mock.call_count == 1


def test_fetch_error(get_mock, response_mock, tested_albums):
    response_mock.json = lambda: []
    response_mock.status_code = 418

    with pytest.raises(Exception):
        tested_albums.fetch(0)

    assert get_mock.call_count == 1


@pytest.mark.parametrize("album_index", [0, 1, 2])
def test_format(tested_albums, sample_albums, album_index):
    album = sample_albums[album_index]
    album_id = album["id"]
    album_title = album["title"]

    assert tested_albums.format(album) == f"[{album_id}] {album_title}"


def test_main_ok(mocker, capsys, tested_albums, fetch_mock):
    mocker.patch("sys.argv", ["MOCK", "0"])

    tested_albums.main()
    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.strip().split("\n") == [
        "[1] album one",
        "[2] album two",
        "[3] album three",
    ]
    assert fetch_mock.call_count == 1


@pytest.mark.parametrize("bad_args", [[], [""], ["x"], ["1", "2"]])
def test_main_error(mocker, capsys, tested_albums, fetch_mock, bad_args):
    mocker.patch("sys.argv", ["MOCK"] + bad_args)

    with pytest.raises(SystemExit) as exc:
        tested_albums.main()

    captured = capsys.readouterr()

    assert "Usage" in (captured.err + str(exc))
    assert exc.value.code != 0
    assert captured.out == ""
    assert fetch_mock.call_count == 0
