import sqlite3
from metaphone import doublemetaphone
from rapidfuzz import fuzz, process

threshold = 50
# Connect to SQLite database (or create one)
conn = sqlite3.connect('known_words.db')

# Create a table to store words and their Metaphone codes
conn.execute('''
    CREATE TABLE IF NOT EXISTS word_sounds (
        word TEXT NOT NULL PRIMARY KEY,
        metaphone_code TEXT NOT NULL
    )
''')
conn.commit()

# Function to insert a word with its Metaphone code into the database
def add_word_to_db(word):
    metaphone_code = doublemetaphone(word)[0]  # Get the primary Metaphone code
    conn.execute('INSERT OR IGNORE INTO word_sounds (word, metaphone_code) VALUES (?, ?)', 
                 (word, metaphone_code))
    conn.commit()


# Function to find words that sound similar using Metaphone and RapidFuzz
def find_similar_words(input_word, threshold):
    # Get the Metaphone code for the input word
    primary_code = doublemetaphone(input_word)[0]
    
    # Query all words and their Metaphone codes from the database
    cursor = conn.execute('SELECT word, metaphone_code FROM word_sounds')
    all_words = cursor.fetchall()
    
    # Prepare a list of words and their codes
    word_list = [(word, metaphone_code) for word, metaphone_code in all_words]
    
    # Find matches based on metaphone codes
    similar_metaphone_matches = [word for word, code in word_list if code == primary_code]

    # Fuzzy matching using RapidFuzz
    # Get the fuzzy matches above the threshold
    fuzzy_matches = process.extract(input_word, [word for word, _ in word_list], scorer=fuzz.ratio, limit=None)
    fuzzy_words = [match for match in fuzzy_matches if match[1] >= threshold]

    # Combine results and remove duplicates
    similar_words = fuzzy_words
    
    return similar_words

# Example usage
mywords = ['car' , 'far', 'jar' , 'add', 'glad', 'sad', 'mad', 'dad']
for word in mywords:
    add_word_to_db(word)
word_to_check = 'bad'
similar_sound_words = find_similar_words(word_to_check, threshold)
print(f'Similar sounding words for "{word_to_check}": {similar_sound_words}')

# Close the database connection
conn.close()
