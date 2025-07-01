from flask import Flask, request, render_template_string
import os
import tempfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
import PyPDF2

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload


def extract_text(file_path):
    """Extract text from PDF or DOCX or TXT"""
    if file_path.endswith('.pdf'):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:  # txt or others
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def analyze_resume_vs_job(resume_text, job_text):
    # Basic similarity using TF-IDF + cosine similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_text])
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(cosine_sim * 100, 2)  # in percentage
    return score


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AI Resume Analyzer & Job Matcher</title>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap" rel="stylesheet" />

    <style>
        /* Reset & basics */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body, html {
            height: 100%;
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
            background: #0f2027;  /* fallback */
            background: linear-gradient(135deg, #203a43, #2c5364);
            color: #eee;
        }

        /* 3D Animated Background using CSS */
        body::before {
            content: "";
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background:
                radial-gradient(circle at 40% 30%, #00ffd5aa, transparent 30%),
                radial-gradient(circle at 70% 80%, #007bff88, transparent 30%),
                radial-gradient(circle at 20% 70%, #ff00ff88, transparent 20%);
            animation: moveBackground 20s linear infinite;
            filter: blur(80px);
            z-index: -1;
            transform-style: preserve-3d;
        }

        @keyframes moveBackground {
            0% {
                transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg);
            }
            50% {
                transform: translate3d(10%, 10%, 0) rotateX(15deg) rotateY(15deg);
            }
            100% {
                transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg);
            }
        }

        .container {
            max-width: 720px;
            margin: 50px auto;
            background: rgba(255, 255, 255, 0.07);
            padding: 30px;
            border-radius: 20px;
            box-shadow:
                0 8px 32px 0 rgba(31, 38, 135, 0.37),
                0 0 0 1px rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        h1 {
            font-weight: 600;
            text-align: center;
            margin-bottom: 25px;
            letter-spacing: 2px;
            color: #00ffd5;
            text-shadow: 0 0 6px #00ffd5aa;
        }

        label {
            font-weight: 600;
            display: block;
            margin-bottom: 8px;
            margin-top: 20px;
            color: #00ffd5cc;
        }

        textarea, input[type="file"] {
            width: 100%;
            padding: 15px 18px;
            border-radius: 15px;
            border: none;
            outline: none;
            font-size: 1rem;
            color: #0f2027;
            font-weight: 500;
            background: #fff;
            box-shadow:
                inset 2px 2px 6px #b8b9be,
                inset -4px -4px 6px #ffffff;
            transition: box-shadow 0.3s ease;
        }

        textarea:focus, input[type="file"]:focus {
            box-shadow:
                inset 1px 1px 3px #007bff,
                inset -1px -1px 3px #00ffd5;
        }

        /* Stylish Button */
        button {
            margin-top: 30px;
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #00ffd5, #007bff);
            border: none;
            border-radius: 25px;
            font-size: 1.2rem;
            font-weight: 700;
            color: #fff;
            cursor: pointer;
            box-shadow:
                0 4px 15px #00ffd5aa,
                0 8px 40px #007bffcc;
            transition: all 0.3s ease;
        }

        button:hover {
            box-shadow:
                0 8px 20px #00ffd5ff,
                0 15px 50px #007bffff;
            transform: scale(1.05);
        }

        .result-box {
            margin-top: 30px;
            padding: 25px;
            border-radius: 18px;
            background: #0f2027;
            box-shadow:
                0 0 15px #00ffd5aa,
                0 0 40px #007bffcc;
            font-size: 1.3rem;
            text-align: center;
            font-weight: 600;
            color: #00ffd5;
            letter-spacing: 1.2px;
            user-select: none;
        }

        .error-msg {
            margin-top: 20px;
            padding: 15px;
            background: #ff3860cc;
            border-radius: 15px;
            font-weight: 700;
            text-align: center;
            color: white;
            user-select: none;
            box-shadow: 0 0 8px #ff3860bb;
        }

        footer {
            margin-top: 50px;
            text-align: center;
            color: #00ffd5aa;
            font-size: 0.9rem;
            user-select: none;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                margin: 20px;
                padding: 25px;
            }
            button {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Resume Analyzer & Job Matcher</h1>
        {% if error %}
            <div class="error-msg">{{ error }}</div>
        {% endif %}
        <form method="POST" enctype="multipart/form-data" autocomplete="off">
            <label for="resume">Upload Your Resume (PDF, DOCX, TXT)</label>
            <input type="file" id="resume" name="resume" accept=".pdf,.docx,.txt" required />

            <label for="job_desc">Paste Job Description / Keywords</label>
            <textarea id="job_desc" name="job_desc" rows="6" placeholder="Enter job description or keywords here..." required>{{ job_desc or '' }}</textarea>

            <button type="submit">Analyze & Match</button>
        </form>

        {% if score is defined %}
            <div class="result-box">
                Matching Score: <span>{{ score }}%</span>
            </div>
        {% endif %}
    </div>

    <footer>Made with 💙</footer>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_desc = request.form.get('job_desc')
        resume_file = request.files.get('resume')

        if not job_desc or not resume_file:
            error = "Please provide both resume and job description."
            return render_template_string(HTML_TEMPLATE, error=error)

        temp_dir = tempfile.gettempdir()
        filename = resume_file.filename.lower()
        file_path = os.path.join(temp_dir, filename)
        resume_file.save(file_path)

        try:
            resume_text = extract_text(file_path)
            if not resume_text.strip():
                raise Exception("Could not extract text from resume.")
        except Exception as e:
            error = f"Error processing resume: {str(e)}"
            if os.path.exists(file_path):
                os.remove(file_path)
            return render_template_string(HTML_TEMPLATE, error=error, job_desc=job_desc)

        score = analyze_resume_vs_job(resume_text, job_desc)

        if os.path.exists(file_path):
            os.remove(file_path)

        return render_template_string(HTML_TEMPLATE, score=score, job_desc=job_desc)

    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    app.run(debug=True)
