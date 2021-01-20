import logging
import sys
from logging import Formatter, FileHandler

from server import app
import template_filters.format_date

import controllers.index
import controllers.venue.create_venue
import controllers.venue.delete_venue
import controllers.venue.edit_venue
import controllers.venue.get_create_venue_form
import controllers.venue.get_edit_venue_form
import controllers.venue.get_venue_by_id
import controllers.venue.get_venues
import controllers.venue.search_venues

import controllers.artist.create_artist
import controllers.artist.delete_artist
import controllers.artist.edit_artist
import controllers.artist.get_artist_by_id
import controllers.artist.get_artists
import controllers.artist.get_create_artist_form
import controllers.artist.get_edit_artist_form
import controllers.artist.search_artists

import controllers.show.create_show
import controllers.show.get_create_show_form
import controllers.show.get_shows

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run()
