from flask import request
from models.genre import Genre


def fill_genres_for(artistOrVenue):
    genres = request.form.getlist('genres')

    artistOrVenue.genres.clear()
    for g in genres:
        genre = Genre.query.filter_by(name=g).first()
        artistOrVenue.genres.append(genre)
