# Rest Api- This is a backend route that follows the four rules below
# It has to have a route 
# It has to have a method (POST/GET/PUT/DELETE)
# It has to have a status code
# It has to return data as JSON
from sqlalchemy import create_engine, select
import sentry_sdk

from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from models import Base, Product, Purchase, User, Sale, Sale_detail, Payment
from sqlalchemy.orm import Session
from datetime import date 
from flask_bcrypt import Bcrypt
from flask import redirect, url_for
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_cors import CORS

sentry_sdk.init(
    dsn="https://6fadeab3e9a236d53adbad8eefef34ee@o4512051738443776.ingest.us.sentry.io/4512057171509248",
    integrations=[FlaskIntegration()],
    send_default_pii=True,
    enable_logs=True,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace"
)
# Test Sentry immediately on app launch
sentry_sdk.capture_message("Sentry test message on startup!")

app = Flask(__name__)

# Configure CORS globally for all routes and origins
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = 'awfegjenhingvrhuigbt54iucn'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Create a database using sqlalchemy engine
engine = create_engine("sqlite:///./flask_duka_api.db", echo=True)

# Create tables into the database using sqlalchemy
Base.metadata.create_all(engine)

# Create a session to do sql transaction 
session = Session(engine)

alloweed_methods = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

@app.before_request
def before_request():
    # Bypass heavy db operations for CORS preflight OPTIONS requests
    if request.method == 'OPTIONS':
        return
    print('A new request is coming:', request.path)

@app.route("/sentry-message")
def trigger_message():
    sentry_sdk.capture_message("Hello from Flask! Sentry test message.")
    return "Message sent to Sentry!"

@app.route('/')
def home():
    if request.method == 'GET':
        data = {'Flask API': 'success'}
        return jsonify(data), 200
    else:
        error = {'Error': 'Method not allowed'}
        return jsonify(error), 405

@app.route('/products', methods=alloweed_methods)
@jwt_required()
def products(): 
    email = get_jwt_identity()
    user = session.scalars(select(User).where(User.email == email)).first()
    if request.method == 'GET':
        query = select(Product)
        products_list = session.scalars(query)
        results = []
        for prod in products_list:
            p = {
                'id': prod.id,
                'user_id': prod.user_id,
                'buying_price': prod.buying_price,
                'selling_price': prod.selling_price
            }
            results.append(p)
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.get_json(silent=True) or {}
        
        if not data.get('buying_price') or not data.get('selling_price'):
            error = {'Error': 'Ensure all fields are set'}
            return jsonify(error), 400
        
        new_product = Product(
            user_id=data.get('id'),
            buying_price=float(data['buying_price']),
            selling_price=float(data['selling_price'])
        )
        session.add(new_product)
        session.commit()
        return jsonify({'Message': 'New product added'}), 201

    else:
        error = {'Error': 'Method not allowed'}
        return jsonify(error), 405

@app.route('/purchases', methods=alloweed_methods)
@jwt_required()
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
        data = request.get_json(silent=True) or {}
        
        if not data.get('product_id') or not data.get('date_purchased') or not data.get('purchase_price'):
            return jsonify({'Message': 'Ensure all fields are set'}), 400
        
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

@app.route('/sales', methods=alloweed_methods)
@jwt_required()
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
        data = request.get_json(silent=True) or {}
        
        if not data.get('user_id') or not data.get('date_sold'):
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

@app.route('/sale-details', methods=alloweed_methods)
@jwt_required()
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
        data = request.get_json(silent=True) or {}
        
        if not data.get('product_id') or not data.get('sale_id') or not data.get('quantity') or not data.get('amount'):
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

@app.route('/payment', methods=alloweed_methods)
@jwt_required()
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
        data = request.get_json(silent=True) or {}
        
        if not data.get('sale_id') or not data.get('date_paid'):
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

@app.route('/login', methods=alloweed_methods)
def login():
    if request.method == 'OPTIONS':
        return '', 200

    if request.method == 'POST':
        login_data = request.get_json(silent=True) or {}
        email = login_data.get('email')
        password = login_data.get('password')
        
        if not password or not email:
            return jsonify({'error': 'ensure all fields are set'}), 400
            
        query = select(User).where(User.email == email)
        user = session.scalars(query).first()
        
        if not user:
            return jsonify({'Error': 'User not found'}), 404
            
        if bcrypt.check_password_hash(user.password, password):
            token = create_access_token(identity=email)
            return jsonify({'id': user.id, 'token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    return jsonify({'error': 'method not allowed'}), 405

@app.route('/register', methods=alloweed_methods)
def register():
    if request.method == 'OPTIONS':
        return '', 200

    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        if not full_name or not password or not email:
            return jsonify({'Error': 'all fields are required'}), 400

        # Check for existing user
        existing_user = session.scalars(select(User).where(User.email == email)).first()
        if existing_user:
            return jsonify({'error': 'user already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password
        )

        try:
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            return jsonify({'error': 'database insertion failed'}), 500

        token = create_access_token(identity=email)
        res = {
            'message': 'user registered successfully',
            'token': token
        }
        return jsonify(res), 201
    
    return jsonify({'Error': 'Method not allowed'}), 405
app.run(debug=True)