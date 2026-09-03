# Rest Api- This is a backend route that follows the four rules below
# it has to have a route 
# It has to have a method (POST/GET/PUT/DELETE)
# It has to have a status code
# It has to return data as JSON
from sqlalchemy import create_engine, select
from flask import Flask, request, jsonify
from models import Base, Product, Purchase, User, Sale, Sale_detail, Payment
from sqlalchemy.orm import Session
from datetime import date 
from flask_bcrypt import Bcrypt
from flask import redirect,url_for

app = Flask(__name__)
bcrypt=Bcrypt(app)

# Create a database using sqlalchemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# Create tables into the database using sqlalchemy
Base.metadata.create_all(engine)

# Create a session to do sql transaction 
session = Session(engine)

user = {
    'id': 7,
    'full_name': 'hillock',
    'email': 'hillockmakori97@gmail.com',
    'password': '2345',
    'phone_number': '89439853489y'
}



@app.before_request
def before_request():
    try:
        print('a new request is coming')
        # Note: Passes dictionary unpack or user object based on model definition
        new_user = User(**user)
        session.add(new_user)
        session.commit()
    except Exception as e:
        print('User already exists or error occurred')




@app.route('/')
def home():
    if request.method == 'GET':
        data = {'Flask API': 'success'}
        return jsonify(data), 200
    else:
        error = {'Error': 'Method not allowed'}
        return jsonify(error), 405



@app.route('/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        # Fetch data from the database
        query = select(Product)
        products = session.scalars(query)
        results = []
        for prod in products:
            p = {
                'id': prod.id,
                'user_id': prod.user_id,
                'buying_price': prod.buying_price,
                'selling_price': prod.selling_price
            }
            results.append(p)
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json()
        
        # Check for empty json or missing fields
        if not data or not data['buying_price'] or not data['selling_price']:
            error = {'Error': 'Ensure all fields are set'}
            return jsonify(error), 400
        
        # Store in the database
        new_product = Product(
            user_id=user['id'],
            buying_price=float(data['buying_price']),
            selling_price=float(data['selling_price'])
        )
        session.add(new_product)
        session.commit()
        return jsonify({'Message': 'New product added'}), 201

    else:
        error = {'Error': 'Method not allowed'}
        return jsonify(error), 405






@app.route('/purchases', methods=['GET', 'POST'])
def purchases():
    if request.method == 'GET':
        query = select(Purchase)
        purchases_list = session.scalars(query)
        result = []
        for i in purchases_list:
            item = {
                'id': i.id,
                'product_id': i.product_id,
                'date_purchased': i.date_purchased,
                'purchase_price': i.purchase_price
            }
            result.append(item)
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.get_json()
        
        # Check for empty input
        if not data or not data['product_id'] or not data['date_purchased'] or not data['purchase_price']:
            return jsonify({'Message': 'Ensure all fields are set'}), 400
        
        # Add the purchase 
        convert_date = date.fromisoformat(data['date_purchased'])
        new_purchase = Purchase(
            product_id=data['product_id'],
            date_purchased=convert_date,
            purchase_price=data['purchase_price']
        )
        session.add(new_purchase)
        session.commit()
        return jsonify({'Message': 'New purchase added'}), 201

    else:
        return jsonify({'Message': 'Method Not Allowed'}), 405







@app.route('/sales', methods=['POST', 'GET'])
def sales():
    if request.method == 'GET':
        query = select(Sale)
        sales_list = session.scalars(query)
        result = []
        for i in sales_list:
            item = {
                'id': i.id,
                'user_id': i.user_id,
                'date_sold': i.date_sold
            }
            result.append(item)
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.get_json()
        
        # Check for empty input
        if not data or not data['user_id'] or not data['date_sold']:
            return jsonify({'Message': 'Ensure all fields are set'}), 400
        
        date_sold = date.fromisoformat(data['date_sold'])
        new_sale = Sale(
            user_id=data['user_id'],
            date_sold=date_sold
        )
        session.add(new_sale)
        session.commit()
        return jsonify({'Message': 'Sale Added Successfully'}), 201

    else:
        return jsonify({'Message': 'Method Not Allowed'}), 405






@app.route('/sale-details', methods=['POST', 'GET'])
def sale_detail():
    if request.method == 'GET':
        query = select(Sale_detail)
        sales_details = session.scalars(query)
        result = []
        for i in sales_details:
            item = {
                'id': i.id,
                'product_id': i.product_id,
                'sale_id': i.sale_id,
                'quantity': i.quantity,
                'amount': i.amount
            }
            result.append(item)
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.get_json()
        
        # Check for empty input
        if not data or not data['product_id'] or not data['sale_id'] or not data['quantity'] or not data['amount']:
            return jsonify({'message': 'All fields are required'}), 400

        new_sale_detail = Sale_detail(
            product_id=data['product_id'],
            sale_id=data['sale_id'],
            quantity=data['quantity'],
            amount=data['amount']
        )
        session.add(new_sale_detail)
        session.commit()
        return jsonify({'Message': 'Sale Added Successfully'}), 201

    else:
        return jsonify({'message': 'method not allowed'}), 405






@app.route('/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'GET':
        query = select(Payment)
        payments = session.scalars(query)
        result = []
        for i in payments:
            item = {
                'id': i.id,
                'sale_id': i.sale_id,
                'date_paid': i.date_paid
            }
            result.append(item)
        return jsonify(result), 200
        
    elif request.method == 'POST':
        data = request.get_json()
        
        # Check for empty input
        if not data or not data['sale_id'] or not data['date_paid']:
            return jsonify({'message': 'All fields are required'}), 400

        date_paid = date.fromisoformat(data['date_paid'])
        new_payment = Payment(
            sale_id=data['sale_id'],
            date_paid=date_paid
        )
        session.add(new_payment)
        session.commit()
        return jsonify({'Message': 'Payment Added Successfully'}), 201

    else:
        return jsonify({'message': 'method not allowed'}), 405

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
        pass
    elif request.method=='POST':
        login_data=request.get_json()
        if not login_data['password'] or not login_data['email']:
            res={'error':'ensure all fields are set'}
            res=jsonify(res),405
        else:
            trial=login_data['email']
            query=select(User).where(User.email==trial)
            user=session.scalars(query).first()
            if not user:
                res={'Error':'User not found'}
                return redirect(url_for('login'))

                
            else:
                # password=bcrypt.generate_password_hash(login_data['password']).decode('utf-8')
                if bcrypt.check_password_hash(user.password,login_data['password']):
                    user_id={'id':user.id}
                         
                    return jsonify(user_id),201
    else:
        res={'error':'method not allowed'}
    return jsonify(res)
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        data=request.get_json()
        res=None
        if not data['full_name'] or not data['password'] or not data['email']:
            res={'Error':'all fields are required'}
            return jsonify(res),403
        else:
            password=data['password']
            hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
            new_user=User(
                full_name=data['full_name'],
                email=data['email'],
                password=hashed_password
            )
        session.add(new_user)
        session.commit()
        res={'Success':'user added successfully'}
        return jsonify(res),201
    
    elif request.method=='GET':
        pass
    else:
        res={'Error':'Method not allowed'}
        res=jsonify(res),405
    return res
app.run(debug=True)