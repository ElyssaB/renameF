# renameF
This is an implementation of a little plugin for radare2 that renames all functions that have not been renamed yet with a random sequence of two words from the most 10000 most used words in the english dictionary (e.g., brown_robot, flat_banana, mighty_fox, snow_crumbles..).
The transformation is deterministic, based on the function address: two people get the same name for the same function.
A letter is added at the end of the name to capture how big the function is (s for small, m for medium, l for large), digits are also added to reflect how many other functions call each particular function , and how many other functions are called by it.

## Usage: 
invoke renameF.py with "#!pipe python3 renameF.py" inside a r2 session.

## Needed librariries:
-r2pipe
