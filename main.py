# Rest Api- This is a backend route that follows the four rules below
# it has to have a route 
# It has to have a method (POST/GET/PUT/DELETE)
# It has to have a status code
# It has to return data as JSON
from flask import Flask,request,jsonify
import json
app=Flask(__name__)
@app.route('/')
def home():
    if request.method == 'GET':
        data={'Flask API' : 'success' }
        return jsonify(data),200

    else:
        error={'Error': 'Method not allowed '}
        return jsonify(error),403
    
app.run(debug=True)