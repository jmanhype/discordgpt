# server.py
from flask import Flask, request, jsonify
from flask_caching import Cache
import openai
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import logging

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
logging.basicConfig(level=logging.INFO)

openai.api_key = 'your-openai-api-key'

@cache.memoize(timeout=3600)  # Cache results for 1 hour
def get_openai_embedding(text, model="text-daidav-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

@app.route('/get_embedding', methods=['POST'])
def get_embedding():
    try:
        data = request.get_json()
        text = data.get('text')
        embedding = get_openai_embedding(text)
        return jsonify({'embedding': embedding.tolist()})
    except Exception as e:
        logging.error(f"Failed to get embedding: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict_outcome', methods=['POST'])
def predict_outcome():
    try:
        data = request.get_json()
        embedding = np.array(data.get('embedding'))
        model = joblib.load('model.joblib')
        prediction = model.predict([embedding])
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        logging.error(f"Failed to predict outcome: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/retrain_model', methods=['POST'])
def retrain_model():
    try:
        data = request.get_json()
        embeddings = np.array(data.get('embeddings'))
        outcomes = np.array(data.get('outcomes'))
        model = RandomForestRegressor(n_estimators=100)
        model.fit(embeddings, outcomes)
        joblib.dump(model, 'model.joblib')
        return jsonify({'message': 'Model retrained successfully.'})
    except Exception as e:
        logging.error(f"Failed to retrain model: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
