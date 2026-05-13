# Flask Project Template

This is a starter for a [Flask web app](https://flask.palletsprojects.com/), built using [Python](https://www.python.org/), that using a [SQLite database](https://sqlite.org/), and [Jinja2 templates](https://jinja.palletsprojects.com/templates/). Basic styling is handled by [PicoCSS](https://picocss.com/).

See the [docs folder](docs) for a quick-start and guides to usage. In particular:

- [Setup](docs/guides/setup.md)
- [Routes](docs/guides/routes.md) in Flask
- [Jinja](docs/guides/jinja.md) templates
- [DB Schema](docs/guides/schema.md)
- [SQL Queries](docs/guides/sqlite.md)

*For easier reading, the docs are hosted as a [GH Pages site](https://waimea-dt.github.io/flask-starter/)*


## Project Structure

```
├── README.md            # Project README
│
├── Dockerfile           # Define environment and launch Flask
│
├── docker-compose.yml   # Docker run configuration
│
├── requirements.txt     # Python modules required
│
├── app/                 # Flask application
│   │
│   ├── __init__.py      # Routes and app logic
│   │
│   ├── .env             # Environment values
│   │
│   ├── templates/       # Jinja2 templates
│   │   ├── pages/       # Full page templates
│   │   └── partials/    # Reusable template parts
│   │
│   ├── static/          # Files to be served directly
│   │   ├── css/         # CSS stylesheets
│   │   ├── images/      # Images
│   │   └── js/          # Javascript files
│   │
│   ├── db/              # Database files
│   │   ├── config.py    # Database schema & seed data
│   │   └── data.sqlite  # SQLite database
│   │
│   └── helpers/         # Helper files (don't modify)
│
└── docs/                # Project documentation
    └── guides/          # Helpful guides
```

## Useful Commands

### Database Management
- `flask db-show` - View database schema and all data
- `flask db-schema` - Show just the schema
- `flask db-data` - Show just the data
- `flask db-reset` - Delete and recreate database with seed data
- `flask db-seed` - Reseed database (keeps structure)
- `flask db-clear` - Clear all data (keeps structure)

### Development
- `flask run` - Start the development server
- `flask --help` - See all available commands

