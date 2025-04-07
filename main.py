from flask import Flask, request, jsonify
import json
import requests
import google.auth
from google.oauth2 import service_account
import datetime

app = Flask(__name__)

# Load service account
SERVICE_ACCOUNT_FILE = 'your-firebase-service-account.json'
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def get_access_token():
    request_now = google.auth.transport.requests.Request()
    credentials.refresh(request_now)
    return credentials.token

def send_fcm(fcm_token, title, body):
    url = 'https://fcm.googleapis.com/v1/projects/healthy-42950/messages:send'
    access_token = get_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }

    payload = {
        "message": {
            "token": fcm_token,
            "notification": {
                "title": title,
                "body": body
            },
            "android": {
                "priority": "high"
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route('/send-fcm', methods=['POST'])
def send_fcm_route():
    data = request.json
    fcm_token = data.get("fcm_token")
    title = data.get("title", "No Title")
    body = data.get("body", "No Body")

    if not fcm_token:
        return jsonify({"error": "Missing fcm_token"}), 400

    result = send_fcm(fcm_token, title, body)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run()
