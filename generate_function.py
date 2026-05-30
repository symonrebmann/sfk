
from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(".env.txt")

api_key: str | None = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not set. Check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

def generate_questions(notes: str, weak_focus_document: str, ai_weak_topic_text: str, question_amount: int) -> str:
    prompt = f"""
    You are a study assistant. Based on these notes-and if there are any weak topics-generate {question_amount} practice questions.
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


def run_generate() -> None:

    today = datetime.now().strftime("%Y-%m-%d-%I-%M-%p")

    fail_count_notes_document = 0

    while fail_count_notes_document < 3:
        notes_document = input("Please input note textfile name: ")
        try:
            with open(f"{notes_document}.txt", "r") as f:
                notes = f.read()
                break
        except FileNotFoundError:
            print(f"Error: '{notes_document}.txt' not found. Please try again.")
            fail_count_notes_document += 1   
    if fail_count_notes_document >= 3:
        print("Too many failed attempts. Exiting.")
        exit()

    fail_count_weak_focus = 0

    question_weak_focus = input("Focus on weak topics? (y/n): ").strip().lower()
    if question_weak_focus == "y":
        while fail_count_weak_focus < 3:
            weak_focus_document_name = input("Please input weak topic textfile name: ")
            ai_weak_topic_text = "Weak Topics: "
            try:
                with open(f"{weak_focus_document_name}.txt", "r") as f:
                    weak_focus_document = f.read()
            except FileNotFoundError:
                print(f"Error: '{notes_document}.txt' not found. Please try again.")
                fail_count_weak_focus += 1   
        if fail_count_weak_focus >= 3:
            print("Too many failed attempts. Exiting.")
            exit()
    else:
        weak_focus_document = ""
        ai_weak_topic_text = ""

    fail_count_question_amount = 0

    while fail_count_question_amount < 3:
        try:
            question_amount = int(input("How many questions would you like? "))
            if question_amount > 25:
                print("Error: Too many questions. Please try an amount 25 or under.")
                fail_count_question_amount += 1
            elif question_amount <= 0:
                print("Error: Please enter a positive integer.")
                fail_count_question_amount += 1
            else:
                break
        except ValueError:
            print("Error: Please enter a valid integer.")
            fail_count_question_amount += 1   
    if fail_count_question_amount >= 3:
        print("Too many failed attempts. Exiting.")
        exit()

    notes_title_stripped = notes_document.strip().lower()
    part_notes_title = notes_title_stripped.split(" ")
    try:
        notes_word_index = part_notes_title.index("notes")
    except ValueError:
        print("Error: Notes filename must contain the word 'notes.'")
        exit()
    subject_parts = part_notes_title[:notes_word_index]
    if not subject_parts:
        print("Error: Could not determine subject from filename. Please include a subject before 'notes (e.g. 'math notes').")
    subject = " ".join(subject_parts).strip()

    questions: str = generate_questions(notes, weak_focus_document, ai_weak_topic_text, question_amount)
    if questions is None:
        print("Questions failed to generate. Please retry.")
        exit()
    else:
        with open(f"{subject} questions {today}.txt", "w") as f:
            f.write(questions)

    print(f"Questions saved to '{subject} questions {today}.txt'")

if __name__ == "__main__":
    run_generate()