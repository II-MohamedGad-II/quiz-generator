import streamlit as st
import pdfplumber
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
import ollama

# Initialize the LLM
LANGUAGE_MODEL = lambda prompt: ollama.generate(model="deepseek-coder:6.7b", prompt=prompt)["response"]

# Define prompt template
PROMPT_TEMPLATE = """
You are an expert assistant specializing in educational question generation.  
Your task is to generate **at least 20 multiple-choice questions (MCQs)** from the provided document, focusing on key concepts, definitions, and practical knowledge.  

### **Strict Guidelines:**  
- Generate questions **directly based on the document content** to ensure accuracy and relevance.  
- **Do NOT generate questions outside the given context.**  
- Each question must have exactly **4 distinct answer choices (A, B, C, D)**.  
- Clearly label the correct answer as **"correct_answer"**.  
- **Do NOT** include explanations, reasoning, or any extra text.  
- If unsure, **skip ambiguous or unclear sections** instead of guessing.  

Context (Document Content):  
{context_text}  

### **Expected Output (Valid JSON Format Only):**  

Return the result **strictly as valid JSON**, like this:  

```json
[
  {{
    "question": "Which SQL clause is used to filter rows based on a specified condition?",
    "options": ["A) ORDER BY", "B) WHERE", "C) GROUP BY", "D) HAVING"],
    "correct_answer": "B) WHERE"
  }},
  {{
    "question": "What is the purpose of a foreign key in a relational database?",
    "options": ["A) To enforce unique values in a column", "B) To establish a relationship between tables", "C) To store binary data", "D) To define a table’s primary identifier"],
    "correct_answer": "B) To establish a relationship between tables"
  }}
]
Additional Requirements:
Content Coverage: Cover a range of topics (e.g., SQL queries, normalization, indexes, joins, constraints, etc.).
Difficulty Levels: Mix easy, medium, and hard questions for balanced assessment.
Validation: Double-check the JSON format for validity and completeness.
Question Count: Generate a minimum of 20 questions — more are welcome, but not fewer.
If the content is insufficient for 20 questions, extract multiple questions per key concept or combine related points to meet the quota.

Do not change the structure or format. Return the questions directly as a JSON array, ready for parsing and saving to a file.
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
    text = text.strip()
    matches = re.findall(r'\{\s*"question".*?\}', text, re.DOTALL)
    
    questions_dict = {}
    
    for idx, match in enumerate(matches, start=1):
        try:
            question_data = json.loads(match)
            questions_dict[idx] = {
                "question": question_data.get("question", ""),
                "options": question_data.get("options", []),
                "correct_answer": question_data.get("correct_answer", "")
            }
        except json.JSONDecodeError:
            continue
    
    return questions_dict

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
