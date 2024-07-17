from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from functools import wraps
import pymysql
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# JWT configuration
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this to a strong key
app.config['JWT_SECRET_KEY'] = 'supersecretjwtkey'  # Change this to a strong key

jwt = JWTManager(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # replace with your MySQL root password
    'database': 'master',
    'cursorclass': pymysql.cursors.DictCursor
}

# Load the tokenizer and model
tokenizer_dir = "../model/saved_tokenizers/alger-ia_dziribert_sentiment"
model_dir = "../model/saved_models/alger-ia_dziribert_sentiment"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
print("Loading model...")
model = AutoModelForSequenceClassification.from_pretrained(model_dir)

# Database connection function
def get_db_connection():
    connection = pymysql.connect(**DB_CONFIG)
    return connection

# Create the necessary tables if they don't exist
def create_tables():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                disease VARCHAR(255),
                comments TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comment_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                comment TEXT,
                predicted_sentiment VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                chat_data TEXT,
                predicted_sentiment VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        connection.commit()
    connection.close()

# Call create_tables function to ensure tables are created
create_tables()

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    disease = data.get('disease')
    
    hashed_password = generate_password_hash(password)
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Check if email already exists
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"msg": "Email already registered"}), 400
        
        # Insert new user
        cursor.execute("""
            INSERT INTO user (full_name, email, password, disease)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, hashed_password, disease))
        connection.commit()
    connection.close()
    
    return jsonify({"msg": "User registered successfully"}), 201

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()
    connection.close()
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"msg": "Bad email or password"}), 401
    
    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token), 200

# Protected route for analyzing sentiment in comments
@app.route('/analyze_comment', methods=['POST'])
@jwt_required()
def analyze_comment():
    data = request.get_json()
    text = data.get('text')
    user_id = get_jwt_identity()
    
    if not text:
        return jsonify({"msg": "No text provided"}), 400
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    sentiment = torch.argmax(predictions, dim=-1).item()
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO comment_analysis (user_id, comment, predicted_sentiment)
            VALUES (%s, %s, %s)
        """, (user_id, text, str(sentiment)))
        connection.commit()
    connection.close()
    
    return jsonify({"sentiment": sentiment}), 200

# Protected route for analyzing sentiment in chat data
@app.route('/analyze_chat', methods=['POST'])
@jwt_required()
def analyze_chat():
    data = request.get_json()
    chat_data = data.get('chat_data')
    user_id = get_jwt_identity()
    
    if not chat_data:
        return jsonify({"msg": "No chat data provided"}), 400
    
    inputs = tokenizer(chat_data, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    sentiment = torch.argmax(predictions, dim=-1).item()
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO chat_analysis (user_id, chat_data, predicted_sentiment)
            VALUES (%s, %s, %s)
        """, (user_id, chat_data, str(sentiment)))
        connection.commit()
    connection.close()
    
    return jsonify({"sentiment": sentiment}), 200

@app.route('/random_verse', methods=['GET'])
def get_random_verse():
    url = "https://api.quran.com/api/v4/verses/random"
    headers = {
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        verse_data = response.json()
        return jsonify(verse_data)
    else:
        return jsonify({"error": "Unable to fetch verse"}), response.status_code
    
    
if __name__ == '__main__':
    app.run(debug=True)
