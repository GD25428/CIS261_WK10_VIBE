# Donovan Gonzalez
# CIS261
# VIBE coding

"""Student record manager with persistent grades and class statistics."""

DATA_FILE = "student_grades.txt"


class ExitProgram(Exception):
	"""Raised when the user chooses to exit with ESC."""


class Student:
	"""Store one student's identifying information and calculated grades."""

	def __init__(self, name, student_id, scores):
		self.name = name
		self.id = student_id
		self.test_scores = scores
		self.average = calculate_average(scores)
		self.grade = calculate_letter_grade(self.average)

def calculate_average(scores):
	"""Return the average of three test scores."""
	return sum(scores) / len(scores)


def calculate_letter_grade(average):
	"""Return the letter grade for an average percentage."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def prompt(text):
	"""Read input and allow ESC to exit from any prompt."""
	value = input(text)
	if value.strip().upper() == "ESC" or "\x1b" in value:
		raise ExitProgram
	return value.strip()


def get_score(test_number):
	"""Read one valid score from 0 through 100."""
	while True:
		try:
			score = float(prompt(f"Test {test_number} score (0-100): "))
		except ValueError:
			print("Please enter a number from 0 to 100.")
			continue

		if 0 <= score <= 100:
			return score
		print("Score must be between 0 and 100.")


def create_student(students):
	"""Prompt for and add one student record."""
	name = prompt("Student name: ")
	if not name:
		print("Name cannot be blank.")
		return

	student_id = prompt("Student ID: ")
	if not student_id:
		print("Student ID cannot be blank.")
		return
	if any(student.id.lower() == student_id.lower() for student in students):
		print("That student ID already exists.")
		return

	scores = [get_score(number) for number in range(1, 4)]
	average = calculate_average(scores)
	students.append(Student(name, student_id, scores))
	print(f"Added {name} with average {average:.2f} ({students[-1].grade}).")


def display_students(students):
	"""Display all students in a formatted table."""
	if not students:
		print("No student records found.")
		return

	print("\nStudent Records")
	print("-" * 88)
	print(f"{'Name':<24} {'ID':<14} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>7}")
	print("-" * 88)
	for student in students:
		scores = student.test_scores
		print(
			f"{student.name:<24.24} {student.id:<14.14} "
			f"{scores[0]:>8.2f} {scores[1]:>8.2f} {scores[2]:>8.2f} "
			f"{student.average:>9.2f} {student.grade:>7}"
		)
	print("-" * 88)


def display_statistics(students):
	"""Display highest, lowest, and overall class averages."""
	if not students:
		print("No class statistics are available.")
		return

	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {calculate_average(averages):.2f}")


def search_students(students):
	"""Find and display students whose names contain the search text."""
	search_text = prompt("Search by student name: ").lower()
	matches = [student for student in students if search_text in student.name.lower()]
	if not matches:
		print("No matching students found.")
		return
	display_students(matches)


def save_students(students):
	"""Save student records to the required text file."""
	try:
		with open(DATA_FILE, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student.name}|{student.id}|{student.test_scores[0]:.2f}|"
					f"{student.test_scores[1]:.2f}|{student.test_scores[2]:.2f}|"
					f"{student.average:.2f}|{student.grade}\n"
				)
		saved_message = f"Saved {len(students)} student record(s) to {DATA_FILE}."
		print(saved_message)
		return True
	except OSError as error:
		print(f"Unable to save records to {DATA_FILE}: {error}")
		return False


def load_students():
	"""Load valid student records, returning an empty list if none exist."""
	try:
		with open(DATA_FILE, "r", encoding="utf-8") as file:
			lines = file.readlines()
	except FileNotFoundError:
		return []
	except OSError:
		print(f"Could not read {DATA_FILE}; starting with no records.")
		return []

	valid_students = []
	for line in lines:
		fields = line.strip().split("|")
		if len(fields) != 7:
			continue
		try:
			name, student_id = fields[0], fields[1]
			scores = [float(score) for score in fields[2:5]]
			if len(scores) != 3 or not all(0 <= score <= 100 for score in scores):
				continue
		except (TypeError, ValueError):
			continue
		if not name or not student_id:
			continue
		valid_students.append(Student(name, student_id, scores))
	return valid_students


def display_menu():
	print("\nStudent Grade Manager")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by student name")
	print("5. Save records")
	print("ESC. Save and exit")


def main():
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s) from {DATA_FILE}.")

	try:
		while True:
			display_menu()
			choice = prompt("Choose an option: ").upper()
			if choice == "1":
				create_student(students)
			elif choice == "2":
				display_students(students)
			elif choice == "3":
				display_statistics(students)
			elif choice == "4":
				search_students(students)
			elif choice == "5":
				save_students(students)
			elif choice == "ESC":
				break
			else:
				print("Please choose 1-5 or press ESC to exit.")
	except (ExitProgram, EOFError, KeyboardInterrupt):
		print("\nExiting program.")
	finally:
		save_students(students)


if __name__ == "__main__":
	main()