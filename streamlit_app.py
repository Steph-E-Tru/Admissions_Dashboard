import streamlit as st
import pandas as pd

# Import your functions from the src/ folder
from src.student_profile import create_student_profile
from src.college_matching import match_colleges
from src.application_checklist import get_college_checklist

st.title("College Admissions Dashboard")

# Load your dataset
df = pd.read_csv("data/colleges_dataset.csv")

# Extract available majors from the dataset for user selection
all_majors = sorted(df['program_type'].dropna().unique())

# User input widgets
name = st.text_input("Enter your name:")
gpa = st.number_input("Enter your GPA (Unweighted):", min_value=0.0, max_value=4.0, step=0.01)
interests = st.multiselect("Select your areas of interest (majors):", all_majors)
degree_level = st.selectbox("Degree Level", ["Associates", "Bachelors", "Masters", "PhD"])
sat = st.number_input("SAT Score", min_value=400, max_value=1600)
act = st.number_input("ACT Score", min_value=1, max_value=36)

# Persist data between reruns:
if "student" not in st.session_state:
    st.session_state["student"] = None
if "colleges" not in st.session_state:
    st.session_state["colleges"] = None
if "matched_colleges" not in st.session_state:
    st.session_state["matched_colleges"] = None

if st.button("Find Matching Colleges"):
    if not name or not interests:
        st.error("Please enter a name and select at least one interest.")
    else:
        # Create student profile
        student = create_student_profile(
            name, gpa, interests, degree_level,
            {"SAT": sat, "ACT": act}, False, []
        )
        colleges = df.to_dict(orient="records")
        st.session_state["student"] = student
        st.session_state["colleges"] = colleges
        st.session_state["matched_colleges"] = match_colleges(student, colleges)

        # Reset completed requirements for all newly matched colleges
        if st.session_state["matched_colleges"]:
            for college in st.session_state["matched_colleges"]:
                college_key = str(college.get("college_id", college.get("college_name", "")))
                st.session_state[college_key] = set()

student = st.session_state["student"]
colleges = st.session_state["colleges"]
matched_colleges = st.session_state["matched_colleges"]

if matched_colleges:
    st.success(f"Found {len(matched_colleges)} matching colleges for {name}")
    for college in matched_colleges:
        # Use college_name for display
        display_name = college.get("college_name", str(college.get("college_id", "Unknown College")))
        st.subheader(display_name)

        college_key = str(college.get("college_id", display_name))

        # Split requirements from application_requirements column
        requirements = [req.strip() for req in college.get("application_requirements", "").split(",") if req.strip()]
        college_for_checklist = dict(college)
        college_for_checklist["requirements"] = requirements

        # Initialize completed set in session_state if not already present
        if college_key not in st.session_state:
            st.session_state[college_key] = set()
        completed_set = st.session_state[college_key]

        checklist = get_college_checklist(college_for_checklist, completed_set)
        if checklist:
            st.write("Application Requirements Checklist:")
            for item in checklist:
                checked = st.checkbox(item["requirement"], key=college_key + item["requirement"], value=item["completed"])
                if checked:
                    completed_set.add(item["requirement"])
                else:
                    completed_set.discard(item["requirement"])
            st.session_state[college_key] = completed_set
            st.write(f"Completed {len(completed_set)}/{len(checklist)} requirements.")
        else:
            st.write("No requirements listed for this college.")
    else:
        st.warning("No colleges matched your criteria.")
