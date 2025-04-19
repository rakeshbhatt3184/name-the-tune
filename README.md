# 🎵 Name the Tune

A mini-project where users guess song titles based on partial lyrics. Built using **Flask** and **MongoDB Atlas**. Ideal for learning backend APIs, database integration, and basic game logic.

---

## 🚀 Features

- 🎶 Randomly shows a song lyric snippet  
- 🧠 Users guess the correct song title  
- 🧾 Stores and tracks user scores  
- 🏆 Leaderboard for top scorers  
- ☁️ Uses MongoDB Atlas for cloud database  
- 🔐 Credentials securely managed with `.env`  

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **Database**: MongoDB Atlas (NoSQL)  
- **Testing**: Postman  

---

## 📁 API Endpoints

### `GET /`
Check if backend is running

### `GET /get_snippet`
Returns a random song lyric snippet

### `POST /submit_guess`
```json
{
  "snippet": "partial lyrics here",
  "guess": "your guess"
}
