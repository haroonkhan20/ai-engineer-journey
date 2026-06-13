# app.py
# Project 5 — AI Document Q&A System
# Built by: Mohammed Haroon Khan
# Stack: HuggingFace Transformers · Sentence Transformers · FAISS · Gradio
# Architecture: PDF → extract → chunk → embed → FAISS index → DistilBERT QA

import fitz                          # PyMuPDF — extracts text from PDF
import faiss                         # vector similarity search
import numpy as np
import gradio as gr
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ── STEP 1: Load models ───────────────────────
# These download once and cache locally (~500MB total)
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
# all-MiniLM-L6-v2: fast, lightweight, excellent for semantic search

print("Loading QA model...")
qa_model = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad"
)
# DistilBERT: 40% smaller than BERT, 97% of performance, runs on CPU

print("Models loaded!")

# ── STEP 2: PDF text extraction ───────────────
def extract_text(pdf_file):
    """
    Extract all text from a PDF file.
    fitz (PyMuPDF) is faster and more accurate than pdfminer.

    Parameters:
        pdf_file: uploaded file path from Gradio
    Returns:
        str: full text of the PDF
    """
    doc  = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# ── STEP 3: Chunking ──────────────────────────
def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into overlapping chunks.
    Overlap ensures answers aren't cut across chunk boundaries.

    Parameters:
        text       (str): full document text
        chunk_size (int): words per chunk
        overlap    (int): words shared between consecutive chunks
    Returns:
        list of str: text chunks
    """
    words  = text.split()
    chunks = []
    start  = 0

    while start < len(words):
        end   = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap   # overlap keeps context

    return chunks

# ── STEP 4: Build FAISS index ─────────────────
def build_index(chunks):
    """
    Embed all chunks and build a FAISS index for fast similarity search.
    This is the core of RAG — finding relevant context for a question.

    Parameters:
        chunks (list): text chunks to index
    Returns:
        tuple: (faiss_index, embeddings array)
    """
    print(f"Embedding {len(chunks)} chunks...")

    # Convert each chunk to a 384-dim vector
    embeddings = embedder.encode(
        chunks,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    # Normalise for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build flat L2 index — exact search, good for <10k chunks
    dimension = embeddings.shape[1]   # 384 for MiniLM
    index     = faiss.IndexFlatIP(dimension)   # Inner Product = cosine after normalisation
    index.add(embeddings)

    print(f"FAISS index built — {index.ntotal} vectors")
    return index, embeddings

# ── STEP 5: Retrieve relevant chunks ──────────
def retrieve(question, index, chunks, top_k=5):
    """
    Find the most relevant chunks for a question using semantic search.

    Parameters:
        question (str): user's question
        index: FAISS index
        chunks (list): original text chunks
        top_k (int): how many chunks to retrieve
    Returns:
        list of str: most relevant chunks
    """
    # Embed the question
    q_vec = embedder.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(q_vec)

    # Search — returns distances and indices
    distances, indices = index.search(q_vec, top_k)

    # Return the actual text chunks
    return [chunks[i] for i in indices[0] if i < len(chunks)]

# ── STEP 6: Extract answer ────────────────────
def get_answer(question, context_chunks):
    """
    Use DistilBERT to extract the exact answer span from context.

    Parameters:
        question      (str): user's question
        context_chunks (list): relevant text chunks from FAISS
    Returns:
        tuple: (answer str, confidence float)
    """
    # Combine top chunks into one context string
    context = " ".join(context_chunks)

    # DistilBERT finds the answer span within context
    result = qa_model(
        question=question,
        context=context,
        max_answer_len=100
    )

    return result["answer"], round(result["score"] * 100, 2)

# ── GLOBAL STATE ──────────────────────────────
# Stores the index and chunks for the current PDF
state = {
    "chunks" : None,
    "index"  : None,
    "loaded" : False,
    "filename": ""
}

# ── GRADIO FUNCTIONS ──────────────────────────
def process_pdf(pdf_file):
    """Called when user uploads a PDF."""
    if pdf_file is None:
        return "Please upload a PDF file."

    try:
        # Extract text
        text   = extract_text(pdf_file)
        if len(text.strip()) < 100:
            return "PDF appears to be empty or image-based (no extractable text)."

        # Chunk it
        chunks = chunk_text(text, chunk_size=300, overlap=50)

        # Build FAISS index
        index, _ = build_index(chunks)

        # Save to global state
        state["chunks"]   = chunks
        state["index"]    = index
        state["loaded"]   = True
        state["filename"] = pdf_file.split("\\")[-1].split("/")[-1]

        return (f"✅ PDF loaded successfully!\n\n"
                f"📄 File: {state['filename']}\n"
                f"📝 Text extracted: {len(text.split())} words\n"
                f"🔢 Chunks created: {len(chunks)}\n"
                f"🧠 FAISS index built: {index.ntotal} vectors\n\n"
                f"Now ask any question about this document!")

    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def answer_question(question):
    """Called when user asks a question."""
    if not state["loaded"]:
        return "Please upload a PDF first!", ""

    if not question.strip():
        return "Please type a question!", ""

    try:
        # Retrieve relevant chunks
        relevant = retrieve(question, state["index"], state["chunks"], top_k=5)

        # Get answer
        answer, confidence = get_answer(question, relevant)

        # Format confidence
        if confidence >= 80:
            conf_label = f"🟢 High confidence: {confidence}%"
        elif confidence >= 50:
            conf_label = f"🟡 Medium confidence: {confidence}%"
        else:
            conf_label = f"🔴 Low confidence: {confidence}% — try rephrasing"

        return answer, conf_label

    except Exception as e:
        return f"Error: {str(e)}", ""

# ── GRADIO UI ─────────────────────────────────
with gr.Blocks(
    title="AI Document Q&A",
    theme=gr.themes.Soft()
) as app:

    gr.Markdown("""
    # 🤖 AI Document Q&A System
    **Built by Mohammed Haroon Khan**
    Upload any PDF → Ask questions → Get AI-powered answers
    *Stack: HuggingFace Transformers · Sentence Transformers · FAISS · DistilBERT*
    """)

    with gr.Row():
        # Left column — upload
        with gr.Column(scale=1):
            gr.Markdown("### 📄 Step 1 — Upload PDF")
            pdf_input  = gr.File(
                label="Upload PDF",
                file_types=[".pdf"]
            )
            upload_btn = gr.Button("Process PDF", variant="primary")
            status_box = gr.Textbox(
                label="Status",
                lines=8,
                interactive=False
            )

        # Right column — Q&A
        with gr.Column(scale=1):
            gr.Markdown("### ❓ Step 2 — Ask Questions")
            question_input = gr.Textbox(
                label="Your question",
                placeholder="e.g. What is the main topic of this document?",
                lines=2
            )
            ask_btn    = gr.Button("Get Answer", variant="primary")
            answer_box = gr.Textbox(
                label="Answer",
                lines=4,
                interactive=False
            )
            conf_box   = gr.Textbox(
                label="Confidence",
                lines=1,
                interactive=False
            )

            gr.Markdown("""
            **Example questions to try:**
            - What is this document about?
            - Who is the author?
            - What are the main conclusions?
            - What methodology was used?
            """)

    # ── Wire up buttons ───────────────────────
    upload_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=[status_box]
    )

    ask_btn.click(
        fn=answer_question,
        inputs=[question_input],
        outputs=[answer_box, conf_box]
    )

    # Also trigger on Enter key
    question_input.submit(
        fn=answer_question,
        inputs=[question_input],
        outputs=[answer_box, conf_box]
    )

if __name__ == "__main__":
    print("Starting AI Document Q&A System...")
    print("Open your browser at: http://localhost:7860")
    app.launch(
        server_name="localhost",
        server_port=7860,
        share=False        # set True to get a public URL
    )