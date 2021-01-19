from flask import request
from utils.genres import fill_genres_for


def fill_venue_data(venue):
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.facebook_link = request.form.get('facebook_link')
    venue.image_link = request.form.get('image_link')
    venue.seeking_talent = request.form.get('seeking_talent', 'n') == 'y'
    venue.seeking_description = request.form.get('seeking_description')
    venue.website = request.form.get('website')
    fill_genres_for(venue)
