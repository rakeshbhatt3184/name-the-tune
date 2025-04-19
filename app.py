from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["name_the_tune"]
songs_col = db["songs"]
users_col = db["users"]

@app.route('/')
def home():
    return "🎵 Name the Tune backend is running!"


@app.route('/get_snippet', methods=['GET'])
def get_snippet():
    song = songs_col.aggregate([{"$sample": {"size": 1}}]) 
    song = list(song)
    if song:
        return jsonify({"snippet": song[0]["snippet"], "song_id": str(song[0]["_id"])})
    return jsonify({"message": "No songs found"}), 404

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    data = request.json
    snippet = data.get("snippet", "").strip()
    guess = data.get("guess", "").strip().lower()
    
    song = songs_col.find_one({"snippet": snippet})
    if song and song["title"].strip().lower() == guess:
        return jsonify({"correct": True, "title": song["title"]})
    return jsonify({"correct": False})

@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.json.get("username", "").strip()
    if users_col.find_one({"username": username}):
        return jsonify({"message": "User already exists"})
    users_col.insert_one({"username": username, "highest_score": 0})
    return jsonify({"message": "User registered successfully"})

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    username = data.get("username", "").strip()
    new_score = data.get("score", 0)
    
    user = users_col.find_one({"username": username})
    if user and new_score > user.get("highest_score", 0):
        users_col.update_one({"username": username}, {"$set": {"highest_score": new_score}})
    return jsonify({"message": "Score updated"})

@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    top_users = list(users_col.find({}, {"_id": 0}).sort("highest_score", -1).limit(10))
    return jsonify(top_users)

if __name__ == '__main__':
    app.run(debug=True)
