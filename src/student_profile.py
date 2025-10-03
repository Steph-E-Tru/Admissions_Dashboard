#Function 1: Create Student Profile

def create_student_profile(name: str, gpa: float, interests: list, degree_level: str, test_scores: dict, location_important: bool, desired_states: list = None) -> dict:
    """Create an expanded student profile.
    Args:
        name: Student's name (string)
        gpa: Student's GPA (float)
        interests: List of subjects/majors (list of str)
        degree_level: Degree being sought (e.g., 'undergraduate', 'bachelor', 'associate')
        test_scores: Dictionary of standardized test scores (e.g., {'SAT': 1490, 'ACT': 32, ...})
        location_important: Is location/proximity to home important? (True/False)
        desired_states: List of preferred states, if location is important (list of str)
    Returns:
        Dictionary representing the student's profile.
    """
    profile = {
        "name": name,
        "gpa": gpa,
        "interests": interests,
        "degree_level": degree_level,
        "test_scores": test_scores,
        "location_important": location_important,
        "desired_states": desired_states if location_important else [],
    }
    # Add a tag to indicate profile is ready for college search
    profile["search_ready"] = True
    return profile
