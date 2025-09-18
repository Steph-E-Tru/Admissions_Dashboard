from src.student_profile import create_student_profile

def test_create_student_profile():
    profile = create_student_profile("Alex", 3.4, ["engineering", "biology"])
    assert isinstance(profile, dict)
    assert profile["name"] == "Alex"
    assert profile["gpa"] == 3.4
    assert "biology" in profile["interests"]

if __name__ == "__main__":
    test_create_student_profile()
    print("All student profile tests passed.")
