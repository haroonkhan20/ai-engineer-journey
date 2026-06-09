def get_grade(score):
    if score >= 95: return "A+"
    elif score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: 
        return "F"
    
def get_average(scores):
    return sum(scores)/len(scores)

def save_report(name, scores, average, grade):

    with open("report.txt", "w") as f:
        f.write(f"Student Report\n")
        f.write(f"{'='*30}\n")
        f.write(f"Name    : {name}\n")
        f.write(f"Scores  : {scores}\n")
        f.write(f"Average : {average:.2f}\n")
        f.write(f"Grade   : {grade}\n")
        
    print("Report saved to report.txt!")

def main():
    print("="*35)
    print("   Student Grade Calculator")
    print("="*35)

    name = input("Student Name: ")
    scores = []
    subjects = ["Maths", "Science", "English", "History", "Python", "AI Fundamentals"]
   
    for subject in subjects:
        score = float(input(f"  {subject} score (0-100): "))
        scores.append(score)
   
    average = get_average(scores)
    grade = get_grade(average)
    max_score = max(scores)
    min_score = min(scores)
    max_sub   = subjects[scores.index(max_score)]
    min_sub   = subjects[scores.index(min_score)]
   
    print(f"\n{'='*35}")
    print(f"  Report for {name}")
    print(f"{'='*35}")
   
    for i, subject in enumerate(subjects):
        print(f"  {subject:<10}: {scores[i]:.1f}  ({get_grade(scores[i])})")
    print(f"{'─'*35}")
    print(f"  Average   : {average:.2f}")
    print(f"  Grade     : {grade}")
    print(f"Best subject  : {max_sub} ({max_score})")
    print(f"Worst subject : {min_sub} ({min_score})")
    print(f"{'='*35}")

    if average >= 90: 
        print("Outstanding performance! 🏆")
    elif average >= 80:
        print("Great job! Keep it up! 👍")
    elif average >= 70:
        print("Good effort, room to improve 📈")
    elif average >= 60:
        print("Needs more work, don't give up 💪")
    else: 
        print("Please seek extra help 📚")

    save = input("Do you want to save the report (y/n)?: ").upper()
    if save == "Y":    
        save_report(name, scores, average, grade)
    else:     
        print("Thank you")

if __name__ == "__main__":
    main()