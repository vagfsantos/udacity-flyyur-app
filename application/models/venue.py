from server import db
from models.genre import venue_genres


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship(
        'Show',
        backref="venue",
        lazy=True,
        cascade='all, delete'
    )
    genres = db.relationship(
        'Genre',
        secondary=venue_genres,
        lazy='subquery',
        backref=db.backref('venue', lazy=True)
    )

    def get_dict(self):
        genres = list(map(lambda g: g.name, self.genres))
        return {**self.__dict__, **{'genres': genres}}
