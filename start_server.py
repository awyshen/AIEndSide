from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from intent_recognition import IntentRecognizer
import threading

app = Flask(__name__)
CORS(app)

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=False, enable_cache=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recognize', methods=['POST'])
def recognize_intent():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': '请输入查询内容'}), 400
    
    result = recognizer.recognize(query)
    return jsonify(result)

@app.route('/api/batch_test', methods=['POST'])
def batch_test():
    data = request.get_json()
    queries = data.get('queries', [])
    
    results = []
    for query in queries:
        result = recognizer.recognize(query)
        results.append({
            'query': query,
            'result': result
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
