# meeting_task

A Python tool that parses meeting transcripts and automatically extracts actionable tasks with assignee, deadline, priority, and reason.  
It uses loop‑based logic to handle ranscripts where task, assignee, and deadline may be spread across different sentences.

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

1. search_assignee(sentences, current_index)
Task: Identify the team member responsible for a task. Description:
      - Loops backwards from the current sentence index.
      - Checks each earlier sentence for keywords associated with team members (from role_keywords).
      - If a match is found, returns the corresponding team member’s name.
      - If no match is found, returns "Unassigned". 

2. search_deadline(sentences, current_index)
Task: Find the deadline associated with a task. Description:
      - Loops forwards from the current sentence index.
      - Scans each later sentence for deadline phrases (from deadline_map).
      - If a match is found, returns the normalized deadline phrase.
      - If no deadline is found, returns "Not specified". 

3. extract_task_phrase(line)
Task: Generate a concise “verb + object” phrase for the task. Description:
      - Uses regex to detect action verbs (e.g., fix, update, design, write, optimize).
      - Captures the verb and the rest of the sentence as the object.
      - Cleans up filler words and deadline references (e.g., before, next, by).
      - Returns a compact phrase like "fix login bug" or "update API documentation". 

4. extract_tasks(transcript)
Task: Process the entire transcript and extract structured tasks. Description:
      - Splits the transcript into sentences using regex.
      - Iterates through each sentence:
        - Skips dependency lines (e.g., “depends on Task #1”).
        - Detects task sentences by checking for action verbs.
        - Calls search_assignee (backward loop) to find the responsible person.
        - Calls search_deadline (forward loop) to find the deadline.
        - Determines priority based on urgency keywords (critical, blocking users, high priority).
        - Calls extract_task_phrase to generate a clean task description.
      - Builds a structured dictionary for each task with fields:
        - id, task, assigned_to, deadline, priority, reason.
      - Returns a list of all extracted tasks. 

5. __main__ block
Task: Run the program end‑to‑end. Description:
      - Reads the transcript from data/meeting.txt.
      - Passes it to extract_tasks to generate structured tasks.
      - Saves the tasks to data/output.json in JSON format.
      - Prints the number of tasks extracted.
