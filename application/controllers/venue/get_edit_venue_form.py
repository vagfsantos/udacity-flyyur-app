
from flask import render_template
from server import app
from models.venue import Venue
from forms import VenueForm


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(data=venue.get_dict())

    return render_template('forms/edit_venue.html', form=form, venue=venue)
