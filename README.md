# Wordle Game Assistant

<<<<<<< HEAD
这是一个帮助解决 Wordle 类游戏的工具。支持3-10个字母的单词，并提供智能推荐功能，词库为GRE.txt文件，可优化。
=======
This is a tool to help solve Wordle-type games. It supports words with 3-10 letters and provides intelligent recommendation functionality.
>>>>>>> 90fe848 (Translate the entire codebase to English)

## Features

### Basic Functions
- Supports word games with 3-10 letters
- Automatically saves and displays the history of each game
- Allows multiple game sessions
- Supports uppercase and lowercase letter input (automatically converted to uppercase)

### Intelligent Matching
- Green letters: Letters that must match at specific positions
- Yellow letters: Letters that must be included in the word but are in wrong positions
- Gray letters: Letters that must not appear in the word
- Automatic letter priority handling:
  - Green letters have the highest priority
  - If a letter is already green, it's automatically removed from yellow and gray
  - If a letter is yellow, it's automatically removed from gray

### Smart Recommendations
- When possible words exceed 10, it recommends the best next guess
- Recommendation strategy: Selects words that provide the most new information
  - Excludes words containing known gray letters
  - Prioritizes words containing the most unknown letters
  - Under the same conditions, selects words with higher usage frequency

### Memory Function
- Automatically remembers yellow letters from previous guesses
- Automatically remembers gray letters from previous guesses
- Allows adding new letters directly with each new guess

## How to Use

1. Select word length (3-10 letters)

2. Enter known information:
   - Green letter positions: Use underscore _ for unknown letters, e.g., "S____" means S is in the first position
   - Yellow letters: Enter letters directly, e.g., "AT"
   - Gray letters: Enter letters directly, e.g., "REIOU"

3. View results:
   - Displays a list of possible words (if more than 10, only shows the first 10)
   - Shows the total number of words matching the criteria
   - If there are many possible words, provides a recommended guess

4. Choose action:
   - Continue the current game
   - End the current game and view the complete record
   - Start a new game
   - Exit the game completely

## Word Database Information
- Includes GRE vocabulary
- Includes common English words
- Supports automatic deduplication and categorization
- Includes word frequency information

## Important Notes
- Ensure correct input format
- The length of green letter positions must match the selected word length
- Avoid entering the same letter in different categories
