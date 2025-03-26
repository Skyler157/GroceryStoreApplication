from http.client import responses
from itertools import product

from flask import Flask, request, jsonify
from flask_cors import CORS
import products_dao
import uom_dao
from sql_connection import get_sql_connection
import json

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

connection = get_sql_connection()

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    products = uom_dao.get_uoms(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProducts', methods=['POST', 'OPTIONS'])
def delete_product():
    if request.method == 'OPTIONS':
        return jsonify(), 200  
    
    if request.method == 'POST':
        data = request.get_json()  
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({"error": "product_id is required"}), 400

        products_dao.delete_product(connection, product_id)

        return jsonify({'product_id': product_id})


@app.route('/insertProducts', methods=['POST'])
def insert_products():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id':product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True, port=5000)  