from flask import render_template
from server import app
from models.artist import Artist
from forms import ArtistForm


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(data=artist.get_dict())

    return render_template('forms/edit_artist.html', form=form, artist=artist)
