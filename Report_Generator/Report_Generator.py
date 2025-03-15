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
