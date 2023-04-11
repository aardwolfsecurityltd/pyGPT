import requests
import json
import threading
import sys
import time

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + YOUR_API_KEY
}


def hourglass_animation(seconds):
    for i in range(seconds):
        time.sleep(1)
        sys.stdout.write('\r')
        sys.stdout.write("Loading... " + "|" * i + " " * (seconds - i) + " |")
        sys.stdout.flush()


conversation_history = []

while True:
    message = input("Enter your message (or type 'exit' to quit, 'reset' to reset the chat): ")

    if message == "exit":
        break
    elif message == "reset":
        conversation_history = []
        print("Chat history cleared. You can start a new conversation now.")
        continue

    conversation_history.append({"role": "user", "content": message})

    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation_history,
        "temperature": 0.7
    }

    # Display hourglass animation while waiting for response
    loading = threading.Thread(target=hourglass_animation, args=(5,))
    loading.start()

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    content = response_json["choices"][0]["message"]["content"]

    # Stop hourglass animation
    loading.join()
    print("\n")
    print(content)
    print("\n")

    conversation_history.append({"role": "assistant", "content": content})
