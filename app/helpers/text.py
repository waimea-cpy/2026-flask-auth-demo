#============================================================================
# Jinja2 Filters for Text
#
# Provides filters:
#   - paragraph      - Convert \n to <br> and \n\n to <p>
#============================================================================


def init_text_filters(app):
    """Register text formatting filters"""

    @app.template_filter('paragraphs')
    def _to_paragraphs(text):
        """Convert newlines to <br> and double newlines to <p>"""
        if not text:
            return ''
        paragraphs = text.split('\n\n')
        text = ''.join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
        text = text.replace('\n', '<br>')
        return text

