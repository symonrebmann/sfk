# SFK — Strive For Knowledge

-

## Features:

-AI powered question generation
-Customizable question count, difficulty, and type
-37 question types across analytical, written, selected response, and STEM-specific formats
-AI-powered grading with detailed feedback
-Analytics dashboard tracking topic performance and trends over time

## Setup & Usage:

  You first need to install the required libraries. You can do this by running the following in the Python console:
	```
	pip install -r requirements.txt
	```
  You will then need to create an environmental variable. You can do this by creating a text document titled .env (you can have the .txt extension) in the folder. Then, in the text document, type "GEMINI_API_KEY=[your Gemini key]."

  Finally, run the file menu.py by typing "python menu.py" in the Python console. From there, you will be asked if you'd like to generate questions, grade your answers, or generate analytics.

  For note files, please keep the format simple using the format "[subject] notes." As well, it is currently required to not change the names of any of the generated documents. Finally, to upload the questions for grading, write your answers in the space provided on the questions document and save it (there is no need for a name change).

## Future plans:

### In Development:

-Upload PDFs, textbook chapters, and images as source material
-Support for multiple note documents
-Auto-detect files / flexible file naming
-Question difficulty scaling tracked in analytics
-Improved analytics charts and graphs
-Session history log

### Planned Features:

-Multiple user profiles
-Question flagging and favorites
-Timed quiz mode
-Recommended difficulty auto-adjustment based on performance
-Simple GUI
-Web or app availability
