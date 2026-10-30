"""
Menu-driven University Course Prerequisite System built on the generic Graph.
An edge  Y -> X  means "course Y is a prerequisite of course X".
"""
import ui
from course import Course
from graph import Graph

MAX_COURSES = 10  # the brief limits the system to at most 10 courses


def load_sample_data():
    """Create the starting courses and prerequisite links. Returns (graph, courses)."""
    sample_courses = [
        Course("CS101", "Introduction to Programming", 4, "Core",
               "Programming fundamentals using Python."),
        Course("CS102", "Discrete Mathematics", 3, "Core",
               "Logic, sets, relations and proof techniques."),
        Course("CS201", "Data Structures", 4, "Core",
               "Lists, stacks, queues, trees and hash tables."),
        Course("CS202", "Object-Oriented Programming", 4, "Core",
               "Classes, inheritance and design principles."),
        Course("CS301", "Algorithms", 4, "Core",
               "Algorithm design and complexity analysis."),
        Course("CS302", "Database Systems", 3, "Elective",
               "Relational databases and SQL."),
        Course("CS303", "Web Development", 3, "Elective",
               "Building dynamic websites."),
    ]
    prerequisites = [  # (prerequisite, course)
        ("CS101", "CS201"), ("CS102", "CS201"),
        ("CS101", "CS202"),
        ("CS201", "CS301"), ("CS102", "CS301"),
        ("CS201", "CS302"),
        ("CS202", "CS303"),
    ]

    graph = Graph()
    courses = {}  # course code -> Course object
    for course in sample_courses:
        courses[course.code] = course
        graph.addVertex(course.code)
    for prerequisite, course_code in prerequisites:
        graph.addEdge(prerequisite, course_code)
    return graph, courses


# ---------- input helpers ----------

def ask_course(courses, prompt):
    """Ask for a course code. Returns the code if it exists, otherwise None."""
    code = input(prompt).strip().upper()
    if code not in courses:
        ui.error(f"Course '{code}' does not exist.")
        return None
    return code


def ask_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        ui.error("Please enter a whole number greater than 0.")


def ask_level():
    while True:
        answer = input("  Level (core/elective): ").strip().lower()
        if answer in ("core", "c"):
            return "Core"
        if answer in ("elective", "e"):
            return "Elective"
        ui.error("Please type 'core' or 'elective'.")


# ---------- display helpers ----------

def show_menu():
    ui.section("MAIN MENU")
    print("  [1] View all courses          [6] Add a course")
    print("  [2] View course details       [7] Add a prerequisite")
    print("  [3] View course profile       [8] Remove a prerequisite")
    print("  [4] View prerequisites        [9] View prerequisite map")
    print("  [5] View courses unlocked     [0] Exit")


def show_details(course):
    """Print every attribute of a course."""
    print(f"  Code         : {course.code}")
    print(f"  Name         : {course.name}")
    print(f"  Credit hours : {course.credit_hours}")
    print(f"  Level        : {course.level}")
    print(f"  Description  : {course.description or '-'}")


def show_course_list(courses, codes, empty_message):
    if not codes:
        ui.info("  " + empty_message)
        return
    for code in sorted(codes):
        print(f"  - {courses[code]}")


# ---------- menu actions ----------

def view_all_courses(courses):
    ui.section("ALL COURSES")
    print(f"  {'No':<4}{'Code':<8}{'Name':<34}{'Credits':>7}  Level")
    ui.line()
    for number, code in enumerate(sorted(courses), start=1):
        c = courses[code]
        print(f"  {number:<4}{c.code:<8}{c.name[:33]:<34}{c.credit_hours:>7}  {c.level}")
    ui.line()
    print(f"  {len(courses)} of {MAX_COURSES} courses")


def view_course_details(courses):
    ui.section("COURSE DETAILS")
    code = ask_course(courses, "  Course code: ")
    if code:
        print()
        show_details(courses[code])


def view_course_profile(courses):
    ui.section("COURSE PROFILE")
    code = ask_course(courses, "  Course code: ")
    if not code:
        return
    course = courses[code]
    print()
    if course.is_core():
        show_details(course)
    else:
        print(f"  Name         : {course.name}")
        ui.info("  Other details are hidden because this is an elective course.")


def view_prerequisites(graph, courses):
    ui.section("PREREQUISITES")
    code = ask_course(courses, "  Course code: ")
    if code:
        print(f"\n  Prerequisites for {courses[code]}:")
        show_course_list(courses, graph.listIncomingAdjacentVertex(code),
                         "None - this course has no prerequisites.")


