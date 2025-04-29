import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# tells system to look at root directory for moduels
from minbpe import BasicTokenizer




def getTokenizer():


    """
    Checks for an existing tokenizer model and loads it if available. If not,
    it processes a text file to train a new tokenizer, saves the trained tokenizer, 
    and returns the tokenizer object.

    The function performs the following steps:
    1. Checks if an existing tokenizer model file exists (tokenizers/tokenizer.model).
    2. If the model exists, it loads the model and returns the tokenizer.
    3. If the model does not exist:
        - Reads a text file (textFiles/output.txt) to extract the text data.
        - Trains a new tokenizer with the text data using a vocabulary size of 1024.
        - Defines special tokens (startoftext, separator, endoftext, unk) and assigns them unique IDs.
        - Saves the newly trained tokenizer to the specified file path (tokenizers/tokenizer).
    4. Returns the tokenizer object.

    Returns:
        BasicTokenizer: The tokenizer object, either loaded from file or newly trained.

    Raises:
        Exception: If an error occurs while training or saving the tokenizer.
    """



    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    existingTokenizerFilePath = os.path.join(root_dir, "tokenizers","tokenizer.model")
    tokenizerFilePath= os.path.join(root_dir, "tokenizers","tokenizer")
    
    tokenizer = BasicTokenizer()

    if os.path.exists(existingTokenizerFilePath):
       tokenizer.load(model_file=existingTokenizerFilePath)
       return tokenizer


    try:

        textpath = "../textFiles/output.txt"

        if not os.path.exists(textpath):
            print(f"File not found: {textpath}")
            return 
        


        with open(textpath, 'r') as f:
            textSequence = f.read()


        tokenizer.train(textSequence ,vocab_size = 1024)
        # can update vocab_size for token output



        tokenizersDirPath = os.path.join(root_dir, "tokenizers")
        os.makedirs(tokenizersDirPath, exist_ok=True)
        
        # Above creates our textFiles directory in the root directory 


        vocab = tokenizer.vocab

        max_vocab_id = list(vocab.keys())[-1]

        tokenizer.special_tokens = {
            "<startoftext>": max_vocab_id + 1,
            "<separator>": max_vocab_id + 2,
            "<endoftext>": max_vocab_id + 3,
            "<unk>": max_vocab_id + 4
        }


        tokenizer.save(file_prefix=tokenizerFilePath)

        print("Succesfully created tokenizer directory files! 😊 ")


        # encoded_tokens = tokenizer.encode(textSequence)

    
        # print(f"Number of tokens generated: {len(encoded_tokens)}")

        # unComment above two lines of code to check how many tokens were generated
  

    except Exception as e:
        print(f"Error saving tokenizer: {e}")

   
    
    return tokenizer





