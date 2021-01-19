from server import db
from models.genre import artist_genres


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=False)
    shows = db.relationship(
        'Show',
        backref="artist",
        lazy=True,
        cascade='all, delete'
    )
    genres = db.relationship(
        'Genre',
        secondary=artist_genres,
        lazy='subquery',
        backref=db.backref('artist', lazy=True)
    )

    def get_dict(self):
        genres = list(map(lambda g: g.name, self.genres))
        return {**self.__dict__, **{'genres': genres}}
