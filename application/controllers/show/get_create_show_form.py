from flask import render_template
from server import app
from forms import ShowForm


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)
