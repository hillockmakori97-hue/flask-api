# Rest Api- This is a backend route that follows the four rules below
# it has to have a route 
# It has to have a method (POST/GET/PUT/DELETE)
# It has to have a status code
# It has to return data as JSON
from sqlalchemy import create_engine,select
from flask import Flask,request,jsonify
from models import Base,Product,Purchase,User,Sale,Sale_detail
from sqlalchemy.orm import Session
from datetime import date 
app=Flask(__name__)

# create a database using sqlachemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

#  create tables into the database using sqlalchemy
Base.metadata.create_all(engine)

# Create a session to do sql transaction 
session=Session(engine)

user={
    'id':7,
    'full_name':'hillock',
    'email':'hillockmakori97@gmail.com',
    'password':'2345',
    'phone_number':'89439853489y'

}
@app.before_request
def before_request():
    try:
        print('a new request is coming')
        new_user=User(user)
        session.add(new_user)
        session.commit(new_user)
        return jsonify({'Message':'New user added successfully'}),200
    
    except:
        print('error found')

@app.route('/')
def home():
    if request.method == 'GET':
        data={'Flask API' : 'success' }
        return jsonify(data),200

    else:
        error={'Error': 'Method not allowed '}
        return jsonify(error),403

@app.route('/products',methods=['POST','GET'])
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
                'buying_price':prod.buying_price,
                'selling_price':prod.selling_price
            }
            results.append(p)
        return jsonify(results),200

    elif request.method=='POST':

        data=request.get_json()
        if data['buying_price'] =='' or data['selling_price']=='' or data['user_id']=='':
            error={'Error':'Ensure all fields are set'}
            return jsonify(error),403
        else:
            # store in the database
            new_product=Product(
                user_id=user['id'],
                buying_price=float(data['buying_price']),
                selling_price= float(data['selling_price']),
            
            )
            session.add(new_product)
            session.commit()
            return jsonify({'Message':'New product added'})


    else:
        error={'Error':'Method not allowed'}
        return jsonify(error),405


@app.route('/purchases',methods=['GET','POST'])
def purchases():
    if request.method=='GET':
        query=select(Purchase)
        purchases=session.scalars(query)
        result=[]
        for i in purchases:
            purchases
            {
                'id' :i.user_id,
                'product_id':i.product_id,
                'date_purchased':i.date_purchased,
                'purchase_price':i.purchase_price
            }
            result.append(purchases)
    elif request.method=='POST':
        data=request.get_json()
        if not data['product_id']or not data['date_purchased']or not data['purchase_price']:
            res=jsonify({'Message':'Ensure all fields are set'})
        
        else:
            # add the purchase 
            convert_date=date.fromisoformat(data['date_purchased'])
            new_purchase=Purchase(
                product_id=data['product_id'],
                date_purchased=convert_date,
                purchase_price=data['purchase_price']
            )
            session.add(new_purchase)
            session.commit()
            res= jsonify({'Message':'New purchase added'})
        return res
@app.route('/sales',methods=['POST','GET'])
def sales():
    if request.method=='GET':
        query=select(Sale)
        sales=session.scalars(query)
        result=[]
        for i in sales:
            sales
            {
                'id':i.id,
                'user_id':i.user_id,
                'date_sold':i.date_sold
            }
            result.append(sales)

    elif request.method=='POST':
        data=request.get_json()
        if not data['user_id'] or not data['date_sold']:
            res=jsonify({'Message':'Ensure all fields are set'})
        else:
            date_sold=date.fromisoformat(data['date_sold'])
            new_sale=Sale(
                user_id=data['user_id'],
                date_sold=date_sold
            )
            session.add(new_sale)
            session.commit()
            res=jsonify({'Message':'Sale Added Successfully'})
        return res
    else:
        return jsonify({'Message':'Method Not Allowed'})


       
@app.route('/sale-details',methods=['POST','GET'])
def sale_detail():
    if request.method=='GET':
        query=select(Sale_detail)
        sales_details=session.scalars(query)
        result=[]
        for i in sales_details:
            sales_details
            {
                'id':i.id,
                'product_id':i.product_id,
                'sale_id':i.sale_id,
                'quantity':i.quantity,
                'amount':i.amount

            }
        re
    elif request.method=='POST':
        pass
    else:
        pass



app.run(debug=True)