import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.Integer, primary_key=True)
    year = sa.Column(sa.Integer)
    artist = sa.Column(sa.Text)
    genre = sa.Column(sa.Text)
    album = sa.Column(sa.Text)


class DBSession():
    """
    Create a session for DB and allow to add or find albums.
    """
    def __init__(self, db_path):
        self.session = connect_to_db(db_path)

    def get_artist_albums(self, artist):
        albums = self.session.query(Album).filter(Album.artist == artist).all()
        album_titles = [album.album for album in albums]
        return album_titles

    def add_album_to_db(self, album_data):
        self._is_album_in_db(album_data)
        self.session.add(album_data)
        self.session.commit()

    def _is_album_in_db(self, album_data):
        if self.session.query(Album).filter(Album.album == album_data.album).first():
            raise DuplicateAlbumError()


class DuplicateAlbumError(Exception):
    pass


def connect_to_db(DB_PATH):
    engine = sa.create_engine(DB_PATH)
    Session = sessionmaker(engine)
    return Session()
