# 🧠 AI Resume Analyzer & Job Matcher 🔍

An intelligent web app built using **Flask** that compares your **resume** with a **job description** using **TF-IDF** and **cosine similarity** to calculate a matching percentage. Designed with a futuristic glassmorphism UI and supports PDF, DOCX, and TXT resume formats.

![AI Resume Matcher UI](https://imgur.com/your-screenshot.png) <!-- Optional: Add your own hosted image -->

---

## ✨ Features

- 📝 Upload Resume (PDF, DOCX, TXT)
- 🧾 Paste Job Description or Keywords
- 🤖 Calculates match score using NLP (TF-IDF + Cosine Similarity)
- 📊 Result shown as a percentage
- 💫 Clean, responsive UI with animated CSS background
- 🔐 File size limit: 5MB

---

## 📦 Technologies Used

- **Python 3**
- **Flask**
- **scikit-learn** (`TfidfVectorizer`, `cosine_similarity`)
- **docx2txt** – Extract text from `.docx` files
- **PyPDF2** – Extract text from `.pdf` files
- **HTML + CSS (Glassmorphism)**

---

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-resume-matcher.git
   cd ai-resume-matcher
