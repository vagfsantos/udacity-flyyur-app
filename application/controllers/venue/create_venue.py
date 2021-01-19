import sys
from flask import render_template, request, flash
from server import app, db
from utils.venues import fill_venue_data
from models.venue import Venue


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
