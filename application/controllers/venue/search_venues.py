from flask import render_template, request
from server import app, db
from models.venue import Venue


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
    response = {
        "count": result.count(),
        "data": result
    }

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=search_term
    )
