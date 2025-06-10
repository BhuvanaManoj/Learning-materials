import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# ============================
# Setup: Gemini API Key
# ============================
GEMINI_API_KEY = "AIzaSyAYbFP5MMt_qm5sgtrzlysXRWxxqZ6uKqo"  # Replace with your inbuilt API key
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel('https://ai.google.dev/gemini-api/docs/models#gemini-2.0-flash')

# ============================
# Prompt Template
# ============================
TASK_PROMPT_TEMPLATE = """
You are a productivity expert and task planning assistant. Your role is to help break down user-provided tasks into subtasks, assign priorities, estimate effort/time, and organize the output in a clear, structured format.

User-provided task: {task}

Follow these instructions:

1. Understand the user's main goal.
2. Break the main task into logical subtasks.
3. Prioritize the subtasks using urgency and logical sequence (High, Medium, Low).
4. Estimate time or effort for each subtask.
5. Detect dependencies (what needs to be completed first).
6. Classify tasks by type (Research, Design, Development, Testing, Review).
7. Generate a JSON-like structured output including:
   - Task ID
   - Task Title
   - Priority
   - Type
   - Estimated Time
   - Dependencies
   - Description

Include a summary at the beginning:
```json
{
  "summary": "This is a breakdown of the project '{task}' into prioritized subtasks. Estimated completion time: X days. Dependencies are considered.",
  "tasks": [ ... ]
}
         