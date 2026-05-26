# AI-Powered Personalized Study Aid

## What it does:

  You are able to use AI to generate practice questions, answer them, have them graded, and view your progression on a wide variety of topics. This program can be used to personalize problems against your weaknesses.

## How to use it:

  You first need to install the required libraries. You can do this by running the following in the Python console:
	```
	pip install -r requirements.txt
	```
  You will then need to create an environmental variable. You can do this by creating a text document titled .env (you can have the .txt extension) in the folder. Then, in the text document, type "GEMINI_API_KEY=[your Gemini key]."

  Finally, run the file menu.py by typing "python menu.py" in the Python console. From there, you will be asked if you'd like to generate questions, grade your answers, or generate analytics.

  For note files, please keep the format simple using the format "[subject] notes." As well, it is currently required to not change the names of any of the generated documents. Finally, to upload the questions for grading, write your answers in the space provided on the questions document and save it (there is no need for a name change).

## Future plans:

### Quality Improvements:

-Ability to customize the amount of questions
-Ability to change question difficulty
-Ability to choose question variety (MCQ, short answer, etc.)

### Optimize:

-Ability to use multiple formats for naming notes, questions, etc.
-Auto-detect files

### Polish

-Simple UI
-Better charts and graphs for analytics
