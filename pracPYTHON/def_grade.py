def get_grade():
    while True:
        try:
            grade = int(input("Enter grade: "))

            if grade >= 90 and grade <= 100:
                print("A")
            elif grade >= 80 and grade < 90:
                print("B")
            elif grade >= 70 and grade < 80:
                print("C")
            elif grade >= 60 and grade < 70:
                print("D")
            elif grade < 60 and grade >= 0:
                print("F")
            else:
                raise ValueError("Invalid input! Grade must be 0–100.")
        except ValueError as e:
            print("Error:", e)
        else:
            print("Grade successfully computed.")
            break
        finally:
            print("Done.")

get_grade()
