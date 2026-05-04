AI Productivity Tool (LangChain Project)

An all-in-one AI-powered productivity application built using Python, LangChain, and Streamlit.
This tool combines multiple intelligent features like code explanation, chatbot interaction, task planning, and notes generation into a single platform.

🧠 Key Features

💻 Code Explainer
Explains code in simple, human-readable language
Helpful for beginners and students
Supports multiple programming concepts

💬 Text Bot (Chatbot)
General-purpose AI chatbot
Answers questions and assists with daily tasks

📅 Planner
Helps organize tasks and schedules
Can be extended into a task management system

📝 Notes Generator
Converts raw text into structured notes
Useful for students and content creators

📄 PDF Chat
Upload PDF files and ask questions
Extracts and understands document content
Useful for studying, research, and summaries

🌐 Streamlit Interface
Clean and interactive UI
Easy to use for non-technical users

📂 Project Structure
AI-Productivity-Tool/
│── app.py                  # Main controller
│── requirements.txt       # Dependencies

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/Machine-learning.git
cd AI-Productivity-Tool
2️⃣ Install Dependencies
pip install -r requirements.txt
🔑 Environment Setup

Create a .env file in the root directory and add:

OPENAI_API_KEY=your_api_key_here

Usage
Run Main Application
python app.py
Run Streamlit UI
streamlit run bot_streamlit.py

🛠️ Tech Stack
Python 
LangChain 
OpenAI API 
Streamlit 