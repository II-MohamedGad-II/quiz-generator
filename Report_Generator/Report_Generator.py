import streamlit as st
import tempfile
import os
import random
import re
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define language model
LANGUAGE_MODEL = OllamaLLM(model="deepseek-r1:1.5b")

PROMPT_TEMPLATE = """
You are an expert assistant specializing in educational question generation.  
Your task is to generate 20 multiple-choice questions (MCQs) from the provided document.  
Each question should have four answer choices (A, B, C, D), with one correct answer labeled at the end as 'Correct Answer'.  
Don't output your think and just output **only** the questions and answer choices and what is the correct answer in the following format be like:

**Question 2:**
question?

A) option a
B) option b
C) option c
D) option d

Correct Answer: C) option c

Now, generate 20 MCQs based on the provided document and keep all questions like the format mentioned.

Context: {context_text}
"""

# Define the function to generate the student performance report
def generate_report(*degrees):
    """Generates a detailed student performance report based on exam scores."""
    
    # Create a dictionary for lecture scores
    scores = {f'Lec{i+1}': degrees[i] for i in range(len(degrees))}
    
    # Define the prompt
    prompt_template = """
    You are an expert educational assistant. Your task is to generate a detailed student performance report based on their exam scores.  

    ### **Instructions:**  
    - Analyze the student's performance in each exam.  
    - Identify strengths and weaknesses based on the scores.  
    - Provide insights on areas that need improvement.  
    - Suggest study strategies for better performance in future exams.  
    - Keep the report structured, clear, and professional.  

    ### **Student Exam Scores:**  
    {scores}  

    ### **Expected Report Output:**  
    1. **Overall Performance Summary:**  
       - Mention the student's strongest and weakest subjects.  
       - Compare their performance across different subjects.  

    2. **Subject-Wise Analysis:**  
       - For each subject, provide a brief evaluation.  
       - If the score is above 85, praise their strong understanding.  
       - If the score is between 60-85, suggest improvement strategies.  
       - If the score is below 60, highlight urgent areas to work on.  

    3. **Actionable Recommendations:**  
       - Suggest learning techniques (e.g., practice tests, revision strategies).  
       - Recommend specific resources (e.g., books, online courses).  
       - Encourage time management tips for exam preparation.  

    Now, generate a **personalized performance report** based on the provided scores.
    """

    # Use ChatPromptTemplate to format the prompt
    conversation_prompt = ChatPromptTemplate.from_template(prompt_template)


    # Invoke the model with the formatted prompt
    response_chain = conversation_prompt | LANGUAGE_MODEL
    return response_chain.invoke({"scores": scores})

# =================================================================================================================================
# Load PDFs
def load_pdf_documents(file_path):
    """Load PDF document using PDFPlumber."""
    document_loader = PDFPlumberLoader(file_path)
    return document_loader.load()

# =================================================================================================================================
# Chunking
def chunk_documents(raw_documents):
    """Split the document into manageable chunks."""
    text_processor = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_processor.split_documents(raw_documents)

# =================================================================================================================================
# Generate questions from document
def generate_questions_from_document(document_chunks):
    """Generate questions based on the document's content."""
    selected_chunks = document_chunks[:5]  # Only take first 5 chunks (adjust as needed)
    context_text = "\n\n".join([doc.page_content for doc in selected_chunks])
    conversation_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    return response_chain.invoke({"context_text": context_text})

# =================================================================================================================================
# Extract questions from model output
def extract(text):
    pattern = r'\*\*Question (\d+):\*\*\s*(.*?)\nA\)\s*(.*?)\nB\)\s*(.*?)\nC\)\s*(.*?)\nD\)\s*(.*?)\nCorrect Answer:\s*(.*?)\n'
    questions_dict = {}
    matches = re.findall(pattern, text, re.DOTALL)
    for match in matches:
        question_number = int(match[0])
        question = match[1].strip()
        options = {
            'A': match[2].strip(),
            'B': match[3].strip(),
            'C': match[4].strip(),
            'D': match[5].strip(),
        }
        correct_answer = match[6].strip()
        questions_dict[question_number] = {
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        }
    return questions_dict