def view_unlocked(graph, courses):
    ui.section("COURSES UNLOCKED")
    code = ask_course(courses, "  Course code: ")
    if code:
        print(f"\n  Courses unlocked by {courses[code]}:")
        show_course_list(courses, graph.listOutgoingAdjacentVertex(code),
                         "None - this course is not a prerequisite of any course.")


def add_course(graph, courses):
    ui.section("ADD COURSE")
    if len(courses) >= MAX_COURSES:
        ui.error(f"The system already has the maximum of {MAX_COURSES} courses.")
        return

    code = input("  Course code  : ").strip().upper()
    if not code:
        ui.error("Course code cannot be empty.")
        return
    if code in courses:
        ui.error(f"Course {code} already exists.")
        return
    name = input("  Course name  : ").strip()
    if not name:
        ui.error("Course name cannot be empty.")
        return
    credits = ask_positive_int("  Credit hours : ")
    level = ask_level()
    description = input("  Description  : ").strip()

    course = Course(code, name, credits, level, description)
    courses[code] = course
    graph.addVertex(code)
    print()
    ui.success(f"Course {course} added.")
    ui.info("  Use option [7] to give it prerequisites.")


def add_prerequisite(graph, courses):
    ui.section("ADD PREREQUISITE")
    course = ask_course(courses, "  Course (X)           : ")
    if not course:
        return
    prerequisite = ask_course(courses, "  New prerequisite (Y) : ")
    if not prerequisite:
        return

    print()
    if prerequisite == course:
        ui.error("A course cannot be a prerequisite of itself.")
    elif graph.hasEdge(prerequisite, course):
        ui.error(f"{prerequisite} is already a prerequisite of {course}.")
    elif graph.hasPath(course, prerequisite):
        # course already leads to prerequisite, so Y -> X would close a loop
        ui.error(f"Not allowed: {prerequisite} already requires {course} "
                 f"(directly or indirectly). This would create a circular prerequisite.")
    else:
        graph.addEdge(prerequisite, course)
        ui.success(f"{prerequisite} is now a prerequisite of {course}.")


def remove_prerequisite(graph, courses):
    ui.section("REMOVE PREREQUISITE")
    course = ask_course(courses, "  Course (X): ")
    if not course:
        return
    current = graph.listIncomingAdjacentVertex(course)
    if not current:
        ui.info(f"  {course} has no prerequisites to remove.")
        return

    print(f"\n  Current prerequisites of {courses[course]}:")
    show_course_list(courses, current, "")
    prerequisite = ask_course(courses, "\n  Prerequisite to remove (Y): ")
    if not prerequisite:
        return

    print()
    if graph.removeEdge(prerequisite, course):
        ui.success(f"{prerequisite} is no longer a prerequisite of {course}.")
    else:
        ui.error(f"{prerequisite} is not a prerequisite of {course}.")


def view_prerequisite_map(graph, courses):
    ui.section("PREREQUISITE MAP")
    print(f"  {'Code':<8}{'Name':<34}Requires")
    ui.line()
    for code in sorted(courses):
        required = sorted(graph.listIncomingAdjacentVertex(code))
        text = ", ".join(required) if required else "-"
        print(f"  {code:<8}{courses[code].name[:33]:<34}{text}")
    ui.line()


# ---------- main program ----------

def main():
    graph, courses = load_sample_data()

    ui.banner("UNIVERSITY COURSE PREREQUISITE SYSTEM",
              "Directed Graph | Edge Y -> X means Y is a prerequisite of X")
    ui.info(f"Loaded {len(courses)} courses.")

    actions = {
        "1": lambda: view_all_courses(courses),
        "2": lambda: view_course_details(courses),
        "3": lambda: view_course_profile(courses),
        "4": lambda: view_prerequisites(graph, courses),
        "5": lambda: view_unlocked(graph, courses),
        "6": lambda: add_course(graph, courses),
        "7": lambda: add_prerequisite(graph, courses),
        "8": lambda: remove_prerequisite(graph, courses),
        "9": lambda: view_prerequisite_map(graph, courses),
    }

    while True:
        show_menu()
        choice = input("\n  Enter choice: ").strip()

        if choice == "0":
            ui.success("Exiting program. Goodbye!")
            break
        if choice in actions:
            actions[choice]()
        else:
            ui.error("Invalid choice, please enter 0-9.")


if __name__ == "__main__":
    main()