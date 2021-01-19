import sys
from flask import redirect, url_for
from server import app, db
from models.venue import Venue
from utils.venues import fill_venue_data


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