# =================================================================================================================================
# Adjust question keys
def adjust_keys(dictionary):
    return {i + 1: v for i, (_, v) in enumerate(dictionary.items())}

# =================================================================================================================================
# Generate questions from uploaded PDFs
def process_uploaded_files(uploaded_files):
    all_quizzes = {}
    for i, uploaded_file in enumerate(uploaded_files):
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        temp_path = os.path.normpath(temp_path)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        raw_docs = load_pdf_documents(temp_path)
        processed_chunks = chunk_documents(raw_docs)
        soup = generate_questions_from_document(processed_chunks)
        questions = extract(soup)
        questions = adjust_keys(questions)
        all_quizzes[f'Lec{i+1}'] = questions
    return all_quizzes

# =================================================================================================================================
# Distribute questions based on scores
def distribute_questions(weighted_dict, total_questions=11):
    total_weight = sum(weighted_dict.values()) or 1  # Avoid division by zero
    allocated = {k: max(2, min(9, round((v / total_weight) * total_questions))) for k, v in weighted_dict.items()}
    diff = total_questions - sum(allocated.values())
    keys = sorted(weighted_dict, key=weighted_dict.get, reverse=True)
    for _ in range(abs(diff)):
        for k in keys:
            if (diff > 0 and allocated[k] < 9) or (diff < 0 and allocated[k] > 2):
                allocated[k] += 1 if diff > 0 else -1
                diff += 1 if diff < 0 else -1
                if diff == 0:
                    break
    return allocated

# =================================================================================================================================
# Generate final distribution
def final_distribution(all_quizzes, numLec, *degrees):
    scores = {f'Lec{i+1}': abs((degrees[i]/2)-9.5) for i in range(len(all_quizzes)-1)}
    score = distribute_questions(scores)  
    score[f'Lec{len(all_quizzes)}'] = 9
    return score

# =================================================================================================================================
# Random question selection
def miniquiz(quiz, numQues):
    return [quiz[i] for i in random.sample(range(1, len(quiz)), numQues)]

# =================================================================================================================================
# Collect final exam
def collection(dictionary, all_quizzes):
    return {i: miniquiz(all_quizzes[i], dictionary[i]) for i in dictionary}

# =================================================================================================================================
# Streamlit UI
# st.title("📄 MCQ Exam Generator")

# uploaded_files = st.file_uploader("Upload Lecture PDFs", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     degrees_input = st.text_input("Enter previous scores separated by commas (e.g., 10, 15, 20)")
#     if degrees_input:
#         degrees = list(map(int, degrees_input.split(',')))
#         all_quizzes = process_uploaded_files(uploaded_files)
#         distrib = final_distribution(all_quizzes, len(all_quizzes)-1, *degrees)
#         final_exam = collection(distrib, all_quizzes)
#         st.subheader("Generated Exam")
#         for lec, questions in final_exam.items():
#             st.write(f"### {lec}")
#             for q in questions:
#                 st.write(f"**Q: {q['question']}**")
#                 for opt, ans in q['options'].items():
#                     st.write(f"{opt}) {ans}")
#                 st.write(f"✅ Correct Answer: {q['correct_answer']}")
#                 st.write("---")
st.title("Student Performance Report Generator")
st.write("Enter the scores for each subject to generate a detailed performance report.")

scores = []
if "subjects" not in st.session_state:
    st.session_state["subjects"] = []

if st.button("Add Subject"):
    st.session_state["subjects"].append(0)

for i in range(len(st.session_state["subjects"])):
    st.session_state["subjects"][i] = st.number_input(f"Enter score for Subject {i+1}:", min_value=0, max_value=100, step=1, value=st.session_state["subjects"][i])

if st.button("Generate Report"):
    with st.spinner("Generating Report..."):
        report = generate_report(*st.session_state["subjects"])
        st.subheader("Performance Report:")
        report = report.split("</think>", 1)[1].strip()
        st.write(report)
