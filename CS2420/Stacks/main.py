"""
Pseudocode for main program:1.open file data.txt2.read an infix
expression from the file3.display the infix expression5.display the
postfix expression6.call function eval_postfix(expr)which you write
eval_postfix()takes a postfix string as input and returns a number.
If the expression is not valid, raise a SyntaxError.7.display the
result of eval_postfix()Output must match the format shown in Figure
1 below.
Welcome to main. The main file has a couple of things. I has 2 functions,
in2post() and eval_postfix(), which takes an infix expression to convert
it to a postfix expression and evaluates a postfix expression
respectively. It also has main() which opens and reads data.txt which
contains all the expressions.
"""

from stack import Stack

def in2post(exp):
    """
    in2post() takes an expression which needs to be a string, otherwise
    it will raise a ValueError. If the expression is not valid, like if
    the equation isn't balanced, it raises a SyntaxError. Takes a
    string, representing the infix expression, checks that it's balanced
    and then returns a string representing the postfix expression.
    """
    new_stack = Stack()
    precendence = {
        "%" : 2,
        "*" : 2,
        "/" : 2,
        "+" : 1,
        "-" : 1,
        "{" : 0,
        "(" : 0,
        "[" : 0
    }
    result = []
    if not isinstance(exp, str):
        raise ValueError
    #Checking first if expression is balanced (has good amount of parans)
    for item in exp:
        if item in ["[", "(", "{"]:
            new_stack.push(item)
        elif item in ["]", ")", "}"]:
            if new_stack.size() == 0:
                raise SyntaxError
            stack_item = new_stack.pop()
            if item == "]" and stack_item != "[" or item == ")" and \
                stack_item != "(" or item == "}" and stack_item != "{":
                raise SyntaxError
    #Clear stack and start working on changing it over
    new_stack.clear()
    for item in exp:
        if item == " ":
            continue
        if item in "1234567890":
            result.append(item)
        elif item in "[({":
            new_stack.push(item)
        elif item in "])}":
            stack_item = new_stack.pop()
            while stack_item not in "[({":
                result.append(stack_item)
                stack_item = new_stack.pop()
        else:
            while (new_stack.size() > 0) and (precendence[new_stack.top()]\
                >= precendence[item]):
                result.append(new_stack.pop())
            new_stack.push(item)
    #Ok, we got all the numbers and operands as they should be listed
    #except the end ones. Time to dump the stack
    while new_stack.size() > 0:
        result.append(new_stack.pop())

    return " ".join(result)

def eval_postfix(exp):
    """
    eval_postfix() takes an expression which needs to be a string, otherwise
    it will raise a ValueError. If the expression is not valid, like if
    there are too many operators, it raises a SyntaxError. Takes a string,
    representing the postfix expression, and then returns a float which is
    the answer to the postfix expression.
    """
    new_stack = Stack()
    if not isinstance(exp, str):
        raise ValueError

    for item in exp:
        if item == " ":
            continue
        if item in "1234567890":
            new_stack.push(float(item))
        elif item in "*/%+-":
            if new_stack.size() < 2:
                raise SyntaxError
            second_number = new_stack.pop()
            first_number = new_stack.pop()
            new_stack.push(eval(f"{first_number} {item} {second_number}"))
    return new_stack.pop()

def main():
    """
    main(), this is it. Reads in the infix expression from data.txt after
    opening it. Displays the infix expression, calls in2post(), displays the
    postfix expression, calls eval_postfix(), then displays the result!
    """
    with open("data.txt", "r") as file:
        for line in file:
            strip_line = line.rstrip("\n")
            print(f"infix: {strip_line}")
            new_line = in2post(strip_line)
            print(f"postfix: {new_line}")
            result = eval_postfix(new_line)
            print(f"answer: {result}")
            print()

if __name__ == "__main__":
    main()
