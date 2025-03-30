import os
import csv
import base64
import pandas as pd
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import requests
from PIL import Image
import io
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Groq API configuration
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Store conversation history
conversation_history = []
csv_data = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_csv_files():
    """Load all CSV files from the data directory"""
    global csv_data
    data_dir = 'data'
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir} directory. Please add your CSV files there.")
        return
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_dir, filename)
            try:
                df = pd.read_csv(file_path)
                csv_data[filename] = df.to_dict(orient='records')
                print(f"Loaded {filename} with {len(df)} records")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

def encode_image(image_path):
    """Encode image to base64 for API request"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_groq(image_path):
    """Send image to Groq for analysis"""
    base64_image = encode_image(image_path)
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",  # Use a model that supports image analysis
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that analyzes images and provides detailed descriptions."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please analyze this image and describe what you see in detail."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 500
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "Sorry, I couldn't analyze the image. Please try again."

def query_groq(messages):
    """Send query to Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Add CSV context to system message
    csv_context = "Here's the data from CSV files you can reference:\n"
    for filename, data in csv_data.items():
        csv_context += f"\n--- {filename} ---\n"
        # Limit to first 5 records to avoid token limits
        for i, record in enumerate(data[:5]):
            csv_context += f"Record {i+1}: {json.dumps(record)}\n"
    
    system_message = {
        "role": "system",
        "content": f"""You are a helpful assistant that analyzes library data and explains insights in plain language.

IMPORTANT INSTRUCTIONS:
1. DO NOT generate SQL code or queries in your responses
2. ALWAYS respond in plain English without code snippets
3. Provide direct answers based on your understanding of the data
4. Format responses using Markdown for readability (bold, lists, etc.)
5. If calculations are needed, perform them yourself and show only the results
6. Focus on insights that would be valuable to librarians

{csv_context}"""
    }
    
    # Prepare messages for API
    api_messages = [system_message] + messages
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": api_messages,
        "temperature": 0.2,  # Lower temperature for more focused responses
        "max_tokens": 800
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error querying Groq: {e}")
        return "Sorry, I encountered an error. Please try again."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analyze the image
        analysis = analyze_image_with_groq(file_path)
        
        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": [
                {"type": "text", "text": "I uploaded an image for analysis."}
            ]
        })
        
        conversation_history.append({
            "role": "assistant",
            "content": analysis
        })
        
        return jsonify({
            "message": "File uploaded successfully",
            "analysis": analysis,
            "filename": filename
        })
    
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        file_path = os.path.join('data', filename)
        file.save(file_path)
        
        # Load the newly uploaded CSV
        try:
            df = pd.read_csv(file_path)
            csv_data[filename] = df.to_dict(orient='records')
            
            # Add to conversation history
            conversation_history.append({
                "role": "user",
                "content": f"I uploaded a CSV file named {filename}."
            })
            
            conversation_history.append({
                "role": "assistant",
                "content": f"I've loaded your CSV file '{filename}' with {len(df)} records. You can now ask questions about this data."
            })
            
            return jsonify({
                "message": "CSV file uploaded successfully",
                "filename": filename,
                "records": len(df),
                "response": f"I've loaded your CSV file '{filename}' with {len(df)} records. You can now ask questions about this data."
            })
        except Exception as e:
            return jsonify({"error": f"Error processing CSV: {str(e)}"}), 400
    
    return jsonify({"error": "File type not allowed. Please upload a CSV file."}), 400

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Add user message to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Get response from Groq
    response = query_groq(conversation_history)
    
    # Add assistant response to conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response
    })
    
    return jsonify({"response": response})

@app.route('/reset', methods=['POST'])
def reset_conversation():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation reset successfully"})

if __name__ == '__main__':
    load_csv_files()
    app.run(debug=True)
