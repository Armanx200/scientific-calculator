import re
import math

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
 
class Stack:
    def __init__(self):
        self.head = Node("head")
        self.size = 0

    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def getSize(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def peek(self):
        if self.isEmpty():
            raise Exception("Peeking from an empty stack")
        return self.head.next.value
 
    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1
 
    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value

class Calculate:
    def __init__(self, equation: str):
        self.equation = self.preprocess(equation)
        
    def preprocess(self, equation: str) -> str:
        # Handle trigonometric and logarithmic functions
        equation = re.sub(r'cos\(([^)]+)\)', lambda m: str(math.cos(math.radians(float(m.group(1))))), equation)
        equation = re.sub(r'sin\(([^)]+)\)', lambda m: str(math.sin(math.radians(float(m.group(1))))), equation)
        equation = re.sub(r'log\(([^,]+),\s*([^)]+)\)', lambda m: str(math.log(float(m.group(1)), float(m.group(2)))), equation)
        return equation
        
    def InfixToPostfix(self):
        Operators = set(['+', '-', '*', '/', '(', ')', '^'])
        Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        stack = Stack()
        output = []
        put = ''

        for character in self.equation:
            if character.isdigit() or character == '.':
                put += character
            elif character == '(':
                if put:
                    output.append(put)
                    put = ''
                stack.push('(')
            elif character == ')':
                if put:
                    output.append(put)
                    put = ''
                while not stack.isEmpty() and stack.peek() != '(':
                    output.append(stack.pop())
                stack.pop()  # Pop the '('
            elif character in Operators:
                if put:
                    output.append(put)
                    put = ''
                while (not stack.isEmpty()) and stack.peek() in Operators and Priority[character] <= Priority[stack.peek()]:
                    output.append(stack.pop())
                stack.push(character)

        if put:
            output.append(put)

        while not stack.isEmpty():
            output.append(stack.pop())

        self.postfix = output
        return output

    def compute(self):
        Operators = set(['+', '-', '*', '/', '^'])
        postfix = self.InfixToPostfix()
        stack = Stack()

        for character in postfix:
            if character not in Operators:
                stack.push(character)
            else:
                a = float(stack.pop())
                b = float(stack.pop())
                if character == '+':
                    stack.push(b + a)
                elif character == '-':
                    stack.push(b - a)
                elif character == '*':
                    stack.push(b * a)
                elif character == '/':
                    if a == 0:
                        raise ZeroDivisionError("Division by zero.")
                    stack.push(b / a)
                elif character == '^':
                    stack.push(b ** a)

        return stack.pop()

# Example usage
expression = "1+2*(3/(4+5))*6+cos(0)+log(2, 2)"
calc = Calculate(expression)
result = calc.compute()
print(f"Result of '{expression}': {result}")
