from src.college_matching import match_colleges

def test_match_colleges():
    student = {"name": "Alex", "gpa": 3.5, "interests": ["engineering", "art"]}
    colleges = [
        {"name": "Tech U", "majors": ["Engineering"], "min_gpa": 3.0, "requirements": []},
        {"name": "History College", "majors": ["History"], "min_gpa": 2.5, "requirements": []}
    ]
    matched = match_colleges(student, colleges)
    assert len(matched) == 1
    assert matched[0]["name"] == "Tech U"

if __name__ == "__main__":
    test_match_colleges()
    print("All college matching tests passed.")
