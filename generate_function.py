
from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(".env.txt")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not set. Check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

def generate_questions(notes, weak_focus_document, ai_weak_topic_text):
    prompt = f"""
    You are a study assistant. Based on these notes-and if there are any weak topics-generate 5 practice questions.
    For each question, and provide a space for answering but do not include the answer.
    Start directly with topic title listing all covered topics seperated by commas in the order of which they are asked in each question at the top of your response. Do not include any extra introduction or explanation other than what's listed.
    Format each one as:
    Topic Title: [topic]
    Q: [question]
    A: [answer space]
    And, remember to keep it in a format that's understandable in a Microsoft notepad document.
    Notes:
    {notes}
    {ai_weak_topic_text}
    {weak_focus_document}
    """
    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = prompt
    )
    return response.text


def run_generate():

    today = datetime.now().strftime("%Y-%m-%d-%I-%M-%p")

    notes_document = input("Please input note textfile name: ")
    question_weak_focus = input("Focus on weak topics? (y/n): ")
    if question_weak_focus == "y":
        weak_focus_document_name = input("Please input weak topic textfile name: ")
        with open(f"{weak_focus_document_name}.txt", "r") as f:
            weak_focus_document = f.read()
        ai_weak_topic_text = "Weak Topics:"
    else:
        weak_focus_document = ""
        ai_weak_topic_text = ""

    with open(f"{notes_document}.txt", "r") as f:
        notes = f.read()

    notes_title_stripped = notes_document.strip()
    part_notes_title = notes_title_stripped.split(" ")
    notes_word_index = part_notes_title.index("notes")
    subject_parts = part_notes_title[:notes_word_index]
    subject = " ".join(subject_parts).strip()

    questions = generate_questions(notes, weak_focus_document, ai_weak_topic_text)

    with open(f"{subject} questions {today}.txt", "w") as f:
        f.write(questions)

    print(f"Questions saved to '{subject} questions {today}.txt'")

if __name__ == "__main__":
    run_generate()