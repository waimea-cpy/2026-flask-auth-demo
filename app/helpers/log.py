#============================================================================
# Logging of Requests and Template Rendering with Rich
#============================================================================

from os import environ, getenv
from sys import exc_info
from dotenv import load_dotenv
from flask import request, session, render_template
from flask.signals import before_render_template
from rich.logging import RichHandler
from rich.console import Console
from rich.table import Table
import logging
import re

# Load Flask environment config
load_dotenv()
FLASK_HOST = getenv("FLASK_RUN_HOST", "localhost")
FLASK_PORT = getenv("FLASK_RUN_PORT", "5000")

# Rich console
console = Console()

STATUS_INFO = {
    200: "OK",
    201: "created",
    202: "accepted",
    204: "no content",
    301: "moved perm.",
    302: "found (redirect)",
    303: "see other",
    304: "from cache",
    307: "temp. redirect",
    308: "perm. redirect",
    400: "bad request",
    401: "unauthorised",
    403: "forbidden",
    404: "not found",
    405: "bad method",
    500: "server error",
}

STATIC = "static"
EXCLUDED_CONTEXT_KEYS = {'request', 'session', 'g', 'config', 'url_for', 'get_flashed_messages'}

APP_LOGGER   = "FLASK"
JINJA_LOGGER = "JINJA"


def log_prefix(action="", colour="yellow", logger=APP_LOGGER):
    """Create a consistent log prefix with color and alignment"""
    return f"[{colour}][{logger}] {action:>7}{':' if action else ' '}[/{colour}]"


def init_logging(app):
    """Initialize Rich logging"""

    import flask
    import jinja2
    import werkzeug

    # Clear console at startup
    if environ.get('WERKZEUG_RUN_MAIN') == 'true':
        console.clear()

    # Configure Rich handler
    handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=5,
        tracebacks_suppress=[
            flask,
            jinja2,
            werkzeug,
            "app/helpers/db.py",
            "app/helpers/log.py",
            "app/helpers/date.py",
        ],
        tracebacks_max_frames=3,
        markup=True,
        show_path=False,
        show_level=False,
        log_time_format="[%X]",
        omit_repeated_times=True,
    )

    # Setup app logger
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Disable Werkzeug's built-in logging
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)

    _register_request_logging(app)
    _register_template_logging(app)
    _announce_server_start(app)

    # Log routes after everything is initialized
    log_routes(app)


def _register_request_logging(app):
    """Register before/after request logging handlers"""

    @app.before_request
    def log_request_start():
        if request.endpoint == STATIC:
            return

        # Get route information
        view_func = app.view_functions.get(request.endpoint) if request.endpoint else None
        if view_func and hasattr(view_func, '__name__'):
            route_name = str(request.url_rule) if request.url_rule else ""
            func_name = f"➜ {view_func.__name__}()"
        else:
            route_name = "[red][bold]✗[/bold] unknown route[/red]"
            func_name = ""

        # Build URL with query string
        query_text = '?' + request.query_string.decode('utf-8') if request.query_string else ''
        path_text = f"{request.path}{query_text}"

        # Log request info
        console.rule()
        app.logger.debug(
            f"{log_prefix('Request')} {request.method} {path_text} ➜ {route_name} {func_name}"
        )

        # Log request data
        if request.view_args:
            app.logger.debug(f"{log_prefix('Params')} {request.view_args}")

        if request.args:
            app.logger.debug(f"{log_prefix('Query')} {dict(request.args)}")

        if request.form:
            app.logger.debug(f"{log_prefix('Form')} {dict(request.form)}")

        if request.files and any(file.filename for file in request.files.values()):
            filenames = [f.filename for f in request.files.values()]
            app.logger.debug(f"{log_prefix('Files')} {filenames}")

        if session:
            app.logger.debug(f"{log_prefix('Session')} {dict(session)}")

    @app.after_request
    def log_request_end(response):
        status_code = response.status_code
        status_name = STATUS_INFO.get(status_code, "")
        status_text = (
            f"{log_prefix('Status')} {request.method} {request.path} ➜ "
            f"{status_code} [dim]({status_name})[/dim]"
        )

        if request.endpoint == STATIC:
            app.logger.debug(f"[dim]{status_text}[/dim]")
        else:
            app.logger.info(status_text)

        return response


def _register_template_logging(app):
    """Register template rendering logging"""

    @before_render_template.connect_via(app)
    def log_before_render(sender, template, context, **extra):
        if not app.debug:
            return

        app.logger.debug(f"{log_prefix('Render', 'magenta', JINJA_LOGGER)} {template.name}")

        # Filter out Flask built-ins from context
        template_data = [
            key for key in context.keys()
            if not key.startswith('_') and key not in EXCLUDED_CONTEXT_KEYS
        ]

        if template_data:
            app.logger.debug(f"{log_prefix('Data', 'magenta', JINJA_LOGGER)} {template_data}")


def _announce_server_start(app):
    """Announce server startup with routes table"""
    if environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return

    console.rule("[green bold]Launching Flask App[/green bold]")
    console.print(
        f"🚀 [green]Server running at[/green] "
        f"[link=http://{FLASK_HOST}:{FLASK_PORT}]http://{FLASK_HOST}:{FLASK_PORT}[/link]"
    )

    if app.debug:
        console.print("🔧 [yellow]Debug mode enabled[/yellow]")


def get_logger():
    """Get the app logger (call after init_logging)"""
    return logging.getLogger('app')

def get_console():
    """Get the app console (call after init_logging)"""
    return console


def truncate(text, width=50):
    """Truncate text to width, properly closing any open quotes"""
    # Strip blank lines and indents, then collapse to single line
    lines = [line.strip() for line in str(text).splitlines() if line.strip()]
    text = ' '.join(lines)

    if len(text) <= width:
        return text

    # Trim, accounting for final three dots
    truncated_text = text[:width - 3]

    # Remove complete quoted strings, leaving only unmatched quotes
    no_doubles = re.sub(r'"[^"]*"', '', truncated_text)
    no_singles = re.sub(r"'[^']*'", '', truncated_text)

    # Close any unmatched quotes
    closing = ""
    if no_singles.count("'") % 2:
        closing += "'"
    if no_doubles.count('"') % 2:
        closing += '"'

    return truncated_text + closing + "..."


def log_exception(error):
    """Log exception with Rich formatting"""
    exc_type, exc_value, exc_traceback = exc_info()
    logger = get_logger()

    logger.error(
        f"{log_prefix('Error', 'red bold')} {exc_type.__name__} ➜ {str(error)}",
        exc_info=True
    )


def log_routes(app):
    """Log all registered routes as a Rich table"""
    if environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return

    table = Table(show_header=False)
    table.add_column("Method",            style="yellow")
    table.add_column("Route Pattern",     style="cyan")
    table.add_column("Endpoint Function", style="green")

    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        endpoint_display = rule.endpoint + ("()" if rule.endpoint != STATIC else "")
        table.add_row(methods, rule.rule, endpoint_display)

    console.rule("[yellow bold]Registered Routes[/yellow bold]")
    console.print(table)


