# 🤖 CodSoft AI Internship — All Tasks
**Author:** Your Name  
**Batch:** CodSoft AI Internship  
**GitHub Repo:** CODSOFT

---

## 📋 Task Overview

| Task | Topic | Key Concepts | Difficulty |
|------|-------|-------------|------------|
| 1 | Rule-Based Chatbot | Regex, Pattern Matching, NLP basics | ⭐⭐ |
| 2 | Tic-Tac-Toe AI | Minimax, Alpha-Beta Pruning, Game Theory | ⭐⭐⭐ |
| 3 | Image Captioning | Computer Vision, Transformers, BLIP | ⭐⭐⭐⭐ |
| 4 | Recommendation System | Collaborative & Content-Based Filtering | ⭐⭐⭐ |
| 5 | Face Detection & Recognition | OpenCV, CNN, dlib | ⭐⭐⭐⭐ |

---

## 🚀 Quick Start

### Task 1 — Chatbot
```bash
python task1_chatbot.py
```
No dependencies needed beyond Python 3.x!

### Task 2 — Tic-Tac-Toe AI
```bash
python task2_tictactoe.py
```
No dependencies needed!

### Task 3 — Image Captioning
```bash
pip install transformers pillow torch requests
python task3_image_captioning.py                          # demo
python task3_image_captioning.py --image photo.jpg        # local file
python task3_image_captioning.py --url https://...        # from URL
```

### Task 4 — Recommendation System
```bash
pip install pandas numpy scikit-learn
python task4_recommendation.py
```

### Task 5 — Face Detection
```bash
pip install opencv-python numpy
pip install face-recognition   # optional — requires cmake + dlib
python task5_face_detection.py --mode webcam
python task5_face_detection.py --mode image --input photo.jpg
python task5_face_detection.py --mode register --name "Alice" --image alice.jpg
```

---

## 📁 File Structure
```
CODSOFT/
├── task1_chatbot.py
├── task2_tictactoe.py
├── task3_image_captioning.py
├── task4_recommendation.py
├── task5_face_detection.py
└── README.md
```
