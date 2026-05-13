#============================================================================
# Jinja2 Filters for DateTime using Arrow
#
# Provides filters:
#   - timezone(dt, tz)      - Convert datetime to a specific timezone
#   - local(dt)             - Convert datetime to default local timezone
#   - format(dt, fmt)       - Format datetime with Arrow tokens
#   - format_date(dt, fmt)  - Format date only
#   - format_time(dt, fmt)  - Format time only
#   - format_human(dt, tz)  - Human-readable relative time (e.g., '2 hours ago')
#
# Provides globals:
#   - now(tz)               - Get current datetime in specified timezone
#============================================================================

from os import getenv
from dotenv import load_dotenv
import arrow


load_dotenv()
DEFAULT_TIMEZONE = getenv("DEFAULT_TIMEZONE", "Pacific/Auckland")

NICE_DATE_FORMAT = "ddd, DD MMM YYYY"
NICE_TIME_FORMAT = "h:mmA"
NICE_DATETIME_FORMAT = f"{NICE_DATE_FORMAT} [at] {NICE_TIME_FORMAT}"


def init_date_filters(app):
    """Register Arrow-based date/time filters with the Flask app"""

    @app.template_filter('timezone')
    def _to_timezone(dt, tz=DEFAULT_TIMEZONE):
        """Convert to specific timezone."""
        if not dt:
            return None
        return arrow.get(dt).to(tz)

    @app.template_filter('local')
    def _to_local(dt):
        """Convert to default local timezone."""
        if not dt:
            return None
        return arrow.get(dt).to(DEFAULT_TIMEZONE)

    @app.template_filter('format')
    def _format_datetime(dt, fmt=NICE_DATETIME_FORMAT):
        """Format datetime. Uses Arrow tokens: YYYY, MM, DD, HH, mm, ss, etc."""
        if not dt:
            return ''
        return arrow.get(dt).format(fmt)

    @app.template_filter('format_date')
    def _format_date(dt, fmt=NICE_DATE_FORMAT):
        """Format date. Uses Arrow tokens: YYYY, MM, DD, etc."""
        return _format_datetime(dt, fmt)

    @app.template_filter('format_time')
    def _format_time(dt, fmt=NICE_TIME_FORMAT):
        """Format time. Uses Arrow tokens: HH, mm, ss, etc."""
        return _format_datetime(dt, fmt)

    @app.template_filter('format_human')
    def _format_date_humanize(dt, tz=DEFAULT_TIMEZONE, granularity='auto'):
        """Human-readable relative time like '2 hours ago'."""
        if not dt:
            return ''
        arr = arrow.get(dt).to(tz)
        return arr.humanize(granularity=granularity)

    # Global function for current time
    app.jinja_env.globals['now'] = lambda tz=DEFAULT_TIMEZONE: arrow.now(tz)

