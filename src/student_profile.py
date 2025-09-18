#Function 1: Create Student Profile

def create_student_profile(name: str, gpa: float, interests: list) -> dict:
    """Create a simple student profile.
    Args:
        name: Student's name (string)
        gpa: Student's GPA (float)
        interests: List of subjects/majors interested in (list of str)
    Returns:
        A dictionary with name, gpa, and interests.
    """
    profile = {"name": name, "gpa": gpa, "interests": interests}  # Collect info
    # Add a tag to indicate profile is ready for college search
    profile["search_ready"] = True
    return profile
