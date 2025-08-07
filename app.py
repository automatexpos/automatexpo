from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)

# Ensure log directory exists
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/consultation', methods=['POST'])
def consultation():
    try:
        data = request.json
        
        # Create structured data
        consultation_entry = {
            'timestamp': datetime.now().isoformat(),
            'name': data.get('name', 'N/A'),
            'email': data.get('email', 'N/A'),
            'topic': data.get('topic', 'N/A')
        }
        
        # Save as formatted text
        log_file = os.path.join(LOG_DIR, 'consultations.txt')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{'='*50}\n")
            f.write(f"Date: {consultation_entry['timestamp']}\n")
            f.write(f"Name: {consultation_entry['name']}\n")
            f.write(f"Email: {consultation_entry['email']}\n")
            f.write(f"Message:\n{consultation_entry['topic']}\n")
            f.write(f"{'='*50}\n\n")
        
        # Also save as JSON for easy parsing
        json_file = os.path.join(LOG_DIR, 'consultations.json')
        consultations = []
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                consultations = json.load(f)
        
        consultations.append(consultation_entry)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(consultations, f, indent=2, ensure_ascii=False)
        
        print(f"Consultation saved: {consultation_entry['name']} - {consultation_entry['email']}")
        
        return jsonify({
            "status": "success", 
            "message": "Thank you! We'll contact you within 24 hours."
        })
        
    except Exception as e:
        print(f"Error saving consultation: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "Something went wrong. Please try again."
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)