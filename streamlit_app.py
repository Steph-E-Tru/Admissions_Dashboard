import streamlit as st
import pandas as pd
import matplotlib

from src.student_profile import create_student_profile
from src.college_matching import match_colleges
from src.application_checklist import get_college_checklist

df = pd.read_csv("data/colleges_dataset.csv")
all_majors = sorted(df['program_type'].dropna().unique())

# Easiest multipage: sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Profile & Search", "My Colleges & Checklist"])

# Persist data between reruns:
if "student" not in st.session_state:
    st.session_state["student"] = None
if "colleges" not in st.session_state:
    st.session_state["colleges"] = None
if "matched_colleges" not in st.session_state:
    st.session_state["matched_colleges"] = None
if "interested_college_ids" not in st.session_state:
    st.session_state["interested_college_ids"] = set()
if "favorites" not in st.session_state:
    st.session_state["favorites"] = set()

if page == "Profile & Search":
    st.image("https://images.squarespace-cdn.com/content/v1/5fc463b9df132613bbd422a5/1607559213633-RU0GHLJ43QYEE3VKV5K6/Graduations+Now+Blog+Different+Types+of+High+School+Graduation+Hats.jpg", width=100)  # Example graduation cap icon
    st.write("Fill out your profile and discover colleges that match your interests and academic background!")
    
    st.header("Create Student Profile & Find Colleges")
    name = st.text_input("Enter your name:")
    gpa = st.number_input("Enter your GPA (Unweighted):", min_value=0.0, max_value=4.0, step=0.01)
    interests = st.multiselect("Select your areas of interest (majors):", all_majors)
    degree_level = st.selectbox("Degree Level", ["Associates", "Bachelors", "Masters", "PhD"])
    sat = st.number_input("SAT Score", min_value=400, max_value=1600)
    act = st.number_input("ACT Score", min_value=1, max_value=36)

    # Key stats with st.metric
    if st.session_state["matched_colleges"]:
        college_df = pd.DataFrame(st.session_state["matched_colleges"])
        cols_to_show = ["college_name", "rank", "cost", "application_fee", "application_deadline", "state_location", "minimum_gpa", "minimum_sat", "minimum_act", "degree_level"]  
        st.dataframe(college_df[cols_to_show])
        st.metric(label="Matched Colleges", value=len(college_df))
        if "cost" in college_df.columns:
            st.metric(label="Average Cost", value=f"${college_df['cost'].mean():,.0f}")

    if st.button("Find Matching Colleges"):
        student = create_student_profile(
            name, gpa, interests, degree_level,
            {"SAT": sat, "ACT": act}, False, []
        )
        colleges = df.to_dict(orient="records")
        matched_colleges = match_colleges(student, colleges)
        st.session_state["student"] = student
        st.session_state["colleges"] = colleges
        st.session_state["matched_colleges"] = matched_colleges
        st.session_state["interested_college_ids"] = set()  # Reset on new search

        # Reset completed requirements for all newly matched colleges
        if matched_colleges:
            for college in matched_colleges:
                college_key = str(college.get("college_id", college.get("college_name", "")))
                st.session_state[college_key] = set()

    matched_colleges = st.session_state["matched_colleges"]
    if matched_colleges:
        st.subheader("Matched Colleges")
        college_df = pd.DataFrame(matched_colleges)
        # Show a color-coded table for cost
        if "cost" in college_df.columns:
            styled_df = college_df.style.background_gradient(subset=["cost"], cmap="Greens")
            st.dataframe(styled_df)
        else:
            st.dataframe(college_df[cols_to_show])

        st.write("Select colleges you are interested in:")
        for college in matched_colleges:
            college_id = college.get("college_id", college["college_name"])
            checked = st.checkbox(f"Interested in {college['college_name']}?", key=f"interest_{college_id}", value=college_id in st.session_state["interested_college_ids"])
            if checked:
                st.session_state["interested_college_ids"].add(college_id)
            else:
                st.session_state["interested_college_ids"].discard(college_id)

            # Favorite button
            fav_checked = st.button(f"⭐ Star {college['college_name']}", key=f"star_{college_id}")
            if fav_checked:
                st.session_state["favorites"].add(college_id)

        # Download matched colleges button
        st.download_button(
            "Download Matched Colleges",
            data=college_df.to_csv(index=False),
            file_name="matched_colleges.csv",
            mime="text/csv"
        )
    else:
        st.write("No matched colleges. Please search first.")

elif page == "My Colleges & Checklist":
    st.header("Your Selected Colleges & Application Checklist")
    interested_ids = st.session_state["interested_college_ids"]
    matched_colleges = st.session_state.get("matched_colleges", [])
    selected_colleges = [c for c in matched_colleges if c.get("college_id", c["college_name"]) in interested_ids]
    for college in selected_colleges:
        display_name = college.get("college_name", str(college.get("college_id", "Unknown College")))
        # Expander for college details (NEW)
        with st.expander(f"{display_name} Details"):
            requirements = [req.strip() for req in college.get("application_requirements", "").split(",") if req.strip()]
            college_for_checklist = dict(college)
            college_for_checklist["requirements"] = requirements
            college_key = str(college.get("college_id", display_name))
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
                # Progress bar
                st.progress(len(completed_set) / len(checklist) if checklist else 0)
                st.write(f"Completed {len(completed_set)}/{len(checklist)} requirements.")
                # Balloons for completing all
                if len(completed_set) == len(checklist) and checklist:
                    st.balloons()
            else:
                st.write("No requirements listed for this college.")
    if not selected_colleges:
        st.write("You haven't selected any colleges yet. Go to the first page to choose them!")
