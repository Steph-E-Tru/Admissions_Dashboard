# Function 2: Match Colleges to Student Profile
import ast

def match_colleges(student: dict, colleges: list) -> list:
    """
    Match colleges to student profile based on interests, GPA, degree level, test scores, and location preferences.
    Args:
        student: Student profile (dict)
        colleges: List of college dicts from CSV
    Returns:
        List of matched college dicts
    """
    matches = []

    # Lowercase interests for matching
    student_interests = [interest.lower().strip() for interest in student.get("interests", [])]
    student_degree = student.get("degree_level", "").lower().strip()
    student_scores = student.get("test_scores", {})
    location_important = student.get("location_important", False)
    desired_states = [state.upper().strip() for state in student.get("desired_states", [])]

    for col in colleges:
        # Major match: substring, not exact
        college_major = str(col.get("program_type", "")).lower().strip()
        if not any(interest in college_major or college_major in interest for interest in student_interests):
            continue

        # Degree match: handle both list and string
        degree_level_val = col.get("degree_level", "")
        try:
            degrees = ast.literal_eval(degree_level_val) if degree_level_val.startswith("[") else [degree_level_val]
        except Exception:
            degrees = [degree_level_val]
        college_degrees = [str(d).lower().strip() for d in degrees if str(d).strip()]
        if student_degree and student_degree not in college_degrees:
            continue

        # Minimum GPA
        try:
            min_gpa = float(col.get("minimum_gpa") or 0.0)
        except (ValueError, TypeError):
            min_gpa = 0.0
        if student.get("gpa", 0.0) < min_gpa:
            continue

        # Location match
        if location_important:
            col_state = str(col.get("state_location", "")).upper().strip()
            if col_state and col_state not in desired_states:
                continue

        # Academic fit (for display only)
        advice = ""
        fit_count = 1  # GPA is always checked
        fit_list = ["GPA"]
        try:
            min_sat = float(col.get("minimum_sat")) if col.get("minimum_sat") not in ["", None] else None
        except:
            min_sat = None
        try:
            min_act = float(col.get("minimum_act")) if col.get("minimum_act") not in ["", None] else None
        except:
            min_act = None
        sat_score = student_scores.get("SAT", None)
        act_score = student_scores.get("ACT", None)
        if min_sat is not None and sat_score is not None and sat_score >= min_sat:
            fit_count += 1
            fit_list.append("SAT")
        if min_act is not None and act_score is not None and act_score >= min_act:
            fit_count += 1
            fit_list.append("ACT")
        summary = f"Academic fit: {fit_count}/3 met ({', '.join(fit_list)})"
        if min_sat is not None and (sat_score is None or sat_score < min_sat):
            advice += "Your SAT score is below the college's suggestion, but you can still apply. "
        if min_act is not None and (act_score is None or act_score < min_act):
            advice += "Your ACT score is below the college's suggestion, but you can still apply. "

        # Build result
        match = dict(col)
        match["academic_fit_summary"] = summary
        if advice:
            match["academic_fit_advice"] = advice.strip()
        matches.append(match)
    return matches
