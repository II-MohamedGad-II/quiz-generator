import streamlit as st
import io
import re
import json
from concurrent.futures import ThreadPoolExecutor
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

LANGUAGE_MODEL = OllamaLLM(model="deepseek-coder:33b")

PROMPT_TEMPLATE = """
You are an expert assistant specializing in educational question generation.  
Generate at least **20 multiple-choice questions (MCQs)** based on the provided content.  
Strict guidelines:  
- Questions must come directly from the document content.  
- Each question must have **4 distinct answer choices (A, B, C, D)**.  
- Label the correct answer as **"correct_answer"**.  
- **Return only valid JSON output**.  

Context (Document Content):  
{context_text}  

Expected Output (Valid JSON Format Only):  

```json
[
  {{
    "question": "Example question?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "B) Option 2" # Ensure this is always provided
  }}
]
``` 
"""


def clean_text(text):
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_pdf_documents(file_bytes, file_name):
    try:
        with io.BytesIO(file_bytes) as file_stream:
            temp_file_name = f"temp_{file_name.replace(' ', '_')}"
            with open(temp_file_name, "wb") as f:
                f.write(file_stream.read())
            document_loader = PDFPlumberLoader(temp_file_name)
            return document_loader.load()
    except Exception as e:
        st.error(f"Failed to load {file_name}: {e}")
        return None


def filter_pages(raw_documents):
    return [doc for doc in raw_documents if len(doc.page_content.strip()) > 100]


def adaptive_split(raw_documents):
    total_length = sum(len(doc.page_content) for doc in raw_documents)
    chunk_size = min(2000, max(500, total_length // 20))
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=200, add_start_index=True)
    return splitter.split_documents(raw_documents)


def extract_questions(text):
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


def generate_questions_from_document(document_chunks):
    selected_chunks = document_chunks[:5]
    context_text = clean_text("\n\n".join([doc.page_content for doc in selected_chunks]))
    conversation_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    return response_chain.invoke({"context_text": context_text})


def generate_additional_questions(existing_questions, document_chunks):
    while len(existing_questions) < 10:
        response = generate_questions_from_document(document_chunks)
        new_questions = extract_questions(response)
        existing_questions.update(new_questions)


st.title("📘 PDF to MCQ Generator")
st.write("Upload one or more PDFs, and generate at least 10 MCQs for each!")

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    results = {}
    for uploaded_file in uploaded_files:
        st.write(f"Processing: {uploaded_file.name}... ⏳")

        try:
            uploaded_file.seek(0)
            file_bytes = uploaded_file.read()

            raw_docs = load_pdf_documents(file_bytes, uploaded_file.name)
            if not raw_docs:
                continue

            filtered_docs = filter_pages(raw_docs)
            processed_chunks = adaptive_split(filtered_docs)
            st.write("Document split into adaptive chunks. Generating questions... 🧠")

            response = generate_questions_from_document(processed_chunks)
            questions = extract_questions(response)

            if len(questions) < 10:
                st.warning(f"⚠️ Only {len(questions)} questions generated. Generating more to reach 10...")
                generate_additional_questions(questions, processed_chunks)

            results[uploaded_file.name] = questions
            st.success(f"✅ {len(questions)} questions generated for {uploaded_file.name}")

        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {e}")

    if results:
        st.json(results)
        st.download_button(
            label="📥 Download Questions as JSON",
            data=json.dumps(results, indent=2),
            file_name="mcq_questions.json",
            mime="application/json"
        )

st.write("Upload more PDFs or refine your content for fresh questions! 🚀")

if __name__ == '__main__':
    st.write("Ready to generate educational content with AI? 🚀")

