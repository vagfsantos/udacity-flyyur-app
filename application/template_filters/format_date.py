from server import app
import dateutil.parser
from babel.dates import format_datetime, format_date
from datetime import datetime


@app.template_filter('datetime')
def format_datetime_filter(value, format='medium'):
    date = value
    if not isinstance(value, datetime):
        date = dateutil.parser.parse(value)

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return format_datetime(date, locale='en', format=format)
