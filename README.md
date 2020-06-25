# renameF
## Description:
This is a little plugin for radare2 that renames all functions that have not been renamed yet with a random sequence of two words from the 10000 most used words in the english dictionary (e.g., brown_robot, flat_banana, mighty_fox, snow_crumbles..). (swear words are not taken into account)
The transformation is deterministic, based on the function address: two people get the same name for the same function.
A letter is added at the end of the name to capture how big the function is (s for small, m for medium, l for large), digits are also added to reflect how many other functions call it, and how many other functions are called by it.

### Output:
Each function will be named as the following :
- word1_word2_a letter reflecting the function's size_ the number of distinct xref calls to the function_the number of distinct xref calls from the function


## Usage: 
invoke renameF.py with "#!pipe python3 renameF.py" inside a r2 session.

## Needed libraries:
-r2pipe
