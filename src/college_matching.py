# Function 2: Match Colleges to Student Profile
def match_colleges(student: dict, colleges: list) -> list:
    """Find colleges matching the student's interests and GPA.
    Args:
        student: Student profile (dict)
        colleges: List of college dicts with 'major' and 'min_gpa'
    Returns:
        Matched colleges as a list of dicts
    """
    matches = []

    # Convert all student interests to lowercase once to avoid issues with case-sensitivity
    student_interests = [interest.lower() for interest in student["interests"]]

    for col in colleges:
        # Convert each college's majors to lowercase
        college_majors = [major.lower() for major in col["majors"]]

        # Check for overlap (case-insensitive)
        if any(interest in college_majors for interest in student_interests):
            # Then also check GPA requirement
            if student["gpa"] >= col["min_gpa"]:
                matches.append(col)  # Add if both conditions met
    return matches
