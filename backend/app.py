from flask import Flask, request, jsonify
import sqlite3
from metaphone import doublemetaphone
from rapidfuzz import fuzz

app = Flask(__name__)

# Connect to SQLite database (or create one)
conn = sqlite3.connect('known_words.db',  check_same_thread=False)

# Create a table to store words and their Metaphone codes
conn.execute('''
    CREATE TABLE IF NOT EXISTS word_sounds (
        word TEXT NOT NULL PRIMARY KEY,
        metaphone_code TEXT NOT NULL
    )
''')
conn.commit()

# Route to add a new word to the database
@app.route('/api/add-word', methods=['POST'])

def add_word():
    data = request.get_json()
    word = data.get('word', '')

    if word:
        metaphone_code = doublemetaphone(word)[0]  # Get the primary Metaphone code
        try:
            conn.execute('INSERT OR IGNORE INTO word_sounds (word, metaphone_code) VALUES (?, ?)', 
                         (word, metaphone_code))
            conn.commit()
            return jsonify({"message": f'Word "{word}" added successfully!'}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No word provided"}), 400

# Route to find similar words based on Metaphone codes and fuzzy matching
@app.route('/api/similar-words', methods=['POST'])
def find_similar_words():
    data = request.get_json()
    input_word = data.get('word', '')

    if input_word:
        primary_code = doublemetaphone(input_word)[0]
        print(f"Primary metaphone code for '{input_word}': {primary_code}")  # Debugging line

        cursor = conn.execute('SELECT word, metaphone_code FROM word_sounds')
        all_words = cursor.fetchall()

        word_list = [(word, metaphone_code) for word, metaphone_code in all_words]
        print(f"Word list: {word_list}")  # Debugging line

        # Find matches based on Metaphone codes
        similar_metaphone_matches = [word for word, code in word_list if code == primary_code]

        # Add fuzzy matching using RapidFuzz (optional enhancement)
        fuzzy_matches = [
            word for word, code in word_list 
            if fuzz.ratio(input_word, word) >= 50  # Similarity threshold, adjust as needed
        ]

        # Combine results and remove duplicates
        combined_results = list(set(similar_metaphone_matches + fuzzy_matches))
        print(f"Similar words: {combined_results}")  # Debugging line

        return jsonify({"similar_words": combined_results}), 200
    else:
        return jsonify({"error": "No word provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
