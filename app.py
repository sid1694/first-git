# app.py
# Required Imports
import os
from datetime import datetime
from random import randint
from flask import Flask, request, jsonify, render_template, json, redirect
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App
app = Flask(__name__)
# Initialize Firestore DB
cred = credentials.Certificate('serviceAccount.json')
default_app = initialize_app(cred)
db = firestore.client()
orderCollection = db.collection(u'ORDERSNEW')
@app.route('/', methods=['POST'])
def add():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    orders = {}
    # print("Starts from here ___________________________")
    # print(request.form.to_dict())
    # print("Ends  here ___________________________")
    data = request.form.to_dict()
    orderDate = datetime.strptime(data['orderDate'], "%Y-%m-%d")
    shipDate = datetime.strptime(data['shipDate'], "%Y-%m-%d")

    orders['orderID'] = randint(100000000, 999999999)
    orders['Region'] = data['region']
    orders['Country'] = data['country']
    orders['itemType'] = data['itemType']
    orders['orderDate'] = orderDate.strftime("%m/%d/%Y")
    orders['salesChannel'] = data['salesChannel']
    orders['orderPriority'] = data['orderPriority']
    orders['shipDate'] = shipDate.strftime("%m/%d/%Y")
    orders['unitsSold'] = data['unitsSold']
    orders["unitPrice"] = data['unitPrice']
    orders["unitCost"] = data['unitCost']
    orders['totalRevenue'] = data['totalRevenue']
    orders['totalCost'] = data['totalCost']
    orders['totalProfit'] = data['totalProfit']

    # orders.orderDate = request.form.to_dict()['orderDate']
    # orders.country = request.form.to_dict()['itemType']
    # orders.salesChannel = request.form.to_dict()['salesChannel']
    # orders.orderPriority = request.form.to_dict()['orderPriority']
    # orders.shipDate = request.form.to_dict()['shipDate']
    # orders.unitsSold = request.form.to_dict()['unitsSold']
    # orders.unitPrice = request.form.to_dict()['unitPrice']
    # orders.unitCost = request.form.to_dict()['unitCost']
    # orders.totalRevenue = request.form.to_dict()['totalRevenue']
    # orders.totalCost = request.form.to_dict()['totalCost']
    # orders.totalProfit = request.form.to_dict()['totalProfit']
    
    try:
        orderCollection.add(orders)
        return redirect('/', code=200)
    except Exception as e:
        return f"An Error Occured: {e}"
@app.route('/', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents
    """
    try:
        docs = db.collection(u'ORDERSNEW').stream() // get all documents in a collection
        orders = []
        for doc in docs:
            orders.append(doc.to_dict())
        return render_template('index.html', orders = orders)
    except Exception as e:
        return f"An Error Occured: {e}"
# @app.route('/update', methods=['POST', 'PUT'])
# def update():
#     try:
#         id = request.json['id']
#         orders.document(id).update(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"
@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection
    """
    try:
        print("Start _____________________")
        print(request.args)
        orderID = request.args.to_dict()['orderID']
        orderID = int(orderID)
        print(orderID)
        print("ENd _____________________")
        print(orderCollection)
        query_ref = orderCollection.where(u'orderID', u'==', orderID)
        print(query_ref)
        for query in query_ref.stream():
            print("*************************************")
            print(query)
            db.collection(u'ORDERSNEW').document(query.id).delete()
        return redirect('/', code=200)
    except Exception as e:
        return f"An Error Occured: {e}"
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
