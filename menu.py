
from generate_function import run_generate
from grade_function import run_grade
from analytics_function import run_analytics

def menu() -> None:

    fail_counter = 0

    while fail_counter < 3:
        goal = input("Please choose one of the following: Generate, Grade, or Analyze: ").strip().lower()

        if goal == "generate":
            run_generate()
            break
        elif goal == "grade":
            run_grade()
            break
        elif goal == "analyze":
            run_analytics()
            break
        else:
            print("Error: Answer not recognized. Please try again.")
            fail_counter += 1

    if fail_counter >= 3:
        print("Too many failed attempts. Exiting.")
        exit()

if __name__ == "__main__":
    menu()