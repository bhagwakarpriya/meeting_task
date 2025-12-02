# meeting_task

A Python tool that parses meeting transcripts and automatically extracts actionable tasks with assignee, deadline, priority, and reason.  
It uses loop‑based logic to handle ranscripts where task, assignee, and deadline may be spread across different sentences.

## Features
- Task Extraction – Detects actionable verbs like *fix, update, optimize, design, write*.  
- Assignee Detection – Loops backwards through transcript until a team member’s name or role keyword is found.  
- Deadline Detection – Loops forwards until a deadline phrase (e.g., tomorrow, next Monday, end of this week) is found.  
- Priority Classification – Marks tasks as Critical, High, or Medium based on urgency keywords.  
- Structured Output – Saves tasks to output.json with fields:  
  - id  
  - task  
  - assigned_to  
  - deadline  
  - priority  
  - reason

## Project Structure
data/ ├── meeting.txt # Input transcript file 
      └── output.json # Extracted tasks (generated)

extractor.py # Main Python script 
README.md # Documentation

## Workflow
- First execute **transcribe.py**, it will convert sp3 to text and save it in a file meeting.txt.
- After that execute **extraction.py** it will generate the output shown as below by following steps:
  1) Sentence Splitting – Splits transcript into sentences using regex.
  2) Verb Detection – Identifies task sentences by action verbs.
  3) Backward Loop – Finds assignee by scanning earlier lines.
  4) Forward Loop – Finds deadline by scanning later lines.
  5) Cleanup – Removes filler words and deadline phrases from task text.
  - Output: 
  {
    "id": 1,
    "task": "fix the critical log",
    "assigned_to": "Sakshi",
    "deadline": "tomorrow",
    "priority": "Critical / High",
    "reason": "Frontend task, blocking users"
  }
