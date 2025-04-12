import random
from word_database import get_filtered_words, get_word_frequency

class WordleSolver:
    def __init__(self, word_length):
        self.word_pool = self.load_words()
        self.word_length = word_length
    
    def load_words(self):
        return get_filtered_words()
    
    def find_words(self, green="", yellow="", grey=""):
        print(f"\nDebug information:")
        print(f"Input green pattern: {green}, Length: {len(green)}")
        print(f"Yellow letters: {yellow}")
        print(f"Gray letters: {grey}")
        
        # Ensure green pattern has correct length
        if len(green) != self.word_length:
            green = green.ljust(self.word_length, '_')
        
        # Convert green to known_positions
        known_positions = {}
        green_letters = set()  # Store all green letters
        for i, letter in enumerate(green):
            if letter != '_':
                known_positions[i+1] = letter
                green_letters.add(letter)
        print(f"Known positions: {known_positions}")
        
        # Process yellow letters (exclude those already in green)
        yellow_letters = set(yellow) - green_letters
        print(f"Letters that must be included (excluding green): {yellow_letters}")
        
        # Process grey letters (exclude those already in green and yellow)
        grey_letters = set(grey) - green_letters - yellow_letters
        print(f"Excluded letters (excluding green and yellow): {grey_letters}")
        
        # Check each word
        possible_words = []
        for word in self.word_pool:
            if len(word) != self.word_length:
                continue
            
            # Check green letter positions
            match = True
            for pos, letter in known_positions.items():
                if word[pos-1] != letter:
                    match = False
                    break
            if not match:
                continue
            
            # Check required yellow letters
            word_letters = set(word)
            if not yellow_letters.issubset(word_letters):
                continue
            
            # Check excluded gray letters (already excluding green and yellow)
            if any(letter in grey_letters for letter in word):
                continue
            
            possible_words.append(word)
        
        # Sort by frequency
        possible_words.sort(key=lambda w: get_word_frequency(w), reverse=True)
        
        return possible_words
    
    def recommend_word(self, possible_words, known_letters, green="", yellow="", grey=""):
        """
        Recommend the next word to guess
        
        Parameters:
            possible_words: Current list of possible words
            known_letters: Known letters set (green + yellow + gray)
            green: Green letter positions
            yellow: Yellow letters
            grey: Gray letters
        """
        # If possible words are less than or equal to 10, no recommendation
        if len(possible_words) <= 10:
            return None
        
        # Get all words of the same length (not just possible words)
        all_words_same_length = [w for w in self.word_pool if len(w) == self.word_length]
        
        # Calculate the information value of each word
        word_scores = {}
        for word in all_words_same_length:
            # Skip words containing gray letters
            if any(letter in word for letter in grey):
                continue
            
            # Calculate how many new letters this word contains (not in known_letters)
            word_letters = set(word)
            new_letters = word_letters - known_letters
            
            # Calculate score: new letters count * 100 + word frequency
            score = len(new_letters) * 100 + get_word_frequency(word)
            word_scores[word] = score
        
        if not word_scores:
            return None
        
        # Return the highest scoring word
        return max(word_scores.items(), key=lambda x: x[1])[0]

def main():
    while True:  # Outer loop handles multiple games
        # Let user select word length
        while True:
            try:
                print("\nAvailable word lengths: 3-10")
                length = int(input("Please select word length: "))
                if 3 <= length <= 10:
                    break
                print("Only words with 3-10 letters are supported. Please select again.")
            except ValueError:
                print("Please enter a number between 3 and 10")
        
        solver = WordleSolver(length)
        history = []  # Store game history
        previous_grey = ""  # Store previous gray letters
        previous_yellow = ""  # Store previous yellow letters
        
        while True:  # Inner loop handles a single game
            print("\n" + "="*50)  # Separator
            
            # Display history
            if history:
                print("\nHistory of previous guesses:")
                for i, record in enumerate(history, 1):
                    print(f"\nGuess #{i}:")
                    print(f"Green letter positions: {record['green']}")
                    print(f"Yellow letters: {record['yellow']}")
                    print(f"Gray letters: {record['grey']}")
                    print(f"Possible words: {record['words']}")
            
            print("\nEnter new guess:")
            print(f"Green letter format: Use _ for unknown letters, e.g. {'S' + '_'*(length-1)}")
            green = input("Green letter positions: ").upper().strip()
            
            # Display and use previous yellow letters
            if previous_yellow:
                print(f"\nYellow letters ({previous_yellow})")  # First show existing yellow letters
                print("Enter new yellow letters (press Enter for none):")
                new_yellow = input().upper().strip()
                yellow = previous_yellow + new_yellow  # Combine old and new yellow letters
                print(f"All current yellow letters: {yellow}")  # Show combined result
            else:
                print("\nYellow letter format: Enter letters directly, e.g. AT")
                yellow = input("Yellow letters: ").upper().strip()
            
            # Display and use previous gray letters
            if previous_grey:
                print(f"\nGray letters ({previous_grey})")  # First show existing gray letters
                print("Enter new gray letters (press Enter for none):")
                new_grey = input().upper().strip()
                grey = previous_grey + new_grey  # Combine old and new gray letters
                print(f"All current gray letters: {grey}")  # Show combined result
            else:
                print("\nGray letter format: Enter letters directly, e.g. REIOU")
                grey = input("Gray letters: ").upper().strip()
            
            # Update previous_grey and previous_yellow for next guess
            previous_grey = grey
            previous_yellow = yellow
            
            words = solver.find_words(
                green=green,
                yellow=yellow,
                grey=grey
            )
            
            # Calculate all known letters
            known_letters = set(green.replace('_', '')) | set(yellow) | set(grey)
            
            # Get recommended word
            recommended = solver.recommend_word(words, known_letters, green, yellow, grey)
            
            # Save this record
            history.append({
                'green': green,
                'yellow': yellow,
                'grey': grey,
                'words': words[:10] if len(words) > 10 else words
            })
            
            print("\nPossible words for this guess:")
            print(words[:10] if len(words) > 10 else words)
            print(f"Found {len(words)} possible words")
            if recommended:
                print(f"\nRecommended guess word: {recommended}")
                print("(This word excludes known letters to help eliminate more possibilities)")
            
            # Ask whether to continue this game
            again = input("\nContinue this game? (y/n): ").lower().strip()
            if again != 'y':
                break
        
        # Display complete history for this game
        print("\n" + "="*50)
        print("\nGame over! Complete guess history:")
        for i, record in enumerate(history, 1):
            print(f"\nGuess #{i}:")
            print(f"Green letter positions: {record['green']}")
            print(f"Yellow letters: {record['yellow']}")
            print(f"Gray letters: {record['grey']}")
            print(f"Possible words: {record['words']}")
        
        # Ask whether to start a new game
        new_game = input("\nStart a new game? (y/n): ").lower().strip()
        if new_game != 'y':
            print("\nGame ended. Thanks for playing!")
            break

if __name__ == "__main__":
    main() 