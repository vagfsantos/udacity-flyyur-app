import sys
from flask import redirect, url_for
from server import app, db
from models.artist import Artist
from utils.artists import fill_artist_data


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
