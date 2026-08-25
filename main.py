# Rest Api- This is a backend route that follows the four rules below
# it has to have a route 
# It has to have a method (POST/GET/PUT/DELETE)
# It has to have a status code
# It has to return data as JSON
from sqlalchemy import create_engine,select
from flask import Flask,request,jsonify
from models import Base,Product
from sqlalchemy.orm import Session

app=Flask(__name__)

# create a database using sqlachemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

#  create tables into the database using sqlalchemy
Base.metadata.create_all(engine)

# Create a session to do sql transaction 
session=Session(engine)

@app.route('/')
def home():
    if request.method == 'GET':
        data={'Flask API' : 'success' }
        return jsonify(data),200

    else:
        error={'Error': 'Method not allowed '}
        return jsonify(error),403

@app.route('/products')
def products():
    if request.method=='GET':
    # fetch data from the database
        query=select(Product)
        products=session.scalars(query)
        results=[]
        for prod in products:
            p={
                'id':prod.id,
                'user_id':prod.user_id,
                'product_name':prod.product_name,
                'buying_price':prod.buying_price
            }
            results=results.append(p)
        return jsonify(results),200

    elif request.method=='POST':

        data=request.get_json()
        if data['product_name']=='' or data['buying_price'] =='' or data['selling_price']=='':
            error={'Error':'Ensure all fields are set'}
            return jsonify(error),403
        else:
            # store in the database
            pass


    else:
        error={'Error':'Method not allowed'}
        return jsonify(error),405


app.run(debug=True)