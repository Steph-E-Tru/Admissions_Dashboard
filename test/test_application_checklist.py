from src.application_checklist import get_college_checklist

def test_get_college_checklist():
    college = {"name": "Art School", "requirements": ["portfolio", "essay"]}
    checklist = get_college_checklist(college)
    assert isinstance(checklist, list)
    assert "portfolio" in checklist
    assert "Reviewed" in checklist

if __name__ == "__main__":
    test_get_college_checklist()
    print("All checklist tests passed.")
