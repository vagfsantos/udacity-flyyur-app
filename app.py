import logging
import sys
from logging import Formatter, FileHandler

import dateutil.parser
from babel.dates import format_datetime, format_date
from datetime import date, datetime

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms import ShowForm, ArtistForm, VenueForm

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
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


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(
        db.Integer, db.ForeignKey('Artist.id'),
        nullable=False
    )
    venue_id = db.Column(
        db.Integer, db.ForeignKey('Venue.id'),
        nullable=False
    )
    start_time = db.Column(db.DateTime, nullable=False)


def fill_genres_for(artistOrVenue):
    genres = request.form.getlist('genres')
    artistOrVenue.genres.clear()
    for g in genres:
        genre = Genre().query.filter_by(name=g).first()
        artistOrVenue.genres.append(genre)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


@app.template_filter('datetime')
def format_datetime_filter(value, format='medium'):
    date = value
    if not isinstance(value, datetime):
        date = dateutil.parser.parse(value)

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return format_datetime(date, locale='en', format=format)
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    venues = Venue.query.all()
    venues_by_state_and_city = db.session.query(
        Venue.state, Venue.city).group_by(Venue.state, Venue.city).all()
    locations = list(
        map(lambda v: {'state': v[0], 'city': v[1]}, venues_by_state_and_city))

    def get_venues_by_location(location):
        def filter_by_location(venue):
            return venue.state == location['state'] and venue.city == location['city']

        all = filter(filter_by_location, venues)
        return all

    def get_result(location):
        all_venue_same_location = get_venues_by_location(location)
        location['venues'] = all_venue_same_location
        return location

    result = list(map(get_result, locations))

    return render_template('pages/venues.html', areas=result)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
    response = {
        "count": result.count(),
        "data": result
    }

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=search_term
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    past_shows = Show.query.filter(
        Show.venue_id == venue.id, Show.start_time < datetime.now())
    upcoming_shows = Show.query.filter(
        Show.venue_id == venue.id, Show.start_time >= datetime.now())
    shows_info = {
        "past_shows": past_shows.all(),
        "upcoming_shows": upcoming_shows.all(),
        "past_shows_count": past_shows.count(),
        "upcoming_shows_count": upcoming_shows.count()
    }

    data = {**venue.get_dict(), **shows_info}
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


def fill_venue_data(venue):
    fill_genres_for(venue)
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


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venue = Venue()
        fill_venue_data(venue)

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Venue could not be created.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return ('', 200)
    # return redirect(url_for('venues'))
    # TODO: (Bonus) Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(data=venue.get_dict())

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        fill_venue_data(venue)

        db.session.add(venue)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
    response = {
        "count": result.count(),
        "data": result
    }

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    past_shows = Show.query.filter(
        Show.artist_id == artist.id, Show.start_time < datetime.now())
    upcoming_shows = Show.query.filter(
        Show.artist_id == artist.id, Show.start_time >= datetime.now())
    shows_info = {
        "past_shows": past_shows.all(),
        "upcoming_shows": upcoming_shows.all(),
        "past_shows_count": past_shows.count(),
        "upcoming_shows_count": upcoming_shows.count()
    }

    data = {**artist.get_dict(), **shows_info}
    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(data=artist.get_dict())

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        fill_artist_data(artist)

        db.session.add(artist)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


def fill_artist_data(artist):
    fill_genres_for(artist)
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


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artist = Artist()
        fill_artist_data(artist)

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Venue could not be created.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return ('', 200)
    # return redirect(url_for('venues'))
    # TODO: (Bonus) Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = map(lambda s: {
        "venue_id": s.venue_id,
        "venue_name": s.venue.name,
        "artist_id": s.artist_id,
        "artist_name": s.artist.name,
        "artist_image_link": s.artist.image_link,
        "start_time": s.start_time
    }, shows)
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show()
        show.artist_id = request.form.get('artist_id')
        show.venue_id = request.form.get('venue_id')
        show.start_time = request.form.get('start_time')

        db.session.add(show)
        db.session.commit()
        flash('Show was successfully created!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Show could not be created.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


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
