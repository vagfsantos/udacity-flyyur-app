from flask import render_template
from server import app, db
from models.venue import Venue
from models.show import Show
from datetime import datetime


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
