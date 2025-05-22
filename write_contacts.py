import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/contacts"]


def get_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("people", "v1", credentials=creds)


def update_contact(resource_name, new_name=None, new_email=None, new_phone=None):
    service = get_service()
    # Primero obtenemos el contacto actual para obtener el etag
    person = (
        service.people()
        .get(
            resourceName=resource_name, personFields="names,emailAddresses,phoneNumbers"
        )
        .execute()
    )
    etag = person.get("etag")
    contact_body = {"etag": etag}
    update_fields = []

    if new_name:
        contact_body["names"] = [{"givenName": new_name}]
        update_fields.append("names")
    if new_email:
        contact_body["emailAddresses"] = [{"value": new_email}]
        update_fields.append("emailAddresses")
    if new_phone:
        contact_body["phoneNumbers"] = [{"value": new_phone}]
        update_fields.append("phoneNumbers")

    if not update_fields:
        print("No hay datos para actualizar.")
        return

    updated = (
        service.people()
        .updateContact(
            resourceName=resource_name,
            updatePersonFields=",".join(update_fields),
            body=contact_body,
        )
        .execute()
    )
    print(
        "Contacto actualizado:",
        updated.get("names", [{}])[0].get("displayName", "Sin nombre"),
    )


if __name__ == "__main__":
    # Ejemplo de uso: actualiza el nombre, email y teléfono de un contacto
    # Reemplaza 'people/cXXXXXXXXXXXX' por el resourceName real del contacto
    update_contact(
        resource_name="people/c2583949602253469377",
        new_name="Vicent Rivero",
        new_email="",
        new_phone="+584142593980",
    )
