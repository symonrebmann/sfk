
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

def grade_answers(answers: str) -> tuple[str, str]:
    prompt = f"""
    You are a study assistant. Based on these answers to the given questions please grade them.
    For each grade please give a reason and if it's a wrong answer offer what went wrong.
    Remember to keep it in a format that's understandable in a Microsoft notepad document.
    As well, if there are equally wrong topics just put the first alphabetical topic (at the same amount wrong) first in the chain relatively.
    Please label the weak topics, if there are any, as there respective grades. If more than one question of the same topic is missed write the topic name and grade on seperate lines equal to the distribution of the grade.
    If all answers are correct do not include any Weak Topics section and don't include the section title.
    Start directly with topic title listing all covered topics seperated by commas in the order of which they are asked in the questions. Do not include any extra introduction or explanation other than what's listed.
    For problems involving math please show your work.
    Format each one as:
    Grading:
    Q: [question given]
    A: [answer given]
    G: [Correct / Partially Correct / Incorrect]
    E: [explanation]
    Weak Topics:
    - [topic that got Incorrect] [grade]
    - [topic that got Partially Correct] [grade]
    Questions and Answers:
    {answers}
    """
    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = prompt
    )
    parts_grade = response.text.split("Weak Topics:")
    grading = parts_grade[0]

    if len(parts_grade) > 1 and len(parts_grade[1].strip()) > 5:
        weak_topics = parts_grade[1]
    else:
        weak_topics = ""

    return grading, weak_topics


def run_grade() -> None:
    
    today = datetime.now().strftime("%Y-%m-%d-%I-%M-%p")

    fail_count_answer_document = 0

    while fail_count_answer_document < 3:
        answer_document = input("Please input answer textfile name: ")
        try:
            with open(f"{answer_document}.txt", "r") as f:
                answers = f.read()
                break
        except FileNotFoundError:
            print(f"Error: '{answer_document}.txt' not found. Please try again.")
            fail_count_answer_document += 1   
    if fail_count_answer_document >= 3:
        print("Too many failed attempts. Exiting.")
        exit()


    grade, weak_topics = grade_answers(answers)

    answers_title_stripped = answer_document.strip().lower()
    part_answers = answers_title_stripped.split(" ")
    try:
        quest_word_index = part_answers.index("questions")
    except ValueError:
        print("Error: Notes filename must contain the word 'questions.'")
        exit()
    subject_parts = part_answers[:quest_word_index]
    if not subject_parts:
        print("Error: Could not determine subject from filename. Please include a subject before 'questions (e.g. 'math questions 2026-05-24-09-35-PM').")
        exit()
    subject = " ".join(subject_parts).strip()

    if grade is None:
        print("Grade failed to generate. Please retry.")
        exit()

    with open(f"graded {subject} answers {today}.txt", "w") as f:
        f.write(grade)

    if len(weak_topics) > 1 and len(weak_topics.strip()) > 5:
        with open(f"weak {subject} topics {today}.txt", "w") as f:
            f.write(weak_topics)
        print(f"Weak topics saved to 'weak {subject} topics {today}.txt'")
    else:
        print("No weak topics found.")

    print(f"Grades saved to 'graded {subject} answers {today}.txt'")

if __name__ == "__main__":
    run_grade()