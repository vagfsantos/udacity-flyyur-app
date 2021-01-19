from flask import render_template
from server import app
from models.artist import Artist


@app.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)
