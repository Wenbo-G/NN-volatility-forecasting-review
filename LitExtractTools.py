import os
import pandas as pd
import numpy as np
import re

def loadLitExtract(x):
    """Loads the .csv file which has the extracted data from a piece of literature
    
        Parameters:
            x (int or string): the reference to the .csv file
            
        Returns:
            data (DataFrame): the pd.DataFrame which holds the information from the .csv file
    """
    path = '3. Data extraction/' + str(x) + '.csv' if isinstance(x,int) else x
    data = pd.read_csv(path,index_col=0,names=['Field','Content']).fillna('')
    data.loc['path'] = path
    return data
    
def checkContent(x):
    """Checks one file for missing values.
    
        Parameters:
            x (int or string or pd.DataFrame): the reference to the .csv file
            
        Returns:
            passed (bool): True if passed, False if failed
    """
    data = x if isinstance(x,pd.DataFrame) else loadLitExtract(x)
    cols = data.index
    passed = True
    for col in cols:
        content = data.loc[col]['Content']

        if content == '' and not (col == 'Interesting notes' or col == 'Insights/my takeaway' or col == 'IN'):
            print(x.loc['path']['Content'],col,content) if isinstance(x,pd.DataFrame) else print(x,col,content)
            passed = False
    
    return passed
            

def loadAllExtracted():
    """Loads all files in the Data extraction folder.
    
        Parameters:
            none
            
        Returns:
            data (list): list of all DataFrames from loadLitExtract
    """
    a = os.scandir('3. Data extraction/')
    data = []
    for entry in a:
        data.append(loadLitExtract(entry.path))
    
    return data
            
def checkAllContent():
    """Checks all files in the Data extraction folder for missing values.
    
        Parameters:
            none
            
        Returns:
            passed (bool): True if passed, False if failed
    """
    data = loadAllExtracted()
    passeds = True
    for paper in data: 
        passed = checkContent(paper)
        passeds = passed and passeds
    print("Passed, there are no missing values where there shouldn't be") if passeds else print("Failed, there are missing values where there shouldn't be")
    return passeds


def retrieveAll(papers,field):
    """Retrieves the content of a field from all papers.
    
        Parameters:
            papers (list of DataFrame): all papers
            field (string): what field to retrieve
            
        Returns:
            items (list): content from field of all papers
    """
    items = []
    for paper in papers:
        item = paper.loc[field]['Content']
        items.append(item)
    return items
    
    
def inCounter(term,array):
    """Counts number of appearances of term in the elements of array (case insensitive), can not count multiple times for one element of array. 
    
        Parameters:
            term (string): The term to count for
            array (array-like): The array to search over
            
        Returns:
            counter (int): Number of appearances
    """
    condition = lambda x,y: x.lower() in y.lower()
    return counter(term,array,condition,remove=False)

def equalCounter(term,array):
    """Counts number of times term equals the element in the array (case insensitive).
    
        Parameters:
            term (string): The term to count for
            array (array-like): The array to search over
            
        Returns:
            counter (int): Number of appearances
    """
    condition = lambda x,y: x.lower() == y.lower()
    return counter(term,array,condition,remove=False)

def inCounter_withRemoval(term,array):
    """Counts number of appearances of term in the elements of array (case insensitive), can not count multiple times for one element of array. 
    Also removes all elements in array with that term.
    
        Parameters:
            term (string): The term to count for
            array (array-like): The array to search over
            
        Returns:
            counter (int): Number of appearances
    """
    condition = lambda x,y: x.lower() in y.lower()
    return counter(term,array,condition,remove=True)

def equalCounter_withRemoval(term,array):
    """Counts number of times term equals the element in the array (case insensitive). 
    Also removes all elements in array equal to that term.
    
        Parameters:
            term (string): The term to count for
            array (array-like): The array to search over
            
        Returns:
            counter (int): Number of appearances
    """
    condition = lambda x,y: x.lower() == y.lower()
    return counter(term,array,condition,remove=True)

    
def counter(term,array,condition,remove):
    """Counts number of times condition is met for term in array.
    
        Parameters:
            term (string): The term to count for
            array (array-like): The array to search over
            condition (function): The condition to count if met
            remove (bool): to remove elements that match the condition or not
            
        Returns:
            counter (int): Number of appearances
    """
    if remove:
        counter = len(array)
        array[:] = [x for x in array if not condition(term,x)]
        counter -= len(array)
        return counter
    else:
        return sum(1 if condition(term,z) else 0 for z in array)
    

def removeBrackets(x):
    """Removes all brackets and content inside brackets
    
        Parameters:
            x (string): String to have brackets and contents removed from
            
        Returns:
            (string): The string without brackets and its contents
    """
    return re.sub("[\(\[].*?[\)\]]", "", x)


def find_replace(x,y,z):
    """Replaces all appearances of string x for string y in string z
    
        Parameters:
            x (string): String to be replaced
            y (string): String to replace with
            z (string): String in which x should be replaced with y
            
        Returns:
            (string): The replaced string
    """
    return z.replace(x,y)

def replace_na(y,z):
    """Replaces all appearances of 'na' for string y in string z
    
        Parameters:
            y (string): String to replace with
            z (string): String in which x should be replaced with y
            
        Returns:
            (string): The replaced string
    """
    return find_replace('na',y,z)

def fixAmpersand(z):
    """Replaces all appearances of '&' for '\\&' in string z, for the overleaf
    
        Parameters:
            z (string): String in which x should be replaced with y
            
        Returns:
            (string): The replaced string
    """
    return find_replace('&','\\&',z)

