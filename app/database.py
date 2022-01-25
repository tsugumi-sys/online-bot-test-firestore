import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_firestore_db():
    cred = credentials.Certificate("./secrets/firebase_searvice_account.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db
