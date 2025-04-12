def load_words_from_files():
    """Load words from GRE file"""
    words = set()  # Use set for deduplication
    
    # Load from GRE file
    try:
        with open('GRE.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
            
            # Process each line
            for line_num, line in enumerate(lines, 1):
                try:
                    # Skip empty lines
                    if not line.strip():
                        continue
                    
                    # Clean the line, remove Chinese and special characters
                    parts = []
                    current_word = ""
                    for char in line:
                        if char.isalpha():
                            current_word += char
                        else:
                            if current_word:
                                parts.append(current_word)
                                current_word = ""
                    if current_word:
                        parts.append(current_word)
                    
                    # Process each possible word
                    for word in parts:
                        word = word.upper()
                        # Only keep pure English words with length >= 3
                        if word.isalpha() and len(word) >= 3 and not any(ord(c) > 127 for c in word):
                            words.add(word)
                            
                except Exception as e:
                    continue
    
    except FileNotFoundError:
        print("Error: File GRE.txt not found")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []
    
    # Add number words (3-10 letters)
    number_words = {
        # 3 letters
        "ONE", "TWO", "SIX", "TEN",
        # 4 letters
        "ZERO", "FOUR", "FIVE", "NINE",
        # 5 letters
        "THREE", "SEVEN", "EIGHT",
        # 6 letters
        "ELEVEN", "TWELVE",
        # 7 letters
        "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTY", "HUNDRED",
        # 8 letters
        "EIGHTEEN", "NINETEEN", "THOUSAND",
        # 9 letters
        "SEVENTEEN", "FORTY", "FIFTY", "SIXTY", "EIGHTY", "NINETY",
        # 10 letters
        "TWENTY", "THIRTY", "MILLION", "BILLION"
    }
    words.update(number_words)
    
    # Add additional words
    additional_words = {
        "HARNESS",
        "OVERTIME",
    }
    words.update(additional_words)
    
    return sorted(list(words))

# Load all words
ALL_WORDS = load_words_from_files()

# Categorize words by length
WORD_DATABASE = {
    "THREE_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 3],
    "FOUR_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 4],
    "FIVE_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 5],
    "SIX_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 6],
    "SEVEN_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 7],
    "EIGHT_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 8],
    "NINE_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 9],
    "TEN_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 10]
}

# Word frequency information (can be adjusted as needed)
WORD_FREQUENCIES = {
    # Common words with frequency 90-100
    "ABOUT": 95, "AFTER": 95, "AGAIN": 95, "ALONE": 95, "ALONG": 95,
    "ALREADY": 94, "ALWAYS": 94, "AMOUNT": 94,
    "ANIMAL": 93, "ANSWER": 93, "ANYONE": 93,
    "APPEAR": 92, "AROUND": 92, "ARRIVE": 92,
    
    # Other words default to frequency 1
}

def get_word_frequency(word):
    """Get the usage frequency of a word"""
    return WORD_FREQUENCIES.get(word.upper(), 1)

def get_filtered_words():
    """Get all words"""
    return ALL_WORDS