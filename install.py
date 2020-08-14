import click
from emotes.wsgi import app, db
import string
import secrets
from emotes.app.models import *

def install():
    db.database.create_tables([
        User,
        Namespace,
        ApiKey,
        Emote,
        Version
    ])

    # Create an admin if they don't exist
    if User.select().where(User.admin == True).count() == 0:
        new_admin = User(name="Administrator", admin=True)
        new_admin.save()

        print("Installer: new admin Administrator saved.")

        admin_key = ApiKey(user=new_admin)
        admin_key.save()
        print(f"Installer: admin's api key is {admin_key.value}.\nKeep this value VERY safely.")
    else:
        pass
        # print("Installer: admin already created, skipping.")

if __name__ == "__main__":
    install()
