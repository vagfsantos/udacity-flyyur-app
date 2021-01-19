from flask import render_template
from server import app
from models.artist import Artist
from models.show import Show
from datetime import datetime


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
