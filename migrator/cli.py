from emotes.wsgi import app
from flask.cli import AppGroup
from slugify import slugify
import click
import os

migration_cli = AppGroup('migrations')

@migration_cli.command("create")
@click.argument('name')
def create_migration(name):
    from datetime import datetime
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = slugify(name).replace("-", "_").lower()

    filename = f"{name}_{time_str}.py"
    path = os.path.join(app.config["MIGRATIONS_PATH"], filename)

    template = f"""from emotes.migrator import migrator, migration
from playhouse.migration import *

@migration("{time_str}")
def migration_{time_str}():
    \"\"\"Put your migration here.\"\"\"
    pass
    """

    with open(path, 'w+') as migration_file:
        migration_file.write(template)

    print(f"Migration {path} created successfully.")


app.cli.add_command(migration_cli)
