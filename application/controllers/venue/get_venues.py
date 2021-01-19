from flask import render_template
from server import app, db
from models.venue import Venue


@app.route('/venues')
def venues():
    def get_venues_by_location(location):
        def filter_by_location(venue):
            return (
                venue.state == location['state'] and
                venue.city == location['city']
            )

        all = filter(filter_by_location, venues)
        return all

    def get_result(location):
        all_venue_same_location = get_venues_by_location(location)
        location['venues'] = all_venue_same_location
        return location

    venues = Venue.query.all()
    venues_by_state_and_city = db.session.query(
        Venue.state, Venue.city).group_by(Venue.state, Venue.city).all()
    locations = list(
        map(lambda v: {'state': v[0], 'city': v[1]}, venues_by_state_and_city))

    result = list(map(get_result, locations))
    return render_template('pages/venues.html', areas=result)
