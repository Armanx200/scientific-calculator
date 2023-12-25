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
    def __init__(self, equation:str):
        pattern = re.compile(r'cos\(([-+]?(?:\d*\.*\d+))\)')
        matches = list(pattern.finditer(equation))
        pattern = re.compile(r'sin\(([-+]?(?:\d*\.*\d+))\)')
        matches = list(pattern.finditer(equation)) + matches
        pattern = re.compile(r'log\(([-+]?(?:\d*\,*.*\d+))\)')
        matches = list(pattern.finditer(equation)) + matches
        if matches:
            matches = [match.group(0) for match in matches]
            for i in matches:
                equation = equation.replace(i, str(eval("math."+i)))
        self.equation = equation
        
    def InfixToPostfix(self):
        Operators = set(['+', '-', '*', '/', '(', ')', '^'])  
        Priority = {'+':1, '-':1, '*':2, '/':2, '^':3}
        stack = Stack()
        output = [] 
        put = ''

        for character in self.equation:
            if character not in Operators:
                put += character

            elif character=='(':
                stack.push('(')

            elif character==')':
                if put:
                    output.append(put)
                    put=''
                while not(stack.isEmpty()) and stack.peek()!='(':
                    output+=stack.pop()
                stack.pop()

            else:
                if put:
                    output.append(put)
                    put=''
                while not(stack.isEmpty()) and stack.peek()!='(' and Priority[character]<=Priority[stack.peek()]:
                    output+=stack.pop()
                stack.push(character)
        if put:
            output.append(put)
        while not(stack.isEmpty()):
            output+=stack.pop()
        
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
                stack.push(eval(f"{b}{character}{a}"))
        return(stack.pop())

            
            
    

                


# calculate(str(input("")))
Calculate("3*cos(0)+cos(1)+sin(0)+log(2, 2)")
a = Calculate("1+2*(3/(4+5))*6+cos(0)")
print(a.compute())