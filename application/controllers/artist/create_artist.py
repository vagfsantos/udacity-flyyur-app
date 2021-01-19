import sys
from flask import render_template, request, flash
from server import app, db
from utils.artists import fill_artist_data
from models.artist import Artist


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artist = Artist()
        fill_artist_data(artist)

        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] +
              ' was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Artist could not be created.')
    finally:
        db.session.close()

    return render_template('pages/home.html')
