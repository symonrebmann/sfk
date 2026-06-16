
from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime
from database import entry_responses, cursor

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
    Start directly with topic title listing all covered topics seperated by commas in the order of which they are asked in each question at the top of your response.
    As well, include the topic title directly above each question. When listing the topic above each question JUST list that question's topic.
    As well, please list the question difficulty above each question a shown in the example below.
    Do not include any extra introduction or explanation other than what's listed.
    For problems involving math please show your work.
    Format each one as:
    Grading:
    Topic Title: [topic]
    Question Difficulty: [difficulty]
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

    try:
        response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = prompt
        )
    except Exception as e:
        if "503" in str(e):
            print("Gemini is currently unavailable due to high demand. Please try again in a moment.")
        else:
            print(f"Generation failed: {e}")

    parts_grade = response.text.split("Weak Topics:")
    grading = parts_grade[0]

    if len(parts_grade) > 1 and len(parts_grade[1].strip()) > 5:
        weak_topics = parts_grade[1]
    else:
        weak_topics = ""

    return grading, weak_topics

def get_answer_document() -> tuple[str, str]:

    answered_documents = []

    file_names = os.listdir(".")

    fail_count_answered_document = 0
    fail_count_read_document = 0
    fail_manual_entry = 0
    fail_count_warn = 0
    answers = None
    already_graded_confirmed = False

    for file in file_names:
        if "questions" in file:
            answered_documents.append(file)

    while fail_count_answered_document < 3 and fail_count_read_document < 3:
        answered_index = 0
        print("Answered Questions: ")
        for file in answered_documents:
            answered_index +=1
            print(f"{answered_index}. {file}")
        print(f"{answered_index + 1}. Manual entry")

        try:
            answered_document = int(input("Please choose one of the above documents by entering the corresponding number (e.g. 1, 2, 3). "))
            if answered_document == answered_index + 1:
                while fail_manual_entry < 3:
                    manual_entry = input("Please enter the full name of the notes document (including the extension): ")
                    answered_documents.append(manual_entry)
                    extension = os.path.splitext(answered_documents[answered_document - 1])[1]
                    if extension == ".txt":
                        break
                    else:
                        print("The file was not recognized. Please try again.")
                        fail_manual_entry += 1
                        continue
                if fail_manual_entry >= 3:
                    print("Too many failed attempts. Please try another document.")
                    continue
        except (ValueError, IndexError):
            print("The document chosen was not recgonized. Please try again.")
            fail_count_answered_document +=1
            continue
        try:
            with open(f"{answered_documents[answered_document - 1]}", "r") as f:
                answers = f.read()
            fail_count_confirm = 0

            lines = answers.split("\n")
            preview = "\n".join(lines[:25])
            print("Document preview: ")
            print(f"{preview}")
                
            while fail_count_confirm < 3:
                document_confirm = input("Is this the correct document? (y/n)").strip().lower()
                if document_confirm == "y":
                    session_id = int(lines[0].replace("Session ID:", "").strip())

                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM responses
                        JOIN questions ON questions.id = responses.question_id
                        WHERE questions.session_id = ?
                    """, (session_id,))

                    count = cursor.fetchone()[0]

                    if count > 0:
                        while fail_count_warn < 3:
                            warn_response = input("Warning: This session has already been graded. Continue anyway? (y/n) ").strip().lower()
                            if warn_response == "y":
                                name_without_suffix = os.path.splitext(answered_documents[answered_document - 1])[0]
                                file_parts = name_without_suffix.split(" ")
                                questions_index = file_parts.index("questions")
                                subject = " ".join(file_parts[:questions_index])
                                return answers, subject
                            elif warn_response == "n":
                                already_graded_confirmed = True
                                break
                            else:
                                print("Invalid response. Please input a valid response (y/n).")
                                fail_count_warn += 1
                        if fail_count_warn >= 3:
                            print("Too many failed attempts. Exiting.")
                            exit()
                    if not already_graded_confirmed:
                        name_without_suffix = os.path.splitext(answered_documents[answered_document - 1])[0]
                        file_parts = name_without_suffix.split(" ")
                        questions_index = file_parts.index("questions")
                        subject = " ".join(file_parts[:questions_index])
                        return answers, subject
                    else:
                        fail_count_answered_document = 0
                        fail_count_read_document = 0
                        fail_manual_entry = 0
                        fail_count_warn = 0
                        answers = None
                        already_graded_confirmed = False
                        break
                elif document_confirm == "n":
                    fail_count_answered_document = 0
                    fail_count_read_document = 0
                    fail_manual_entry = 0
                    fail_count_warn = 0
                    answers = None
                    break
                else:
                    print("Invalid response. Please input a valid response (y/n).")
                    fail_count_confirm += 1
            if fail_count_confirm >= 3:
                print("Too many failed attempts. Exiting.")
                exit()
            continue
        except:
            print("Notes extractions failed. Please try another notes document.")
            fail_count_read_document += 1
    if fail_count_answered_document >= 3 or fail_count_read_document >= 3:
        print("Too many failed attempts. Exiting.")
        exit()
    if answers is None:
        print("Too many failed attempts. Exiting.")
        exit()

def run_grade() -> None:
    
    today = datetime.now().strftime("%Y-%m-%d-%I-%M-%p")

    answers, subject = get_answer_document()

    grade, weak_topics = grade_answers(answers)

    session_id = int(answers.split("\n")[0].replace("Session ID:", "").strip())

    if grade is None:
        print("Grade failed to generate. Please retry.")
        exit()

    header = f"Session ID: {session_id}\n\n"
    final_grade_output = header + grade 

    entry_responses(grade, session_id)

    with open(f"graded {subject} answers {today}.txt", "w") as f:
        f.write(final_grade_output)
        print(f"Grades saved to 'graded {subject} answers {today}.txt'")

    if len(weak_topics) > 1 and len(weak_topics.strip()) > 5:
        with open(f"weak {subject} topics {today}.txt", "w") as f:
            f.write(weak_topics)
        print(f"Weak topics saved to 'weak {subject} topics {today}.txt'")
    else:
        print("No weak topics found.")

if __name__ == "__main__":
    run_grade()