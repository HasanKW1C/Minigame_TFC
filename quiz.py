def run_quiz(questions):
    score = 0
    for question in questions:
        print(question["prompt"])
        for option in question["options"]:
            print(option)
        answer = input("Enter your answer (A, B, C or D): ").upper()
        if answer == question["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print("Incorrect, the answer was", question["answer"] ,"\n")

    print(f"Your score is {score} out of {len(questions)}")

# LIST OF QUESTIONS
questions = [
    {
        "prompt": "How many days are there in a leap year?",
        "options": ["A. 365", "B. 364", "C. 366", "D. 360"],
        "answer": "C"
    },
    {
        "prompt": "What is your body's largest organ?",
        "options": ["A. Brain", "B. Skin", "C. Veins", "D. Intestines"],
        "answer": "B"
    }
]

run_quiz(questions)