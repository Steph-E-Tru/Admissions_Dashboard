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
gpa = st.number_input("Enter your GPA:", min_value=0.0, max_value=4.0, step=0.01)
interests = st.multiselect("Select your areas of interest (majors):", all_majors)

if st.button("Find Matching Colleges"):
    if not name or not interests:
        st.error("Please enter a name and select at least one interest.")
    else:
        # Create student profile
        student = create_student_profile(name, gpa, interests)

        # Build a list of colleges for matching (simulate college records from CSV)
        colleges = []
        for idx, row in df.iterrows():
          # Extract requirements as a list if avaliable
          if "application_requirements" in df.columns and pd.notna(row["application_requirements"]):
                # Split on commas if requirements are stored as a single string
                requirements = [req.strip() for req in str(row["application_requirements"]).split(",")]
          else:
                requirements = []  
          
          college = {
                "name": row.get("college_name", "Unknown College"),
                "majors": [row.get("program_type", "Unknown")],
                "min_gpa": row.get("minimum_gpa", 0.0),
                "requirements": ["transcript", "essay"]  # Replace with realistic requirements if available in CSV
            }
          colleges.append(college)

        # Use matching function
        matched_colleges = match_colleges(student, colleges)

        # Show results
        if matched_colleges:
            st.success(f"Found {len(matched_colleges)} matching colleges for {name}:")
            for college in matched_colleges:
                st.subheader(college["name"])
                checklist = get_college_checklist(college)
                st.write("Requirements:")
                st.write(checklist)
        else:
            st.warning("No colleges matched your criteria.")
