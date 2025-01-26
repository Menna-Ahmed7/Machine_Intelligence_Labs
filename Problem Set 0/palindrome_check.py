import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #TODO: ADD YOUR CODE HERE
    if string=='' or len(string)<=2:
        return True
    elif len(string) % 2 ==0:
        #[::-1] to reverse the string
        return string[0:len(string)//2]==string[-len(string)//2:][::-1]
    else:
        return string[0:len(string)//2]==string[(-len(string)//2)+1:][::-1]
        