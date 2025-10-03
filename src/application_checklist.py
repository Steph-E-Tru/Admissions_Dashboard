# Function 3: Get College Checklist
def get_college_checklist(college: dict, completed: set = None) -> list:
    """
    Return the application requirements checklist for a given college with completion tracking.
    Args:
        college: College dict with 'requirements' field (list of strings)
        completed: Set of requirements the user has already completed (set of strings)
    Returns:
        List of dicts with 'requirement' and 'completed' keys.
    """
    # Extract requirements from the college dictionary; default to empty if not present
    checklist_items = college.get("requirements", [])
    completed = completed or set()
    checklist = []
    # Iterate through each requirement in the college's list
    for item in checklist_items:
        checklist.append({
            "requirement": item,
            "completed": item in completed
        })
    # Return the full checklist (with completion status)
    return checklist
