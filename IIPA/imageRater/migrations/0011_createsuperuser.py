import os


from django.contrib.auth.models import User
from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

from google.cloud import secretmanager
from django.conf import settings
import json
from google.oauth2 import service_account






def createsuperuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    Password is pulled from Secret Manger (previously created as part of tutorial)
    """
    if os.getenv("LOCAL_DEV", None):
        # We are in CI, so just create a placeholder user for unit testing.
        admin_password = "test"
    else:
        with open(os.path.join(os.getcwd(), "credential.json"), "r") as neep:
            data = json.load(neep)
            neep.close()
        
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
            data,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        # # _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()  # type: ignore
        # # Pull secrets from Secret Manager
        # project_id = "iipa-32fdd" # env("GOOGLE_CLOUD_PROJECT")
        client = secretmanager.SecretManagerServiceClient(credentials=GS_CREDENTIALS)

        # Retrieve the previously stored admin password
        PASSWORD_NAME = os.environ.get("PASSWORD_NAME", "superuser_password")
        name = f"projects/iipa-32fdd/secrets/{PASSWORD_NAME}/versions/latest"
        admin_password = client.access_secret_version(name=name).payload.data.decode(
            "UTF-8"
        )
    users = User.objects.all()
    for user in users:
        print(f'user is {user}')
        
    # Create a new user using acquired password, stripping any accidentally stored newline characters
    User.objects.create_superuser("superuser", "jazwickler@gmail.com" ,password = admin_password.strip())
    

class Migration(migrations.Migration):

   dependencies = [
        ('imageRater', '0010_alter_imagerating_rating'),
    ]
   
   operations = [migrations.RunPython(createsuperuser)]
