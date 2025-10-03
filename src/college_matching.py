# Function 2: Match Colleges to Student Profile
def match_colleges(student: dict, colleges: list) -> list:
    """ 
    Match colleges to student profile based on interests, GPA, degree level, test scores, and location preferences.
    Args:
        student: Student profile (dict)
        colleges: List of college dicts with 'majors', 'min_gpa', 'degree_levels', 'min_test_scores', 'states'
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
        college_degrees = [deg.lower() for deg in col.get("degree_levels", [])]

        # Match interests, gpa, and degree level
        if not any(interest in college_majors for interest in student_interests):
            continue
        if student["gpa"] < col.get("min_gpa", 0.0):
            continue
        if student_degree not in college_degrees:
            continue

        # Standardized test score filter (if applicable)
        min_scores = col.get("min_test_scores", {})
        test_score_ok = True
        for test, min_val in min_scores.items():
            # if student didn't take a required test or scores are too low, skip
            if test in student_scores and student_scores[test] < min_val:
                test_score_ok = False
                break
            elif test not in student_scores and min_val is not None:
                test_score_ok = False
                break
        if not test_score_ok:
            continue

        # Location filter if important
        if location_important:
            college_states = [state.upper() for state in col.get("states", [])]
            if not any(state.upper() in college_states for state in desired_states):
                continue

        matches.append(col)

    return matches
