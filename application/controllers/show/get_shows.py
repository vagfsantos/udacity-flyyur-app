from flask import render_template
from server import app
from models.show import Show


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
