import firebase_admin

import os

import json

from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccount.json")

firebase_admin.initialize_app(cred)

db = firestore.client()
file_path = "./takehome.json"
collection_name = "ORDERSNEW"
# for filename in os.listdir('data'):

#     if filename.endswith('.json'):

#         collectionName = filename.split('.')[0] # filename minus ext will be used as collection name

f = open(file_path, 'r')

docs = json.loads(f.read())

# for doc in docs:
#         print(json.dumps(doc))

        #     id = doc.pop('id', None)

        #     if id:

        #         db.collection(collection_name).document(id).set(doc, merge=True)

        #     else:

#     db.collection(collection_name).add(doc)
    
# orders = db.collection(u'ORDERSNEW').stream()
# print(orders)
# store = []
# for order in orders:
#         store.append(order.to_dict())
# print(store)

orderID = 
orders_ref = db.collection(u'ORDERSNEW')
query_ref = orders_ref.where(u'orderID', u'==', orderID)
for query in query_ref.stream():
        print(query)
        print("************")
        print(query.id)
        db.collection(u'ORDERSNEW').document(query.id).delete()


