import os
import pickle
import datetime
import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Si modificas estos alcances, elimina el archivo token.pickle.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]


def main():
    creds = None
    # El archivo token.pickle almacena el token de acceso del usuario.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # Si no hay credenciales válidas, solicita el login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima vez.
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("people", "v1", credentials=creds)

    # Llama a la API de People para obtener todos los datos posibles de los contactos
    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=1000,
            personFields="names,emailAddresses,phoneNumbers,addresses,organizations,biographies,birthdays,genders,photos,urls,events,relations,imClients,occupations",
        )
        .execute()
    )
    connections = results.get("connections", [])

    # Extrae los datos a una lista de diccionarios
    data = []
    for person in connections:
        resource_name = person.get("resourceName", "")
        name = person.get("names", [{}])[0].get("displayName", "")
        email = person.get("emailAddresses", [{}])[0].get("value", "")
        phone = person.get("phoneNumbers", [{}])[0].get("value", "")
        phone_label = person.get("phoneNumbers", [{}])[0].get("type", "")
        address = person.get("addresses", [{}])[0].get("formattedValue", "")
        organization = person.get("organizations", [{}])[0].get("name", "")
        biography = person.get("biographies", [{}])[0].get("value", "")
        birthday = person.get("birthdays", [{}])[0].get("date", "")
        birthday = (
            datetime.date(
                birthday.get("year", 0),
                birthday.get("month", 0),
                birthday.get("day", 0),
            )
            if birthday
            else ""
        )
        birthday = birthday.strftime("%d-%m-%Y") if birthday else ""
        gender = person.get("genders", [{}])[0].get("value", "")
        # photo = person.get("photos", [{}])[0].get("url", "")
        # url = person.get("urls", [{}])[0].get("value", "")
        event = person.get("events", [{}])[0].get("type", "")
        relation = person.get("relations", [{}])[0].get("person", "")
        im_client = person.get("imClients", [{}])[0].get("username", "")
        occupation = person.get("occupations", [{}])[0].get("value", "")
        data.append(
            {
                "resource_name": resource_name,
                "Nombre": name,
                "Email": email,
                "Telefono": phone,
                "Etiqueta": phone_label,
                "Dirección": address,
                "Organización": organization,
                "Biografía": biography,
                "Cumpleaños": birthday,
                "Género": gender,
                # "Foto": photo,
                # "URL": url,
                "Evento": event,
                "Relación": relation,
                "IM": im_client,
                "Ocupación": occupation,
            }
        )

    # Crea el DataFrame
    df = pd.DataFrame(data)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
