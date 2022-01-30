import firebase_admin
from firebase_admin import credentials, firestore


def get_firestore_db():
    try:
        _ = firebase_admin.get_app(name="[DEFAULT]")
        db = firestore.client()
        return db
    except ValueError:
        cred = credentials.Certificate("./secrets/firebase_searvice_account.json")
        firebase_admin.initialize_app(cred)

        db = firestore.client()
    return db
