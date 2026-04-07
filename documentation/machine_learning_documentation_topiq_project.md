# 📘 Machine Learning Documentation — Topiq Project

## 🔹 Introduction

This document explains how Machine Learning (ML) is used in the Topiq project in a simple and clear way. The system does not use heavy deep learning; instead, it uses lightweight and practical ML techniques to improve search and recommendation quality.

---

# 🧠 Where ML is Used in the Project

Machine Learning is used in two main parts:

1. **Smart Topic Search (TF-IDF + Cosine Similarity)**
2. **Resource Ranking System (Scoring + Feedback Learning)**

---

# 🔍 1. Smart Topic Search

## 📌 Problem
Users may type queries in different ways:
- "dead lock"
- "deadlock"
- "os deadlock"

A simple keyword search may fail.

## ✅ Solution: TF-IDF + Cosine Similarity

### 🔹 What is TF-IDF?
TF-IDF (Term Frequency–Inverse Document Frequency) converts text into numbers so that the system can understand importance of words.

### 🔹 How it Works

#### Step 1: Prepare Topic Text
Each topic is converted into a combined text:

Example:
```
Binary Tree + tags + keywords + description
```

#### Step 2: Convert to Vectors
Text → Numerical vectors

```
"binary tree" → [0.2, 0.8, 0.1 ...]
```

#### Step 3: Convert User Query

```
"tree" → [0.1, 0.7, 0.2 ...]
```

#### Step 4: Calculate Similarity

Cosine similarity is used:

```
similarity = cosine(query_vector, topic_vector)
```

The topic with the **highest similarity score** is selected.

---

## 🎯 Example

User input:
```
dead lock problem
```

System matches with:
```
Deadlock (Operating System)
```

Even though spelling is different, system understands meaning.

---

# 📊 2. Resource Ranking System

After selecting the best topic, the system ranks resources.

## 📌 Formula Used

```
score = (rating × 0.4) + (normalized_views × 0.3) + (feedback_score × 0.3)
```

---

## 🔹 Features Used

### 1. Rating
- Indicates quality
- Higher rating → better rank

### 2. View Count
- Indicates popularity
- Normalized for fairness

### 3. Feedback Score
- Based on user actions
- Helpful 👍 / Not Helpful 👎

---

## 🎯 Example Table

| Video | Rating | Views | Feedback | Result |
|------|--------|-------|----------|--------|
| A | 4.8 | High | Low | Medium |
| B | 4.5 | Medium | High | High |

👉 Even if rating is lower, high feedback can boost ranking.

---

# 🔄 3. Feedback Learning (Adaptive System)

## 📌 How it Works

1. User clicks **Helpful / Not Helpful**
2. System updates counts
3. Score recalculated
4. Future ranking improves

---

## 🎯 Example

Initially:
```
Video A > Video B
```

After feedback:
```
Video B > Video A
```

👉 System learns from user interaction

---

# ⚠️ 4. Cold Start Problem

## 📌 Problem
At the beginning:
- No feedback available

## ✅ Solution Used

System relies on:
- Rating
- View count

Additionally, seed data includes initial values to simulate real-world behavior.

---

# 🧪 ML Techniques Used

| Technique | Purpose |
|----------|--------|
| TF-IDF | Convert text into vectors |
| Cosine Similarity | Match query with topics |
| Weighted Scoring | Rank resources |
| Feedback Loop | Improve over time |

---

# 🚀 How the Whole System Works

```
User Query
   ↓
TF-IDF Vectorization
   ↓
Cosine Similarity Matching
   ↓
Best Topic Selected
   ↓
Fetch Resources
   ↓
Apply Ranking Formula
   ↓
Return Top 3 Videos + Articles
```

---

# 💬 Viva Ready Explanation

**Short Answer:**

"We use TF-IDF and cosine similarity for intelligent query matching, and a weighted scoring system with user feedback for adaptive resource ranking."

---

# 🎯 Conclusion

The project uses lightweight machine learning techniques to:
- Understand user queries
- Match relevant topics
- Rank resources intelligently
- Improve results over time using feedback

👉 This makes the system smarter than simple keyword search.

---

✅ End of Documentation

