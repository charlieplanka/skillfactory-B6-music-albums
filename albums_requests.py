from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
from albums_database import DBSession, Album, DuplicateAlbumError

DB_PATH = "sqlite:///albums.sqlite3"
session = DBSession(DB_PATH)


class YearValueError(Exception):
    pass


class EmptyValueError(Exception):
    pass


@route("/albums/<artist>")
@route("/albums/<artist>/")
def find_albums(artist):
    """
    Returns a list of all artist's albums found in the database.
    """
    albums = session.get_artist_albums(artist)
    if not albums:
        error_message = f"No albums for {artist}"
        return HTTPError(404, error_message)
    html_message = make_html_with_albums_list(artist, albums)
    return html_message


def make_html_with_albums_list(artist, albums):
    """
    Makes an unordered HTML list from artist's albums.
    """
    albums_qty = len(albums)
    html_albums = [f"<li>{album}</li>" for album in albums]
    html_albums = "".join(html_albums)
    html_message = f"<strong>{artist}</strong> has {albums_qty} album(s):<br><ul>{html_albums}</ul>"
    return html_message


@route("/albums", method="POST")
@route("/albums/", method="POST")
def add_new_album():
    """
    Adds new album to the database.
    Returns 400 error if received values are not valid.
    Returns 409 error if the album is already in the database.
    """
    try:
        album_data = parse_request_data()
        session.add_album_to_db(album_data)
    except EmptyValueError:
        return HTTPError(400, "Album or artist cannot be empty")
    except YearValueError:
        return HTTPError(400, "Invalid year value")
    except DuplicateAlbumError:
        error_message = f"Album '{album_data.album}' has been already added"
        return HTTPError(409, error_message)
    else:
        return f"Album '{album_data.album}' by {album_data.artist} has been successfully added."


def parse_request_data():
    """
    Parses data from POST-request.
    """
    album = request.forms.get("album")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    year = request.forms.get("year")
    album = Album(
        album=album,
        artist=artist,
        genre=genre,
        year=year
    )
    validate_values(album)
    return album


def validate_values(album):
    """
    Checks if received values are valid.
    """
    if not album.artist or not album.album:
        raise EmptyValueError()
    try:
        if album.year is not None and int(album.year) < 1900:
            raise YearValueError()
    except ValueError:  # will arise if year is not an integer
        raise YearValueError()


if __name__ == "__main__":
    run(host="localhost", port=8081, debug=True)
