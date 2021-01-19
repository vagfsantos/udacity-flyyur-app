import sys
from flask import render_template, request, flash
from server import app, db
from models.show import Show


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
