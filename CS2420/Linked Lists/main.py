"""
Drivers for the project. I copied these from Romina Owen's (the TA) post in Microsoft
Teams as I took it be an example of the drivers required.
"""
from course import Course
from courselist import CourseList

def main():
    ''' driver code to load courses into CourseList from data.txt file '''
    course_list = CourseList()
    number, name, credit, grade = range(4)
    with open("data.txt") as file:
        for line in file:
            data = line.strip().split(",")
            course_list.insert(Course(int(data[number]), data[name], \
            float(data[credit]), float(data[grade])))

    size = course_list.size()
    print(f"Current List: ({size})")
    print(course_list)
    print()
    print(f"Cumulative GPA: {course_list.calculate_gpa():.3f}")
    print()

if __name__ == "__main__":
    main()
