# AI Engineer Journey 🤖

**Mohammed Haroon Khan** · Robotics & AI Engineer · Bengaluru, India

A structured, project-first journey from Python fundamentals to production AI systems.  
Every folder = a working project. Every commit = real learning.

---

## 🚀 Projects built

### P5 — AI Document Q&A System
> HuggingFace Transformers · Sentence Transformers · FAISS · DistilBERT · Gradio · Python

A complete RAG (Retrieval Augmented Generation) pipeline:
- Upload any PDF → extracts and chunks text automatically
- Embeds chunks using Sentence Transformers (all-MiniLM-L6-v2)
- Indexes with FAISS for fast semantic similarity search
- Extracts precise answers using DistilBERT QA model
- Clean Gradio web UI with confidence scoring — runs 100% on CPU

**Run it:**
```bash
cd projects/p5-pdf-qa
pip install gradio transformers sentence-transformers faiss-cpu PyMuPDF torch
python app.py
# Open http://localhost:7860
```

---

### P4 — SamBot: AI Chatbot Web App
> Python · Flask · Groq API · LLaMA 3.3 70B · HTML/CSS/JS

A full-stack conversational AI assistant with:
- Real conversation memory — context persists across full session
- Clean chat bubble web UI with typing indicators
- REST API backend with Flask
- Secure API key management via OS environment variables

**Run it:**
```bash
cd projects/p4-sambot
pip install flask groq
python app.py
# Open http://localhost:5000
```

---

### P3 — Student Grade Calculator
> Python · Functions · File I/O · Conditions

- Multi-subject grade calculator with A+ grading scale
- Best/worst subject detection using max/min
- Conditional report saving to file
- Performance message based on average

---

### P2 — Number Guessing Game
> Python · Loops · Random · Game logic

- Adaptive hint system (too high / too low)
- Score system based on attempts used
- Play again loop with full game reset

---

### P1 — Temperature Converter
> Python · Functions · Type conversion · Input validation

- Celsius ↔ Fahrenheit ↔ Kelvin
- Input validation and unit normalisation
- Clean formatted output

---

## 📚 Phase 1 — Python for AI (completed)

| Lesson | Topic | Key concepts |
|---|---|---|
| L1 | Variables & data types | str, int, float, bool, type conversion |
| L2 | Lists, loops, conditions | for/while, enumerate, filtering |
| L3 | Functions & modules | def, return, docstrings, imports |
| L4 | NumPy for AI | Arrays, vectorised ops, shapes, broadcasting |
| L5 | Pandas for data | DataFrame, cleaning, groupby, feature engineering |
| L6 | Matplotlib | Training curves, heatmaps, confusion matrix, dashboard |
| L7 | OOP for AI pipelines | Classes, inheritance, AIDataPipeline class |

---

## 🛠️ Stack used

`Python 3.12` `Flask` `Groq API` `LLaMA 3.3` `HuggingFace Transformers` `Sentence Transformers` `FAISS` `DistilBERT` `Gradio` `NumPy` `Pandas` `Matplotlib` `Scikit-learn` `OpenCV`

---

## 📁 Structure

```
ai-engineer-journey/
├── projects/
│   ├── p1-temp-converter/
│   ├── p2-guessing-game/
│   ├── p3-grade-calculator/
│   ├── p4-sambot/          ← AI chatbot web app
│   └── p5-pdf-qa/          ← RAG document Q&A system
├── phase1/                  ← Python fundamentals
└── phase2/                  ← ML (in progress)
```

---

## Author

**Mohammed Haroon Khan**  
Robotics & AI Engineer · B.E. Robotics & Automation · Rajarajeswari College of Engineering, Bengaluru  
[LinkedIn](https://www.linkedin.com/in/haroon-khan-43031531a) · [GitHub](https://github.com/haroonkhan20)