# Quiz and Performance Management System

## 📚 Project Overview
This repository contains a complete solution for managing student evaluations in an educational platform. It includes two main components:

1. **MCQ Generator:** Automatically generates multiple-choice questions from uploaded lecture PDFs, customizing the quiz content based on student performance in previous lectures.
2. **Performance Report Generator:** Creates detailed performance reports for students, analyzing scores and providing personalized recommendations to enhance learning.

Together, these tools help instructors create tailored learning experiences, track student progress, and continuously optimize the educational process.

## 📂 Project Structure

```
quiz-generator/
├── 📂 Questions-Generator
│   ├── MCQ_Generator.py
│   └── README.md
│
├── 📂 Report_Generator
│   ├── Report_Generator.py
│   └── README.md
│
└── 📄 README.md  <-- (This file)
```

## 🚀 Features
- **Customized Quizzes:** Generates dynamic quizzes based on lecture content and student scores.
- **Detailed Reports:** Analyzes student performance and suggests personalized improvement strategies.
- **PDF Processing:** Extracts content from uploaded PDFs for question generation.
- **Interactive UI:** Built with Streamlit for easy data input, quiz generation, and report display.
- **Local LLM Support:** Uses Ollama for fast and secure local language model inference.

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **LangChain**
- **Ollama**
- **pdfplumber**

## 🏁 Getting Started

### 1. Clone the Repository:
```bash
git clone https://github.com/II-MohamedGad-II/quiz-generator.git
cd quiz-generator
```

### 2. Create a Virtual Environment:
```bash
python -m venv venv
```

Activate the environment:
- **Windows:**
```bash
.\venv\Scripts\Activate
```
- **Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the Applications:

#### 📘 MCQ Generator:
```bash
cd Questions-Generator
streamlit run MCQ_Generator.py
```

#### 📝 Report Generator:
```bash
cd ../Report_Generator
streamlit run Report_Generator.py
```

## 🎯 Workflow
1. **Generate Quizzes:** Upload lecture PDFs and student scores. The system generates a quiz customized to the student's previous performance.
2. **Evaluate Student Performance:** After students complete their quizzes, input their scores into the report generator.
3. **Analyze and Improve:** The report generator provides a detailed performance analysis, highlighting strengths, weaknesses, and areas to improve.

## 📄 Example Use Case
- A teacher uploads lecture slides in PDF format.
- The MCQ Generator creates a quiz tailored to each student’s strengths and weaknesses.
- After students take the quiz, their scores are fed into the Report Generator.
- The system generates a comprehensive performance report, complete with personalized recommendations.

## 🤝 Contributing
Want to improve the system? Feel free to fork the repository, submit issues, or make pull requests. Let’s make learning smarter together!

---
Let me know if you want me to refine anything or add more sections! 🚀

