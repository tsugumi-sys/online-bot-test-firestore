import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./secrets/firebase_searvice_account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

db.collection("test").add({"id": 123456})
res = db.collection("test").where("id", "==", 1234567).get()
print(res)
print(res[0].id)
