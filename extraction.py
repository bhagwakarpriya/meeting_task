import re
import json

# Team members and expertise
team_members = {
    "Sakshi": "Frontend task, blocking users",
    "Mohit": "Backend expertise",
    "Arjun": "UI/UX task, relevant experience",
    "Lata": "QA expertise, testing task"
}

# Role keywords for inference
role_keywords = {
    "Sakshi": ["frontend", "bug", "login"],
    "Mohit": ["backend", "database", "api", "performance"],
    "Arjun": ["design", "ui", "ux", "screen"],
    "Lata": ["qa", "test", "unit", "automation", "payment module"]
}

# Deadline mapping
deadline_map = {
    "tomorrow evening", "tomorrow", "next monday", "wednesday", "friday", "before friday's release", "end of this week"
}

def search_assignee(sentences, current_index):
    # Loop backwards until a name/role keyword is found
    for i in range(current_index, -1, -1):
        line = sentences[i].lower()
        for name, keywords in role_keywords.items():
            if any(k in line for k in keywords):
                return name
    return "Unassigned"

def search_deadline(sentences, current_index):
    # Loop forwards until a deadline phrase is found
    for i in range(current_index, len(sentences)):
        line = sentences[i].lower()
        for pat in deadline_map:
            if pat in line:
                return pat
    return "Not specified"

def extract_task_phrase(line):
    match = re.search(r"\b(fix|update|design|tackle|write|optimization|performance|implement|create|develop)\b(.*)", line.lower())
    if match:
        verb = match.group(1)
        obj = match.group(2).strip()
        obj = re.sub(r"(before|next|previous|for the|to|this|and|by).*", "", obj).strip()
        phrase = f"{verb} {obj}".strip()
        return phrase
    return line.strip()

def extract_tasks(transcript: str):
    sentences = re.split(r'[.!?]\s+', transcript)
    tasks = []
    task_id = 1

    for i, line in enumerate(sentences):
        line = line.strip()
        if not line:
            continue

        # Skip dependency lines
        if "depends on" in line.lower():
            continue

        if re.search(r"\b(fix|update|design|write|optimize|tackle|implement|create|develop)\b", line.lower()):
            assignee = search_assignee(sentences, i)  
            deadline = search_deadline(sentences, i)   

            if "critical" in line.lower() or "blocking users" in line.lower():
                priority = "Critical / High"
            elif "high priority" in line.lower() or "before friday's release" in line.lower() or "affecting user experience" in line.lower():
                priority = "High"
            else:
                priority = "Medium"

            reason = team_members.get(assignee, "")
            task_phrase = extract_task_phrase(line)

            tasks.append({
                "id": task_id,
                "task": task_phrase,
                "assigned_to": assignee,
                "deadline": deadline,
                "priority": priority,
                "reason": reason
            })
            task_id += 1

    return tasks

if __name__ == "__main__":
    with open("data/meeting.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    tasks = extract_tasks(transcript)

    with open("data/output.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

    print(f"\n{len(tasks)} tasks extracted and saved to data/output.json")
