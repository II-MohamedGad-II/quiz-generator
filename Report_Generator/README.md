# Student Performance Report Generator

## 📚 Project Overview
This project is designed to enhance the educational experience by generating personalized student performance reports. By analyzing students' scores in previous lectures, the system provides detailed feedback, identifies areas of improvement, and suggests study strategies to help students perform better in future exams.

## 🚀 Features
- **Performance Analysis:** Analyzes scores to detect strengths and weaknesses.
- **Detailed Reports:** Generates structured reports with section-wise feedback.
- **Actionable Recommendations:** Suggests study techniques, learning resources, and time management tips.
- **PDF Support:** Loads PDF documents for additional context or study material.
- **Interactive UI:** Built with Streamlit for easy data input and report generation.

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (for the interactive UI)
- **LangChain** (for prompt handling)
- **Ollama** (for local LLM generation)
- **PDFPlumber** (for PDF extraction)

## 🏁 Getting Started

### 1. Clone the Repository:
```bash
git clone https://github.com/II-MohamedGad-II/quiz-generator.git
cd quiz-generator/Report_Generator
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
streamlit run Report_Generator.py
```

The app will run locally, and you can access it at [localhost:8501](http://localhost:8501).

## 🧠 How It Works
1. **Input Scores:** Enter student scores for each lecture or subject.
2. **Analyze Performance:** The app uses an LLM to analyze scores and generate a report.
3. **Generate Report:** The generated report includes an overall performance summary, subject-wise analysis, and tailored recommendations.
4. **PDF Integration:** Optionally, upload lecture PDFs for question generation or content analysis.

## 📄 Example Output
The generated report includes:

1. **Overall Performance Summary:** Highlights strengths, weaknesses, and score trends.
2. **Subject-Wise Analysis:** Evaluates each subject with improvement suggestions.
3. **Actionable Recommendations:** Offers strategies like practice tests, revision schedules, and learning resources.

## 📂 File Structure
Your file can be found in the following path within the repository:

📂 quiz-generator
└── 📂 Report_Generator
    └── 📄 [Report_Generator.py](https://github.com/II-MohamedGad-II/quiz-generator/blob/main/Report_Generator/Report_Generator.py)

## 🤝 Contributing
Feel free to fork the repository, submit issues, or make pull requests. Let’s refine the report generator together!

---
Let me know if you’d like any adjustments! 🚀

