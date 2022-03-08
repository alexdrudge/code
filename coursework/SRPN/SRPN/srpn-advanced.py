#This is your SRPN file. Make your changes here.
import re
import math

class Stack:
    '''stack class to hold all integers'''
    def __init__(self):
        self.items = []
    
    def push(self, item):
        # maximum number of elements in the stack is 23
        if len(self.items) > 22:
            print("Stack overflow.")
        else:
            # maximum values of integers in the stack
            if item > 2147483647:
                item = 2147483647
            elif item < -2147483648:
                item = -2147483648
            self.items.append(item)

    def pop(self):
        # underflow if it tries to remove an item from an empty list
        if len(self.items) == 0:
            print("Stack underflow.")
            return None
        else:
            return self.items.pop()
    
    def peek(self):
        # empty if it tries to look at an empty list
        if len(self.items) == 0:
            print("Stack empty.")
            return None
        else:
            return self.items[-1]
    
    def dump(self):
        # if the stack is empty it will return the max lowest number
        if len(self.items) == 0:
            print(-2147483648)
        else:
            for i in self.items:
                print(i)
    
    def full(self):
        # if the list is full then return True
        if len(self.items) > 22:
            return True
        else:
            return False

# initiate global stack as to not change the main function
# better practise would be to change the main function
stack = Stack()
RANDOM = [1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492, 596516649, 1189641421, 1025202362, 1350490027, 783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426, 304089172, 1303455736, 35005211, 521595368]
count = 0

def process_command(command):
    ''' process the command that has been inputted
    makes use of re library to categorise the commands
    either returns the result of = operator or None'''
    # remove comments from the text
    ## "# text#" breaks the program as it waits for a second comment ending
    command = re.sub("#[ ][^#]+[ ]#", " ", command)
    # split the text at any space
    ###commands = re.split("([\-]*[0-9]+)|[.]?", command)
    commands = re.split(" ", command)
    for command in commands:
        if command != None:
            # output the number on the top of the stack
            if re.fullmatch("[=]", command):
                return stack.peek()
            # any of the basic operators
            elif re.fullmatch("[\+]|[\-]|[\*]|[\/]|[\%]|[\^]", command):
                process_calculation(command)
            # dump every item in the stack
            elif re.fullmatch("[d]", command):
                stack.dump()
            # add a 'random' number to the stack
            elif re.fullmatch("[r]", command):
                global count
                if not stack.full():
                    stack.push(RANDOM[count])
                    count = (count + 1) % 22
                else:
                    stack.push(RANDOM[count])
            # deals with negative integers and repeated negatives
            elif re.fullmatch("[\-]+[0-9]+", command):
                split = re.findall("[\-]+|[0-9]+", command)
                # even numbers of negatives are processed as minuses
                if (len(split[0]) % 2) == 0:
                    length = len(split[0])
                    # if the number starts with 0 try to turn it into octal
                    if split[1][0] == "0":
                        try:
                            split[1] = int(split[1], 8)
                        except:
                            pass
                    else:
                        split[1] = int(split[1])
                else:
                    length = len(split[0]) - 1
                    # if the number starts with 0 try to turn it into octal
                    if split[1][0] == "0":
                        try:
                            split[1] = int(split[1], 8) * -1
                        except:
                            pass
                    else:
                        split[1] = int(split[1]) * -1
                for i in range(length):
                    process_calculation("-")
                stack.push(split[1])
            # any positive or negative number
            elif re.fullmatch("[0-9]+", command):
                # if the number starts with 0 try to turn it into octal
                if command[0] == "0":
                    try:
                        stack.push(int(command, 8))
                    except:
                        pass
                else:
                    stack.push(int(command))
            # any remaining non white space will be read as a 0
            elif re.fullmatch("\S", command):
                print("Unrecognised operator or operand \"%s\"." % command)
            # random advanced bodges
            ## does not handle any form of octal numbers
            elif re.fullmatch("\S+", command):
                try:
                    # handles basic one line maths that could have an equals at the end
                    if command[-1] == "=":
                        command2 = re.sub("#", "~", command)
                        result = eval(command2[:len(command) - 1])
                        commands2 = re.split("([\-]*[0-9]+)|[.]?", command)
                        num = None
                        for i in commands2:
                            if i != None:
                                if re.fullmatch("[\-]?[0-9]+", i):
                                    num = i
                                if i == "=" and num != None:
                                    print(num)
                    else:
                        command2 = re.sub("#", "~", command)
                        result = eval(command2)
                    stack.push(int(result))
                except:
                    # handles anything that is only one line of text e.g. a broken comment
                    commands2 = re.split("([\-]*[0-9]+)|[.]?", command)
                    num = None
                    for i in commands2:
                        if i != None:
                            if re.fullmatch("[\-]?[0-9]+", i):
                                num = i
                            if i == "=" and num != None:
                                print(num)
                            process_command(i)
    return None

def process_calculation(command):
    '''process all 6 operators
    two values are taken from the stack and one is returned to the stack
    if there are not two values on the stack return any taken
    prints any errors that occur (divide by 0 and negative power)'''
    result = None
    num2, num1 = None, None
    # obtain the two values to be operated on
    num2 = stack.pop()
    if num2 != None:
        num1 = stack.pop()
        if num1 == None:
            stack.push(num2)
    # basic calculations
    if num1 != None and num2 != None:
        if command == "+":
            result = num1 + num2
        elif command == "-":
            result = num1 - num2
        elif command == "*":
            result = num1 * num2
        elif command == "/":
            # prevent division by 0 and also use integer division
            if num2 == 0:
                print("Divide by 0.")
                stack.push(num1)
                stack.push(num2)
            else:
                result = num1 // num2
                # always truncates the number and never round up the negative
                if num1 < 0 and num2 > 0 and num1 % num2 != 0:
                    result += 1
                if num2 < 0 and num1 > 0 and num1 % num2 != 0:
                    result += 1
        elif command == "%":
            # two divide by 0 errors (only one intended)
            if num1 == 0 or num2 == 0:
                print("Divide by 0.")
                stack.push(num1)
                stack.push(num2)
            else:
                result = num1 % num2
                # if a number is less than 0 it needs to return a negative number
                if num1 < 0 and num2 > 0 and result != 0:
                    result -= num2
                # if second number is less than 0 it needs to return a positive
                if num2 < 0 and num1 > 0 and result != 0:
                    result -= num2
        elif command == "^":
            # avoid going to the power of a negative number
            if num2 < 0:
                print("Negative power.")
                stack.push(num1)
                stack.push(num2)
            else:
                try:
                    result = math.pow(num1, num2)
                except:
                    result = 2147483647 + 1 # saturated answer
    # if a result was generated add it onto the stack
    if result != None:
        stack.push(int(result))


#This is the entry point for the program.
#Do not edit the below
if __name__ == "__main__":
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
            if pc != None:
                print(str(pc))
        except:
            exit()
