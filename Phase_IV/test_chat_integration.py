import requests
import json
import uuid
import time
from jose import jwt

# Configuration
API_URL = "http://127.0.0.1:8000"
SECRET = "PrkNWTriWNtT6lO+L/R2WufIiY9cshUs6HjiiGSW1xU="  # From .env
USER_ID = "test-user-gemini-integration"

def generate_token():
    payload = {"sub": USER_ID}
    return jwt.encode(payload, SECRET, algorithm="HS256")

def test_chat_flow():
    token = generate_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"Testing with User ID: {USER_ID}")

    # 1. Create Conversation
    print("\n1. Creating Conversation...")
    try:
        response = requests.post(
            f"{API_URL}/api/chat/conversations",
            json={"title": "Integration Test"},
            headers=headers
        )
        if response.status_code != 200:
            print(f"Failed to create conversation: {response.text}")
            return

        conversation = response.json()
        conversation_id = conversation["id"]
        print(f"Success! Conversation ID: {conversation_id}")
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return

    # 2. Send Message to Create Task
    print("\n2. Sending Message: 'Create a task to buy groceries'...")
    try:
        response = requests.post(
            f"{API_URL}/api/chat/{conversation_id}/messages",
            json={
                "message": "Create a task to buy groceries",
                "tools_enabled": True
            },
            headers=headers
        )

        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
            return # Don't return, check if partial failure? No, strict check.

        chat_response = response.json()
        print("Response received from Chatbot.")
        print(f"Message ID: {chat_response['message_id']}")
        print(f"Content: {chat_response['content']}")

        if chat_response.get("function_calls"):
            print("Function Calls executed:")
            for fc in chat_response['function_calls']:
                print(f" - {fc['name']}: {fc['arguments']}")

        if chat_response.get("function_responses"):
            print("Function Responses:")
            for fr in chat_response['function_responses']:
                print(f" - {fr['name']}: {fr['result']}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

    # 3. Verify Task Creation
    print("\n3. Verifying Task Creation via Task API...")
    try:
        response = requests.get(
            f"{API_URL}/api/tasks",
            headers=headers
        )

        if response.status_code != 200:
            print(f"Failed to list tasks: {response.text}")
            return

        tasks = response.json()
        found = False
        for task in tasks:
            if "buy groceries" in task["title"].lower():
                print(f"SUCCESS! Task found: {task['id']} - {task['title']}")
                found = True
                break

        if not found:
            print("FAILURE! Created task was not found in the list.")
            print("Current tasks:", tasks)

    except Exception as e:
        print(f"Error fetching tasks: {e}")

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server...")
    time.sleep(5)
    test_chat_flow()
