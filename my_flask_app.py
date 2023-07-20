from flask import Flask, jsonify
from my_database_module import get_resource_data

app = Flask(__name__)

@app.route('/get_resource_data', methods=['GET'])
def resource_data():
    data = get_resource_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
