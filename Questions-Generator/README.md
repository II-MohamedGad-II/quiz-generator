# Multi-PDF RAG-Based MCQ Generator

## 📚 Project Overview

This project is designed to integrate with the backend of an educational platform, providing teachers and instructors with an automated system for generating customized quizzes for students. The goal is to assist in student evaluation by creating tailored multiple-choice quizzes based on individual performance in previous lectures.

The quiz content and distribution are dynamically generated, with questions selected and weighted according to the student's historical performance and degrees.

## 🚀 Features

- **Multi-PDF Upload Support:** Upload multiple PDF resources as input material.
- **Intelligent Text Processing:** Automatic text extraction and normalization.
- **Chunk Splitting:** Splits large documents into manageable chunks for efficient processing.
- **Custom Quiz Generation:** Generates 20 MCQs per batch, with exactly four options and a correct answer labeled with a degree score.
- **Performance-Based Customization:** Quiz content is adjusted based on student scores from previous lectures.
- **Structured Output:** Questions, options, and correct answers are neatly structured for easy integration.

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (for the interactive UI)
- **pdfplumber** (for PDF extraction)
- **LangChain** (for prompt handling)
- **Ollama** (for local LLM generation)

## 🏁 Getting Started

### 1. Clone the Repository:

```bash
git clone https://github.com/II-MohamedGad-II/quiz-generator.git
cd quiz-generator/Questions-Generator
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

### 4. Run the Application:

```bash
streamlit run MCQ_Generator.py
```

The app will run locally, and you can access it at [localhost:8501](http://localhost:8501).

### 5. Upload PDF Documents:

Upload your learning materials (PDF format) and let the system generate customized quizzes.

## 🧠 How It Works

1. **Upload PDFs:** The app reads and extracts text from the uploaded files.
2. **Text Preprocessing:** The extracted content is cleaned and split into chunks.
3. **Quiz Generation:** The system uses an LLM (via Ollama) to generate 20 MCQs.
4. **Result Structuring:** The generated quiz is presented in a structured format, ready for integration into the platform.
5. **Performance-Based Distribution:** Instructors can use student scores from previous lectures to influence question difficulty and selection.



## 🤝 Contributing

Feel free to fork the repository, submit issues, or make pull requests. Let’s build an even smarter quiz generation tool together!
