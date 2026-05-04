from flask import Flask, request, jsonify, render_template
import ollama

app = Flask(__name__)


chat_history = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user = data["user"]
    message = data["message"]

    if user not in chat_history:
        chat_history[user] = []

    chat_history[user].append({"role": "user", "content": message})

    response = ollama.chat(
        model="llama3",
        messages=chat_history[user]
    )

    reply = response['message']['content']

    chat_history[user].append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

app.run(debug=True)