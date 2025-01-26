from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #TODO: ADD YOUR CODE HERE
    words:List[str]=ciphered.split(' ')
    #List lookups are O(n), but set lookups are O(1) so we will convert list of the dictionary to a set
    dictionary_set = set(dictionary)
    minNumberofDiff=len(words)
    numberofShifts:int=0
    decipheredText:str=""

    for i in range(0,25,1):
        newstr=""
        numberofDiff=0
        #deciphering each char
        for char in ciphered:
            if char!=' ':
                char_ascii_deciphered=(ord(char)-97-i)
                if char_ascii_deciphered<0:
                    newstr+=chr((char_ascii_deciphered+26)+97)
                else:
                    newstr+=chr((char_ascii_deciphered)+97)
            else: newstr+=' '
        #checking for each word whether in the dictionary or not
        words: List[str] = newstr.split(' ')
        for word in words:
            # print(word)
            if word not in dictionary_set:
                numberofDiff += 1
            if numberofDiff>minNumberofDiff:
                break
        # getting the deciphered with minimum number of words out of the dictionary
        if numberofDiff<minNumberofDiff:
            minNumberofDiff=numberofDiff
            numberofShifts=i
            decipheredText=newstr
    return (decipheredText,numberofShifts,minNumberofDiff)

