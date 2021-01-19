from flask import request
from utils.genres import fill_genres_for


def fill_artist_data(artist):
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.address = request.form.get('address')
    artist.phone = request.form.get('phone')
    artist.facebook_link = request.form.get('facebook_link')
    artist.image_link = request.form.get('image_link')
    artist.seeking_venue = request.form.get('seeking_venue', 'n') == 'y'
    artist.seeking_description = request.form.get('seeking_description')
    artist.website = request.form.get('website')
    fill_genres_for(artist)
