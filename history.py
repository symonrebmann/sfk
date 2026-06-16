from database import cursor
import math

def get_session_list() -> list[dict]:
    session_list = []

    cursor.execute("""
        SELECT sessions.question_type, sessions.difficulty, sessions.date, sessions.id
        FROM sessions                   
        ORDER BY sessions.date
        """)
                            
    for row in cursor.fetchall():
        question_type = row[0].lower()
        difficulty = row[1]
        date = row[2]
        session_id = row[3]

        cursor.execute("""
            SELECT session_subjects.subject
            FROM session_subjects
            WHERE session_subjects.session_id = ?
        """, (session_id,))

        subjects = [row[0].lower() for row in cursor.fetchall()]

        cursor.execute("""
            SELECT questions.question_number, responses.grade
            FROM questions
            JOIN responses ON questions.id = responses.question_id
            WHERE questions.session_id = ?
        """, (session_id,))

        scores = []

        rows = cursor.fetchall()

        total_questions = len(rows)

        for row in rows:

            if row[1] == "Correct":
                score = 1.0
            elif row[1] == "Partially Correct":
                score = .5
            else:
                score = 0.0
            scores.append(score)

        try:
            grade_avg = sum(scores) / len(scores)
        except ZeroDivisionError:
            print("No results found. Please try again once there is at least one graded session.")
            exit()

        session = {
            "date": date,
            "session_id": session_id,
            "subjects": subjects,
            "question_type": question_type,
            "difficulty": difficulty,
            "grade": f"{grade_avg:.2f}",
            "total_questions": total_questions
        }
        session_list.append(session)

    session_list.sort(key=lambda x: x["date"])

    return session_list

def get_session_preview():
    
    session_list = get_session_list()

    page_total = math.ceil(len(session_list)/10)

    current_page = 1

    while True:
    
        start = (current_page - 1) * 10
        end = min(start + 10, len(session_list))

        print(f"Session Previews Page {current_page}/{page_total}")

        for i, session in enumerate(session_list[start:end], start = start + 1):
            if len(session["subjects"]) > 1:
                subjects = " ".join(subject for subject in session["subjects"])
                text_subject = "Subjects: " + subjects
            else:
                text_subject = "Subject: " + session["subjects"][0]
            print(f"""
    {i}. {session["date"]}
    Session ID: {session["session_id"]}
    Difficulty: {session["difficulty"]}
    {text_subject}
    You answered {session["total_questions"]} {session["question_type"]} questions.
    Your final grade was {session["grade"]}    
    """)
        
        while True:
            if current_page == 1:
                session_response = input("Please choose one of the above sessions by entering the corresponding number (e.g. 1, 2, 3). Or, enter n/e to view the next page/exit. ").lower().strip()
            elif current_page == page_total:
                session_response = input("Please choose one of the above sessions by entering the corresponding number (e.g. 1, 2, 3). Or, enter b/e to view the previous page/exit. ").lower().strip()
            else:
                session_response = input("Please choose one of the above sessions by entering the corresponding number (e.g. 1, 2, 3). Or, enter n/b/e to view the next/previous page/exit. ").lower().strip()
            if session_response == "n" and current_page < page_total:
                current_page += 1
                break
            elif session_response == "b" and current_page != 1:
                current_page -= 1
                break
            elif session_response == "e":
                exit()
            elif session_response == "n":
                print("You are already on the last page.")
            elif session_response == "b":
                print("You are already on the first page.")
            else:
                try:
                    session_response = int(session_response)
                    if start + 1 <= session_response <= end:
                        if len(session["subjects"]) > 1:
                            subjects = " ".join(subject for subject in session_list[session_response - 1]["subjects"])
                            text_subject = "Subjects: " + subjects
                        else:
                            text_subject = "Subject: " + session_list[session_response - 1]["subjects"][0]
                        get_full_session(session_list[session_response - 1], text_subject)
                        break
                    else:
                        print("Invalid response. Please try again.")
                except ValueError:
                    print("Invalid response. Please try again.")

def get_full_session(session_prev: dict[str, any], text_subject: str):

    session = session_prev

    session_id = session["session_id"]

    cursor.execute("""
        SELECT sessions.question_category
        FROM sessions
        WHERE sessions.id = ?
        """, (session_id,))
                            
    fetch_category = cursor.fetchone()

    question_category = fetch_category[0]

    session["question_category"] = question_category

    cursor.execute("""
        SELECT questions.id, questions.question_number, questions.question_topic, questions.question_text
        FROM questions  
        WHERE questions.session_id = ?
        ORDER BY question_number
    """, (session_id,))
    
    question_ids = []
    question_numbers = []
    question_topics = []
    question_texts = []

    for row in cursor.fetchall():
        question_ids.append(row[0])
        question_numbers.append(row[1])
        question_topics.append(row[2])
        question_texts.append(row[3])

    placeholders = ",".join("?" * len(question_ids))
    cursor.execute(f"""
        SELECT responses.answer, responses.grade, responses.explanation
        FROM responses
        WHERE responses.question_id IN ({placeholders})
        ORDER BY responses.question_id
    """, tuple(question_ids))

    responses = []

    for row in cursor.fetchall():

        response = {
            "answer": row[0],
            "grade": row[1],
            "explanation": row[2]
        }

        responses.append(response)

    print(f"""
    {session["date"]}
    Session ID: {session["session_id"]}
    Subjects: {text_subject}
    Question Type: {session["question_category"]} — {session["question_type"]}
    Difficulty: {session["difficulty"]}
    Questions: {session["total_questions"]}
    Grade: {session["grade"]}
    """)

    for x in range(int(session["total_questions"])):
        print(f"""
    {question_numbers[x]}
    Topic Title: {question_topics[x]}
    Q: {question_texts[x]}
    A: {responses[x]["answer"]}
    G: {responses[x]["grade"]}
    E: {responses[x]["explanation"]}
    """)

    fail_count_go_on = 0

    while fail_count_go_on < 3:
        go_on = input("Would you like to view another session? (y/n) ").lower().strip()
        if go_on == "y":
            break
        elif go_on == "n":
            exit()
        else:
            print("Invalid response. Please input a valid response (y/n).")
            fail_count_go_on += 1
    if fail_count_go_on >= 3:
        print("Too many failed attempts. Exiting.")
        exit()

if __name__ == "__main__":
    get_session_preview()