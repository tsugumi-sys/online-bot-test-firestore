import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./secrets/firebase_searvice_account.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

bots = db.collection("bot").stream()
bot_list = [d.to_dict() for d in bots]
print(bot_list)
