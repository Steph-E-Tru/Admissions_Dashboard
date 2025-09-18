🚀 Admissions Dashboard

A simple, interactive Streamlit app that helps students find, compare, and track application requirements for colleges based on their interests and GPA.

📋 Table of Contents

Overview
Features
Installation
Quickstart
Usage Examples
Project Structure
Acknowledgments

📖 Overview

This project helps students streamline the college admissions process by allowing them to build a profile, select their academic interests, and instantly view colleges that match their preferences and eligibility. Application requirements for each college are listed to help students stay organized and expedite the application process. The dashboard is built with Streamlit for maximum interactivity and simplicity, making college search and application tracking accessible for everyone.

✨ Features

✅ Build a student profile by entering name, GPA, and selecting majors.
✅ Get a personalized list of matching colleges from the database and review each school's application requirements.
✅ Interactive user experience with real-time results.
🚧 Planned feature: Save favorite schools and export custom checklists.
🚧 Planned feature: Input additional filters for colleges such as location and tuition cost.

⚙️ Installation

Clone the repository and install dependencies.

```bash
git clone https://github.com/Steph-E-Tru/Admissions_Dashboard
cd Admissions_Dashboard
pip install -r requirements.txt
```                    
🚀 Quickstart

Launch the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```                    
Visit the URL displayed in your terminal to interact with the app in your browser.

💡 Usage Examples

- Enter student information and select interests (majors).
- Hit the “Find Matching Colleges” button to instantly see colleges that fit your profile.
- Review the requirements checklist for each college, displayed in an easy-to-read format.
                    
📁 Project Structure

Admissions_Dashboard/

│

├── streamlit_app.py          # The Streamlit interface

├── src/

│   ├── student_profile.py    # Profile creation code

│   ├── college_matching.py   # Matching code

│   └── application_checklist.py # Checklist code

├── requirements.txt          # Dependencies

├── README.md                 # This documentation

├── data/

│   └── colleges_dataset.csv   # College/program data

├── tests/                    # Sanity tests

│   ├── test_student_profile.py

│   ├── test_college_matching.py

└── └── test_application_checklist.py


🙏 Acknowledgments

Inspired by course guidance, provided by Dr. Yaroslava Yingling, and the NCSU MSE 490 prototype assignments. Thanks to Streamlit/Colab and other AI tools for rapid prototyping.                    
