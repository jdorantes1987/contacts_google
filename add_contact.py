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


def add_contact(
    name,
    email,
    phone,
    phone_label,
    address,
    organization,
    biography,
    birthday,  # formato: "YYYY-MM-DD"
    gender,
    event,
    relation,
    im_client,
    occupation,
):
    service = get_service()
    contact_body = {}

    if name:
        contact_body["names"] = [{"givenName": name}]
    if email:
        contact_body["emailAddresses"] = [{"value": email}]
    if phone:
        phone_dict = {"value": phone}
        if phone_label:
            phone_dict["type"] = phone_label
        contact_body["phoneNumbers"] = [phone_dict]
    if address:
        contact_body["addresses"] = [{"formattedValue": address}]
    if organization:
        contact_body["organizations"] = [{"name": organization}]
    if biography:
        contact_body["biographies"] = [{"value": biography}]
    if birthday:
        try:
            year, month, day = map(int, birthday.split("-"))
            contact_body["birthdays"] = [
                {"date": {"year": year, "month": month, "day": day}}
            ]
        except Exception:
            print("Formato de cumpleaños inválido. Usa YYYY-MM-DD.")
    if gender:
        contact_body["genders"] = [{"value": gender}]
    if event:
        contact_body["events"] = [{"type": "custom", "value": event}]
    if relation:
        contact_body["relations"] = [{"person": relation}]
    if im_client:
        contact_body["imClients"] = [{"username": im_client}]
    if occupation:
        contact_body["occupations"] = [{"value": occupation}]

    created = service.people().createContact(body=contact_body).execute()
    print(
        "Contacto creado:",
        created.get("names", [{}])[0].get("displayName", "Sin nombre"),
    )


if __name__ == "__main__":
    # Datos hardcodeados para el nuevo contacto
    name = "Tibisay Chaparro"
    email = ""
    phone = "+584242964199"
    phone_label = "mobile"
    address = "Caracas, Venezuela"
    organization = ""
    biography = ""
    birthday = ""
    gender = "female"
    event = ""
    relation = "Familia"
    im_client = ""
    occupation = ""

    add_contact(
        name,
        email,
        phone,
        phone_label,
        address,
        organization,
        biography,
        birthday,
        gender,
        event,
        relation,
        im_client,
        occupation,
    )
