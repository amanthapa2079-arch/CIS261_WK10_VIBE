# Aman Thapa
# CIS261
# WK10 VIBE Coding

from __future__ import annotations

from pathlib import Path
from typing import List


class Student:
    def __init__(self, name: str, student_id: str, test1: float, test2: float, test3: float) -> None:
        self.name = name.strip()
        self.id = student_id.strip()
        self.test_scores = [test1, test2, test3]
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return round(sum(self.test_scores) / len(self.test_scores), 2)

    def calculate_grade(self) -> str:
        average = self.average
        if average >= 90:
            return "A"
        if average >= 80:
            return "B"
        if average >= 70:
            return "C"
        if average >= 60:
            return "D"
        return "F"

    def to_line(self) -> str:
        return "|".join(
            [
                self.name,
                self.id,
                f"{self.test_scores[0]:.2f}",
                f"{self.test_scores[1]:.2f}",
                f"{self.test_scores[2]:.2f}",
                f"{self.average:.2f}",
                self.grade,
            ]
        )

    @classmethod
    def from_line(cls, line: str) -> "Student":
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 7:
            raise ValueError("Invalid student record format")
        name, student_id, test1, test2, test3, average, grade = parts
        student = cls(name, student_id, float(test1), float(test2), float(test3))
        student.average = float(average)
        student.grade = grade
        return student

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Test 1: {self.test_scores[0]:.2f}\n"
            f"Test 2: {self.test_scores[1]:.2f}\n"
            f"Test 3: {self.test_scores[2]:.2f}\n"
            f"Average: {self.average:.2f}\n"
            f"Grade: {self.grade}"
        )


class StudentGradeCalculator:
    def __init__(self, filename: str = "student_grades.txt") -> None:
        self.filename = Path(filename)
        self.students: List[Student] = []

    def load_students(self) -> None:
        if not self.filename.exists():
            print("No saved student file found. Starting with an empty list.")
            return

        try:
            with self.filename.open("r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
        except OSError as error:
            print(f"Error reading file: {error}")
            return

        self.students = []
        for line in lines:
            try:
                self.students.append(Student.from_line(line))
            except ValueError as error:
                print(f"Skipping invalid record: {error}")

        print(f"Loaded {len(self.students)} student record(s).")

    def save_students(self) -> None:
        try:
            with self.filename.open("w", encoding="utf-8") as file:
                for student in self.students:
                    file.write(student.to_line() + "\n")
            print(f"Student records saved to {self.filename.name}.")
        except OSError as error:
            print(f"Error saving file: {error}")

    def add_student(self) -> None:
        name = input("Enter student name: ").strip()
        if not name:
            raise ValueError("Student name cannot be empty.")

        student_id = input("Enter student ID: ").strip()
        if not student_id:
            raise ValueError("Student ID cannot be empty.")

        test1 = self.get_valid_score("Enter Test 1 score (0-100): ")
        test2 = self.get_valid_score("Enter Test 2 score (0-100): ")
        test3 = self.get_valid_score("Enter Test 3 score (0-100): ")

        student = Student(name, student_id, test1, test2, test3)
        self.students.append(student)
        self.save_students()
        print(f"Added student: {student.name}")

    def get_valid_score(self, prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt))
                if 0 <= value <= 100:
                    return value
                print("Score must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

    def display_all_students(self) -> None:
        if not self.students:
            print("No student records to display.")
            return

        print("\nStudent Grade Report")
        print("-" * 100)
        print(f"{'Name':<15} {'ID':<10} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>8} {'Grade':>6}")
        print("-" * 100)
        for student in self.students:
            print(
                f"{student.name:<15} {student.id:<10} {student.test_scores[0]:>8.2f} {student.test_scores[1]:>8.2f} {student.test_scores[2]:>8.2f} {student.average:>8.2f} {student.grade:>6}"
            )

    def display_class_statistics(self) -> None:
        if not self.students:
            print("No student records available for statistics.")
            return

        averages = [student.average for student in self.students]
        highest_student = max(self.students, key=lambda s: s.average)
        lowest_student = min(self.students, key=lambda s: s.average)
        class_average = round(sum(averages) / len(averages), 2)

        print("\nClass Statistics")
        print("-" * 40)
        print(f"Highest Average: {highest_student.name} ({highest_student.average:.2f})")
        print(f"Lowest Average: {lowest_student.name} ({lowest_student.average:.2f})")
        print(f"Class Average: {class_average:.2f}")

    def search_student(self) -> None:
        search_name = input("Enter student name to search: ").strip().lower()
        if not search_name:
            print("Search name cannot be empty.")
            return

        matches = [student for student in self.students if search_name in student.name.lower()]
        if not matches:
            print("No matching student found.")
            return

        print("\nMatching Students")
        print("-" * 40)
        for student in matches:
            print(student)
            print("-" * 25)

    def display_menu(self) -> None:
        print("\nStudent Grade Calculator")
        print("1. Add a new student")
        print("2. Display all students")
        print("3. Search for a student")
        print("4. Show class statistics")
        print("5. Exit")
        print("Press ESC or type 5 to exit.")

    def run(self) -> None:
        self.load_students()
        print("Welcome to the Student Grade Calculator.")

        while True:
            self.display_menu()
            choice = input("Choose an option: ").strip()

            if choice in {"", "\x1b", "esc", "ESC"}:
                print("Exiting program. Goodbye!")
                self.save_students()
                break

            try:
                if choice == "1":
                    self.add_student()
                elif choice == "2":
                    self.display_all_students()
                elif choice == "3":
                    self.search_student()
                elif choice == "4":
                    self.display_class_statistics()
                elif choice == "5":
                    print("Exiting program. Goodbye!")
                    self.save_students()
                    break
                else:
                    print("Please enter a valid option.")
            except ValueError as error:
                print(f"Error: {error}")


def main() -> None:
    calculator = StudentGradeCalculator()
    calculator.run()


if __name__ == "__main__":
    main()
