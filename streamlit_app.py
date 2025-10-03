import streamlit as st
import pandas as pd

# Import your functions from the src/ folder
from src.student_profile import create_student_profile
from src.college_matching import match_colleges
from src.application_checklist import get_college_checklist

st.title("College Admissions Dashboard")

# Load your dataset (adjust the path if needed)
df = pd.read_csv("data/colleges_dataset.csv")

# Extract available majors from the dataset for user selection
all_majors = sorted(df['program_type'].dropna().unique())

# User input widgets
name = st.text_input("Enter your name:")
gpa = st.number_input("Enter your GPA (Unweighted):", min_value=0.0, max_value=4.0, step=0.01)
interests = st.multiselect("Select your areas of interest (majors):", all_majors)
degree_level = st.selectbox("Degree Level", ["Undergraduate", "Associate", "Bachelor", "PhD"])
sat = st.number_input("SAT Score", min_value=400, max_value=1600)
act = st.number_input("ACT Score", min_value=1, max_value=36)
location_important = st.checkbox("Is location/proximity to home important?")
desired_states = []
if location_important:
    us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC', 'PR', 'VI']  # Full list of states
    desired_states = st.multiselect("Select preferred states", us_states)

#Find Matching Colleges
if st.button("Find Matching Colleges"):
    if not name or not interests:
        st.error("Please enter a name and select at least one interest.")
    else:
        # Create student profile
        student = create_student_profile(name, gpa, interests, degree_level,
            {"SAT": sat, "ACT": act}, location_important, desired_states
        )

        # Build a list of colleges for matching (simulate college records from CSV)
        colleges = []
        
        matched_colleges = match_colleges(student, colleges)
        if matched_colleges:
            st.success(f"Found {len(matched_colleges)} matching colleges for {name}")
            for college in matched_colleges:
                st.subheader(college.get("name", "Unknown College"))
                # Track completion, e.g. in session state or reload per user
                requirements = get_college_checklist(college)
                completed_set = st.session_state.get(college["name"], set())
                checklist = get_college_checklist(college, completed_set)
                for req in checklist:
                    checked = st.checkbox(req["requirement"], value=req["completed"], key=college["name"] + req["requirement"])
                    # Update completed_set according to checkboxes
                # st.write(requirements)
        else:
            st.warning("No colleges matched your criteria.")
