from emotes.migrator import migrator, migration
from emotes.app.models import *
from playhouse.migrate import *
from werkzeug.security import generate_password_hash

@migration("20210123_223521")
def migration_20210123_223521():
    """Hash API keys"""

    users = User.select()

    for user in users:
        for api_key in user.api_keys:
            api_key.value = generate_password_hash(api_key.value)
            api_key.save()

            print(api_key.value)
