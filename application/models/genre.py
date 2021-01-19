from server import db


artist_genres = db.Table('ArtistGenres',
                         db.Column('genre_id', db.Integer, db.ForeignKey(
                             'Genre.id'), primary_key=True),
                         db.Column('artist_id', db.Integer, db.ForeignKey(
                             'Artist.id'), primary_key=True)
                         )
venue_genres = db.Table('VenueGenres',
                        db.Column('genre_id', db.Integer, db.ForeignKey(
                            'Genre.id'), primary_key=True),
                        db.Column('venue_id', db.Integer, db.ForeignKey(
                            'Venue.id'), primary_key=True)
                        )


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
