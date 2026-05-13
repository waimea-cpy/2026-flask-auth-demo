#============================================================================
# Error handlers for the application
#============================================================================

from flask import render_template
from app.helpers.log import log_exception


def init_error_handlers(app):
    """Register error handlers with the Flask app"""

    @app.errorhandler(404)
    def page_not_found(error):
        """Handle 404 - Page Not Found"""
        return render_template("pages/404.jinja"), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        log_exception(error)
        return render_template("pages/500.jinja"), 500

