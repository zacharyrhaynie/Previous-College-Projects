"""
Welcome to stack.py. Here lies the stack class.
"""

class Stack:
    """
    The stack class. A stack object has a couple methods. It has push(),
    pop(), top(), size() and clear().
    """
    def __init__(self):
        """
        Initializes the stack object with a list that simulates the stack.
        I know this has it's own disadvantages, but no where in the
        instructions did it say I couldn't use a list, and it seems
        to be easier than using an array or a linked list (though I may
        try those on my own because it seems like it would be a good
        learning experience).
        """
        self.stack = []

    def push(self, item):
        """
        Adds an item to the stack.
        """
        self.stack.append(item)

    def pop(self):
        """
        Firstly, raises an IndexError if the stack is empty. Removes the
        top item from the stack and returns it.
        """
        if self.size() == 0:
            raise IndexError
        return self.stack.pop()

    def top(self):
        """
        Firstly, raises an IndexError if the stack is empty. Returns the
        top item of the stack without removing it.
        """
        if self.size() == 0:
            raise IndexError
        return self.stack[len(self.stack) - 1]

    def size(self):
        """
        Returns the size of the stack. Could've just called len() on
        self.stack but I decided to have it be part of the state too.
        """
        return len(self.stack)

    def clear(self):
        """
        Clears the stack and sets self.size to 0.
        """
        self.stack.clear()
