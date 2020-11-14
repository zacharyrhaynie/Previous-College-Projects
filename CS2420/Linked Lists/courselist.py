"""
Defines the CourseList class and does all the work for a linked list.
"""
class CourseList:
    """
    Does all the hard work in creating a linked list. Gets called on by the drivers in main and
    (when making a new course) fed a course number (int), name (string), credit hour (float), and
    grade (float).
    """
    def __init__(self):
        """
        Initializes with an empty head.
        """
        self.head = None

    def insert(self, course):
        """
        Starts off the insertion bandwagon by being fed a course and then feeding it into a
        insertion helper.
        """
        if self.head is None:
            self.head = course
            return self.head

        if course.number() <= self.head.number():
            course.next = self.head
            self.head = course
            return self.head

        heading = self.head
        while heading.next is not None and heading.next.number() < course.number():
            heading = heading.next

        course.next = heading.next
        heading.next = course

    def size(self):
        """
        Returns the size of the head, or how many items have been inserted
        """
        list_size = 0
        heading = self.head
        while heading is not None:
            list_size += 1
            heading = heading.next
        return list_size

    def __str__(self):
        """
        Joins all the printed __str__s of the indiviual courses within course list
        and prints them all seperated on their own lines.
        """
        string = ""
        heading = self.head
        while heading is not None:
            string = string + "\n" + str(heading)
            heading = heading.next
        return string

    def calculate_gpa(self):
        """
        Calculates the GPA by multiplying them by credit hours then adding them all up
        then dividing by credit hours.
        """
        gpa = 0.0
        hours = 0
        heading = self.head
        while heading is not None:
            hours += heading.credit_hr()
            gpa += (heading.grade() * heading.credit_hr())
            heading = heading.next
        if gpa == 0 or hours == 0:
            return 0.00
        return gpa/hours

    def is_sorted(self):
        """
        Checks if self.head is sorted
        """
        if self.head is None:
            return True
        heading = self.head
        while heading.next is not None:
            if heading.number() > heading.next.number():
                return False
            heading = heading.next
        return True

    def find(self, number):
        """
        Find the first iteration of a number it's passed or returns -1.
        """
        heading = self.head
        while heading is not None:
            if heading.number() == number:
                return heading
            heading = heading.next
        return -1

    def remove(self, number):
        """
        Removes an entry from the head when given the entry.
        """
        previous_heading = None
        heading = self.head

        while heading is not None:
            if heading.number() == number:
                if previous_heading is not None:
                    previous_heading.next = heading.next
                else:
                    self.head = self.head.next
                return True
            previous_heading = heading
            heading = heading.next

    def remove_all(self, number):
        """
        Removes every instance of a number within the head.
        """
        previous_heading = None
        heading = self.head

        while heading is not None and heading.number() == number:
            self.head = heading.next
            heading = self.head
        
        while heading is not None:
            while heading is not None and heading.number() != number:
                previous_heading = heading
                heading = heading.next
            if heading is None:
                return self.head
            previous_heading.next = heading.next
            heading = previous_heading.next
    
    def __iter__(self):
        """
        Makes a CourseList Object iterable.
        """
        self.heading = self.head
        return self

    def __next__(self):
        """
        Iterates next as next is called on the CourseList Object and
        raises an objection if you iterate too far. 
        """
        if self.heading:
            self.heading = self.heading.next
            if not self.heading:
                raise StopIteration("No more courses.")
            else:
                return self.heading.name()
