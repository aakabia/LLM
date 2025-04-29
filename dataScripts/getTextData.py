import pandas as pd
import re
import os
import gc


pd.set_option('display.max_colwidth', None)
# Above sets our dataframes with so we can see full values in columns/rows

# Login using e.g. `huggingface-cli login` to access this dataset
df = pd.read_parquet("hf://datasets/FradSer/OpenSubtitles-en-zh-cn-20m/OpenSubtitles-en-zh-cn-20m-v1.parquet")

# load our data in from hugging face 
# Since the dataset is large (~5GB), we explicitly delete the DataFrame and run garbage collection at the end of the script to free up memory.


def cleanString(value:str): 

    """
    Cleans a string by removing any characters that are not letters, 
    digits, spaces, or periods. Collapses multiple spaces into one,
    and ensures the string ends with a single period.

    Args:
        Value (str): A string to clean.
        

    Returns:
        str: A cleaned string including proper chars, spacing and punctuation.
    """   

    value = re.sub(r"[^a-zA-Z0-9.' ]", "", value)

  
    value = re.sub(r'\s+', ' ', value).strip()
    
    if value and not value.endswith(('.','?','!')):
        value += '.'
    
    return value



def getWordsOfLength(series:list[str], wordsAmount:int):

    """
    Creates a list of strings from a series, ensuring the total number of words
    does not exceed the specified limit.

    Args:
        Series list[str]: A series of strings.
        wordsAmount (int): The Amount of words to output.
        

    Returns:
       List[str]: A list of strings where the total number of words equals what the user asked for.
    """ 







    maxWords = wordsAmount
    totalWords = 0 
    words = []

    for line in series:
        splitString = line.split(" ")
        lengthOfSplitString = len(splitString)

        if(lengthOfSplitString + totalWords <= maxWords ):
            separator = " "
            joinedString = separator.join(splitString)
            words.append(joinedString)
            totalWords = totalWords + lengthOfSplitString
        else:
            break

    
    return words




def cleanAndWriteTextData(series:list[str], wordsAmount:int):

    """
    Processes a series of strings with the following steps:
    1. Cleans each string by:
        - Removing any characters that are not letters, digits, spaces, or periods.
        - Collapsing multiple consecutive spaces into a single space.
        - Ensuring the string ends with a single period.
    2. Filters out strings that:
        - Seem to be concatenated words (e.g., missing appropriate spaces).
        - Begin with digits or symbols.
        - Contain ellipses ('...').
    3. Accumulates words from the cleaned strings until a specified total word count is reached.
    4. Writes the resulting list of words to a text file.
  
    Args:
        Series list[str]: A series of strings.
        wordsAmount (int): The Amount of words to output.
       
        

    Returns:
        None: Writes the cleaned content to a text file.

    """  

    nums = ("0","1","2","3","4","5","6","7","8","9","'")
    series = series.apply(cleanString)
    cleanedSeries = series[~series.str.contains(r'\.{3,}|…', na=False) & ~series.str.startswith(nums) & ~series.str.contains(r'\b[a-z]{10,}\b|[a-z]+[A-Z][a-z]+') & (series != "")]
    # rgular exprssions above help remove elippses, strings that start with a num and concated strings. 
    # note* Concated strings interesting
    
    listOfWords = getWordsOfLength(cleanedSeries, wordsAmount)


    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    textDirPath = os.path.join(root_dir, "textFiles")
    os.makedirs(textDirPath, exist_ok=True)
    
   # Above creates our textFiles directory in the root directory 


    textPath = os.path.join(textDirPath, "output.txt")

    with open(textPath, 'w') as f:
        for line in listOfWords:
            f.write(f"{line}")
    
    print("Succesfully created text directory and file! 😊 ")




english_rows = df["source"] 
# Create series from dataFrame 


cleanAndWriteTextData(english_rows,350000)
# clean and write the data


del df
gc.collect()


