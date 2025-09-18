# Function 3: Get College Checklist
def get_college_checklist(college: dict) -> list:
    """Return the application requirements checklist for a given college.
    Args:
        college: College dict with 'requirements' field
    Returns:
        List of requirement strings (list)
    """
    # Use .get to avoid KeyError if missing
    checklist = college.get("requirements", [])  # Safe extract
    # Add a 'Reviewed' flag for demo
    return checklist + ["Reviewed"]
