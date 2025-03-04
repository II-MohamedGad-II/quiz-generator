import streamlit as st
import pdfplumber
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
import ollama

# Initialize the LLM
LANGUAGE_MODEL = lambda prompt: ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)["response"]

# Define prompt template
PROMPT_TEMPLATE = """
You are an expert assistant specializing in educational question generation.  
Your task is to generate exactly 20 multiple-choice questions (MCQs) from the provided document.  

### **Strict Guidelines:**  
- Each question must have exactly four answer choices (A, B, C, D).  
- One correct answer should be labeled at the end with a numerical degree (1-100).  
- Do **not** include explanations, reasoning, or any extra text.  
- The format **must** be followed exactly without any deviation.  

### **Expected Format (Strictly Follow This):**  

**Question 1**  
question?  

A) option a  
B) option b  
C) option c  
D) option d  

Correct Answer: C) option c (85)

**Question 2**  
question?  

A) option a  
B) option b  
C) option c  
D) option d  

Correct Answer: B) option b (90)

(Continue this pattern for all 20 MCQs and **don't change any letter or space**.)  

**Context:**  
{context_text}  
"""

def load_pdfs(files):
    """Extracts text from multiple uploaded PDF files."""
    text = ""
    for file in files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    return text

def normalize_text(text):
    """Cleans and normalizes extracted text."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text):
    """Splits text into smaller chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_text(text)

def generate_mcqs(context_text):
    """Generates MCQs using the LLM."""
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt.format(context_text=context_text)
    
    response = LANGUAGE_MODEL(formatted_prompt)  # Direct function call, no .invoke()
    
    return response



def extract_mcqs(text):
    """Extracts MCQs into structured format with numerical degrees."""
    pattern = r'\*\*Question \d+\*\*\s+(.*?)\s+\nA\) (.*?)\s+\nB\) (.*?)\s+\nC\) (.*?)\s+\nD\) (.*?)\s+\n\nCorrect Answer: (A|B|C|D)\) (.*?) \((\d+)\)'
    mcqs = re.findall(pattern, text, re.DOTALL)
    structured_mcqs = []
    for mcq in mcqs:
        structured_mcqs.append({
            'question': mcq[0].strip(),
            'options': {
                'A': mcq[1].strip(),
                'B': mcq[2].strip(),
                'C': mcq[3].strip(),
                'D': mcq[4].strip(),
            },
            'correct_answer': mcq[5].strip(),
            'degree': int(mcq[7].strip())
        })
    return structured_mcqs

# Streamlit UI
st.title("📚 MCQ Generator")
st.write("Upload PDF documents and generate multiple-choice questions!")

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    st.success("PDFs uploaded successfully!")
    
    # Extract and process the documents
    raw_text = load_pdfs(uploaded_files)
    normalized_text = normalize_text(raw_text)
    chunks = chunk_text(normalized_text)
    
    st.write("✅ Documents processed successfully!")
    
    # Generate MCQs
    st.write("🔍 Generating MCQs...")
    while True:
        generated_text = generate_mcqs("\n\n".join(chunks[:5]))  # Use first 5 chunks
        mcqs = extract_mcqs(generated_text)
        
        if len(mcqs) > 13:
            st.write("Done ✅")
            break
        else:
            st.write("--")
    
    st.write("🎯 **Generated MCQs:**")
    for i, mcq in enumerate(mcqs, start=1):
        st.write(f"**Question {i}:** {mcq['question']}")
        st.write(f"A) {mcq['options']['A']}")
        st.write(f"B) {mcq['options']['B']}")
        st.write(f"C) {mcq['options']['C']}")
        st.write(f"D) {mcq['options']['D']}")
        st.write(f"✅ **Correct Answer:** {mcq['correct_answer']} ({mcq['degree']})")
        st.write("---")
