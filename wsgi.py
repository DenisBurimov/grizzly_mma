#!/user/bin/env python
import click

from app import create_app, db, models, forms
from app.controllers.ldap import LDAP

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, forms=forms, ldap=LDAP())


@app.cli.command()
@click.option("--test-data/--no-test-data", default=False)
def create_db(test_data: bool = False):
    """Create the configured database."""
    from app.controllers import init_db

    db.create_all()
    init_db(test_data)


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
