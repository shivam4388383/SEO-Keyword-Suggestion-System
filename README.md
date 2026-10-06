# SEO Keyword Suggestion System

## 1. Project Overview

The SEO Keyword Suggestion System is a web-based application that generates related SEO keywords from a user-provided topic and analyzes social-media-style textual data using sentiment analysis.

The system combines keyword analysis with sentiment analysis to provide simple data-driven insights through an interactive dashboard.

---

## 2. Objectives

- Generate related SEO keyword suggestions.
- Calculate estimated keyword relevance scores.
- Analyze social-media-style textual data.
- Classify text into Positive, Neutral, and Negative sentiment.
- Display sentiment distribution using visualization.
- Recommend the highest-scoring keyword.
- Maintain recent keyword search history.

---

## 3. Main Features

- Keyword suggestion
- Keyword word-count analysis
- Estimated keyword score
- Sentiment analysis
- Positive/Neutral/Negative classification
- Sentiment doughnut chart
- Keyword recommendation
- Search history
- Responsive web interface

---

## 4. Technologies Used

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### Backend
- Python
- Flask
- Flask-CORS

### Data Processing
- Pandas

### Natural Language Processing
- NLTK
- TextBlob

### Database
- SQLite

---

## 5. System Architecture

User
↓
Frontend Dashboard
↓
Flask REST API
↓
Keyword Suggestion Engine
↓
Keyword Analysis
↓
Social Media Dataset
↓
Sentiment Analysis
↓
Visualization & Recommendation
↓
Search History

---

## 6. Project Structure

```text
SEO-Keyword-Suggestion-System/
│
├── .vscode/
│   └── settings.json
│
├── backend/
│   ├── app.py
│   ├── keyword_engine.py
│   ├── analyzer.py
│   ├── sentiment_engine.py
│   └── sentiment_analyzer.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   └── social_media_data.csv
│
├── models/
│
├── search_history.db
│
├── requirements.txt
│
└── README.md