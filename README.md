# SFK — Strive For Knowledge

- An AI-powered study tool built in Python using the Gemini API. Ingest notes from text files, PDFs, or images, generate targeted practice questions across 37 types, get graded feedback, and track your performance through an analytics pipeline with session history and weakness ranking.

## Features:

- Multi-source ingestion — Notes can be text files, PDFs, and images; with the ability to combine multiple documents for richer context
- Auto-detection — Auto-detects notes and generated files, with manual entry always available
- 37 question types — Analytical, written, selected response, and STEM-specific formats with difficulty scaling from 1–10
- Weak topic targeting — Optionally pull your 10 weakest topics from past performance to focus generation where you need it most
- AI-powered grading — Detailed feedback and explanations on every answer
- Performance analytics — Topic weakness ranking, trend detection, and weighted averages
- Session history — Review of past sessions; option to review full question, answer, and grade detail
- Persistent session database — Stores every question, answer, grade, and explanation across all sessions for long-term tracking and review

## Setup & Usage:

  You first need to install the required libraries. You can do this by running the following in your terminal:
	```
	pip install -r requirements.txt
	```
  You will then need to create an environmental variable. You can do this by creating a text document titled .env (you can have the .txt extension) in the folder. Then, in the text document, type "GEMINI_API_KEY=[your Gemini key]."

  Finally, in your terminal, run: "python menu.py". From there, you will be asked if you'd like to generate questions, grade your answers, generate analytics, or view session history.

  For note files, please keep the format somewhat simple using the format including just the subject and keywords like "notes, unit, chapter, textbook, slides" and similar keywords. As well, do not change the name of the generated questions documents; grading auto-detection relies on it (or else you'd have to use manual entry). Finally, to upload the questions for grading, write your answers in the space provided on the questions document and save it.

## Roadmap:

### Phase 1: Foundation - Complete
- Multi-source ingestion (text, PDF, images) ✓
- Multiple document combining ✓
- Auto-detection for notes and generated files ✓
- SQLite migration ✓
  
### Phase 2: Memory — In Progress
- Session history ✓
- Question favorites
  
### Phase 3: Insight
- Knowledge map / mastery tracking
- Difficulty analytics
- Better graphs
  
### Phase 4: Adaptation
- Auto difficulty adjustment
- Personalized study sessions
- Review scheduling
  
### Phase 5: Interface
- Timed mode
- Multi-user support
- GUI
  
### Phase 6: Reach
- Web deployment
