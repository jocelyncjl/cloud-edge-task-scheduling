from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    alert = request.get_json()
    print("Received alert:", alert)

    subprocess.run(['python3', 'migrate_pod.py'])

    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


    