# Function 2: Match Colleges to Student Profile
def match_colleges(student: dict, colleges: list) -> list:
    """ 
    Match colleges to student profile based on interests, GPA, degree level, test scores, and location preferences.
    Args:
        student: Student profile (dict)
        colleges: List of college dicts with 'majors', 'min_gpa', 'degree_level', 'min_test_scores', 'states'
    Returns:
        List of matched college dicts
    """
    matches = []

    # Convert all student interests to lowercase once to avoid issues with case-sensitivity
    student_interests = [interest.lower() for interest in student["interests"]]
    student_degree = student.get("degree_level", "").lower()
    student_scores = student.get("test_scores", {})
    location_important = student.get("location_important", False)
    desired_states = student.get("desired_states", [])

    for col in colleges:
        # Convert each college's majors and degrees to lowercase
        college_majors = [major.lower() for major in col["majors"]]
        college_degrees = [deg.lower() for deg in col.get("degree_level", [])]

        # Match interests, gpa, and degree level
        if not any(interest in college_majors for interest in student_interests):
            continue
        if student["gpa"] < col.get("min_gpa", 0.0):
            continue
        if student_degree not in college_degrees:
            continue

         # SAT/ACT logic (suggested, not required)
        min_sat = col.get("minimum_sat", None)
        min_act = col.get("minimum_act", None)
        sat_score = student_scores.get("SAT", None)
        act_score = student_scores.get("ACT", None)
        fit_criteria = []

        # GPA always met (since filtered)
        fit_criteria.append("GPA")

        if min_sat is not None and sat_score is not None and sat_score >= min_sat:
            fit_criteria.append("SAT")
        if min_act is not None and act_score is not None and act_score >= min_act:
            fit_criteria.append("ACT")

        summary = f"Academic fit: {len(fit_criteria)}/3 thresholds met ({', '.join(fit_criteria)})"
        advice = ""
        # If SAT/ACT are present but not met, add supportive advice
        if min_sat is not None and (sat_score is None or sat_score < min_sat):
            advice += "Your SAT score is below suggestions, but this is not a strict requirement. "
        if min_act is not None and (act_score is None or act_score < min_act):
            advice += "Your ACT score is below suggestions, but this is not a strict requirement. "

        match = dict(col)  # All college data
        match["academic_fit_summary"] = summary
        if advice:
            match["academic_fit_advice"] = advice.strip()

        # Location filter if important
        if location_important:
            college_states = [state.upper() for state in col.get("states", [])]
            if not any(state.upper() in college_states for state in desired_states):
                continue

        matches.append(col)

    return matches
