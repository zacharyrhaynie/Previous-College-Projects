"""
Defines the Course class.
"""

class Course:
    """
    Class of courses. Recieves a course number (int), course name (string), course credit (float),
    and course GPA (float). Possibly is assigned a next to refence the next object of the list.
    """

    def __init__(self, c_number=0, c_name="", c_credit_hr=0.0, c_grade=0.0):
        """
        Initializes the function and takes the info it's passed in and validates it first to
        make sure all the values are correct, otherwise it raises an error.
        """
        if isinstance(c_number, int):
            if c_number >= 0:
                self.c_number = c_number
            else:
                raise ValueError('Course number must be a number, and be positive!')
        else:
            raise ValueError('Course number must be a number, and be positive!')

        if isinstance(c_name, str):
            self.c_name = c_name
        else:
            raise ValueError("Course name must be a string!")

        if isinstance(c_credit_hr, float):
            if c_credit_hr >= 0:
                self.c_credit_hr = c_credit_hr
            else:
                raise ValueError("Course credit hours must be a float,\
                and greater than or equal to 0!")
        else:
            raise ValueError("Course credit hours must be a float, and greater than or equal to 0!")

        if isinstance(c_grade, float):
            if c_grade >= 0:
                self.c_grade = c_grade
            else:
                raise ValueError("Course grade must be a float, and between 0.0 and 4.0!")
        else:
            raise ValueError("Course grade must be a float, and between 0.0 and 4.0!")

        self.next = None

    def number(self):
        """#Way to get the number of the course"""
        return self.c_number

    def name(self):
        """Way to get the course name"""
        return self.c_name

    def credit_hr(self):
        """Way to get the course's credit hours"""
        return self.c_credit_hr

    def grade(self):
        """Way to get the grade recieved in the course"""
        return self.c_grade

    def __str__(self):
        """Returns the string for the object"""
        return f"cs{self.c_number} {self.c_name}"+ \
        f" Grade:{self.c_grade} Credit Hours: {self.c_credit_hr}"
