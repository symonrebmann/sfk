
from datetime import datetime

import os

def extract_topics(text: str) -> list[str]:
    list_topics = []
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Topic Title:"):
            topics = stripped.replace("Topic Title:", " ").strip()
            for t in topics.split(","):
                list_topics.append(t.strip())
    if not list_topics:
        first_line = lines[0].strip()
        for t in first_line.split(","):
                list_topics.append(t.strip())
    return list_topics
                

def extract_grades(text: str) -> list[str]:
    list_grades = []
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("G:"):
            grade = stripped[2:].strip()
            list_grades.append(grade)
    return list_grades

def get_topics_and_grades(text: str) -> list[tuple[str, str]]:
    topics = extract_topics(text)
    grades = extract_grades(text)
    topics_and_grades = list(zip(topics, grades))
    return topics_and_grades

def get_stats(records: list[dict[str, any]]) -> dict[str, any] | None:
    total = sum(r["count"] for r in records)
   
    if total == 0:
        return None

    correct = sum(1 for r in records if r["grade"] == "Correct")
    partial = sum(1 for r in records if r["grade"] == "Partially Correct")
    incorrect = sum(1 for r in records if r["grade"] == "Incorrect")
    fully_correct_percent = correct / total
    partial_and_correct_percent = (correct + partial) / total
    total_weighted_score = sum(r["score"] for r in records)
    weighted_average = total_weighted_score / total
    
    return {
        "total": total,
        "correct": correct,
        "partial": partial,
        "incorrect": incorrect,
        "correct%": fully_correct_percent,
        "partial%": partial_and_correct_percent,
        "weighted": weighted_average
            }

def score_bar(score: float, width: int = 10) -> str:
    filled = int(score * width)
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"

def get_trend(records: list[dict[str, any]]) -> str:
    records_sorted = sorted(records, key=lambda r: r["date"])
    
    if len (records_sorted) < 2:
        return "Needs more data"
    mid = int(len(records_sorted) / 2)

    first_half = records_sorted[:mid]
    second_half = records_sorted[mid:]

    first_average = (sum(r["score"] for r in first_half)) / len(first_half)
    second_average = (sum(r["score"] for r in second_half)) / len(second_half)
    
    if first_average < second_average:
        return "Improvement ↑"
    elif first_average > second_average:
        return "Worsen ↓"
    else:
        return "No Change →"

def generate_report(topic_groups: dict[str, any]) -> str:
    topic_with_stats = []
    for topic, records in topic_groups.items():
        stats = get_stats(records)
        if stats is not None:
            topic_with_stats.append((topic, records, stats))

    topic_with_stats.sort(key=lambda x: x[2]['weighted'])
    
    lines = []
    lines.append("Weakness Ranking")
    lines.append("=" * 50)

    for topic, records, stats in topic_with_stats:
        trend = get_trend(records)
        lines.append("  ")
        lines.append(topic)
        lines.append(f"Total: {stats['total']} | Correct: {stats['correct']} | Partially Correct: {stats['partial']} | Incorrect: {stats['incorrect']} |")
        lines.append(f" Percentage Correct: {stats['correct%']:.0%} | Percentage Correct or Partially Correct: {stats['partial%']:.0%} | Weighted Average: {stats['weighted']:.2f}")
        lines.append(f"  Trend: {trend}")
        lines.append("  History:")

        for record in sorted(records, key = lambda r: r["date"], reverse = True):
            bar = score_bar(record["score"])
            lines.append(f"     {record['date']}: {bar} {record['score']:.1f}  {record['grade']}")
    return "\n".join(lines)

def run_analytics() -> None:
  
    today = datetime.now().strftime("%Y-%m-%d-%I-%M-%p")

    file_names = os.listdir(".")

    grade_data = []

    for file in file_names:
        if file.startswith("graded"):
            try:
                with open(file, "r") as f:
                    contents = f.read()
                    file_name_stripped = file.strip()
                    file_name_parts = file_name_stripped.split(" ")
                    try:
                        answers_index = file_name_parts.index("answers")
                    except ValueError:
                        print(f"Warning: Skipping '{file}' — unexpected filename format.")
                        continue
                    date_with_suffix = " ".join(file_name_parts[answers_index + 1:])
                    date = date_with_suffix.removesuffix(".txt").strip()
                    graded_index = file_name_parts.index("graded")
                    subject = " ".join(file_name_parts[graded_index + 1:answers_index])
                    topics = get_topics_and_grades(contents)
                    grade_data.append({
                        "filename": file,
                        "subject": subject,
                        "date": date,
                        "topics": topics
                    })
            except ValueError:
                print(f"Warning: Skipping '{file}' — unexpected filename format.")
    if not grade_data:
        print("No graded files found. Please remember title formating for graded documents is 'graded subject answers today' (e.g. graded math answers 2026-05-25-11-04-AM.txt)")
        exit()

    all_records = []

    topic_groups = {}

    for file_data in grade_data:
        date = file_data["date"]
        for topic, grade in file_data["topics"]:
            if grade == "Correct":
                score = 1.0
            elif grade == "Partially Correct":
                score = .5
            else:
                score = 0.0
            all_records.append({
                "subject": file_data["subject"],
                "date": date,
                "topic": topic,
                "grade": grade,
                "score": score
            })
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append({
                    "date": date,
                    "grade": grade,
                    "score": score
                })

    averaged_topic_groups = {}

    for topic, records in topic_groups.items():
        date_groups = {}
        for record in records:
            if record["date"] not in date_groups:
                date_groups[record["date"]] = []
            date_groups[record["date"]].append(record["score"])
        
        averaged = []

        for date, scores in date_groups.items():
            avg = sum(scores) / len(scores)
            if avg >= .8:
                g = "Correct"
            elif .8 > avg >= .4:
                g = "Partially Correct"
            else:
                g = "Incorrect"
            averaged.append({"date": date, "score": avg, "grade": g, "count": len(scores)})

        averaged_topic_groups[topic] = averaged

    topic_groups = averaged_topic_groups

    report = generate_report(topic_groups)

    with open(f"analytics report {today}.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Analytics saved to 'analytics report {today}.txt'")

if __name__ == "__main__":
    run_analytics()