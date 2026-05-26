
from generate_function import run_generate
from grade_function import run_grade
from analytics_function import run_analytics

fail_counter = 0

while fail_counter < 3:
    goal = input("Please choose one of the following: Generate, Grade, or Analyze:")

    if goal == "Generate":
        run_generate()
        break
    elif goal == "Grade":
        run_grade()
        break
    elif goal == "Analyze":
        run_analytics()
        break
    else:
        print("Error: Answer not recgonized. Please try again")
        fail_counter += 1

if fail_counter >= 3:
    print("Too many failed attempts. Exiting")
    exit()