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


def update_contact(
    resource_name,
    new_name=None,
    new_email=None,
    new_phone=None,
    phone_label=None,  # <-- Nuevo parámetro
    new_address=None,
    new_organization=None,
    new_biography=None,
    new_birthday=None,  # formato: "YYYY-MM-DD"
    new_gender=None,
    new_event=None,
    new_relation=None,
    new_im_client=None,
    new_occupation=None,
):
    service = get_service()
    person = (
        service.people()
        .get(
            resourceName=resource_name,
            personFields="names,emailAddresses,phoneNumbers,addresses,organizations,biographies,birthdays,genders,events,relations,imClients,occupations",
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
        phone_dict = {"value": new_phone}
        if phone_label:
            phone_dict["type"] = phone_label  # Ejemplo: "mobile", "home", "work"
        contact_body["phoneNumbers"] = [phone_dict]
        update_fields.append("phoneNumbers")
    if new_address:
        contact_body["addresses"] = [{"formattedValue": new_address}]
        update_fields.append("addresses")
    if new_organization:
        contact_body["organizations"] = [{"name": new_organization}]
        update_fields.append("organizations")
    if new_biography:
        contact_body["biographies"] = [{"value": new_biography}]
        update_fields.append("biographies")
    if new_birthday:
        try:
            year, month, day = map(int, new_birthday.split("-"))
            contact_body["birthdays"] = [
                {"date": {"year": year, "month": month, "day": day}}
            ]
            update_fields.append("birthdays")
        except Exception:
            print("Formato de cumpleaños inválido. Usa YYYY-MM-DD.")
    if new_gender:
        contact_body["genders"] = [{"value": new_gender}]
        update_fields.append("genders")
    if new_event:
        contact_body["events"] = [{"type": "custom", "value": new_event}]
        update_fields.append("events")
    if new_relation:
        contact_body["relations"] = [{"person": new_relation}]
        update_fields.append("relations")
    if new_im_client:
        contact_body["imClients"] = [{"username": new_im_client}]
        update_fields.append("imClients")
    if new_occupation:
        contact_body["occupations"] = [{"value": new_occupation}]
        update_fields.append("occupations")

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
    # Ejemplo de uso: actualiza todos los campos posibles de un contacto
    update_contact(
        resource_name="people/c2525935020055560378",
        new_name="Rosbely Herrera",
        new_email="",
        new_phone="+58 4141952418",
        phone_label="mobile",
        new_address="Caracas, Venezuela",
        new_organization="",
        new_biography="",
        new_birthday="",
        new_gender="female",
        new_event="",
        new_relation="",
        new_im_client="",
        new_occupation="RRHH",
    )
