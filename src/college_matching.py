# Function 2: Match Colleges to Student Profile
import ast

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
        # Major match
        college_major = col.get("program_type", "").lower().strip()
        if not any(interest == college_major for interest in student_interests):
            continue
            
        # Degree match
        try:
            degrees = ast.literal_eval(col.get("degree_level", "[]"))
            college_degrees = [d.lower().strip() for d in degrees]
        except Exception:
            college_degrees = []
        if student_degree not in college_degrees:
            continue
        
        # Minimum GPA
        try:
            min_gpa = float(col.get("minimum_gpa") or 0.0)
        except (ValueError, TypeError):
            min_gpa = 0.0
        if student["gpa"] < min_gpa:
            continue
        
        # Location match
        if location_important:
            col_state = col.get("state_location", "").upper().strip()
            if col_state not in desired_states:
                continue
        
        # Academic fit
        advice = ""
        fit_count = 1  # Only GPA is required
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
