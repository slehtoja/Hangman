import glob
import sqlite3
from datetime import datetime

from Leaderboard import Leaderboard


class Model:
    def __init__(self):
        # English car model hangman_words_en.db
        self.database_name = 'databases/hangman_words_ee.db'
        self.image_files = glob.glob('images/*.png')  # All hangman images
        # New game
        self.new_word = None  # Random word from database
        self.user_word = []  # User find letter
        self.all_user_chars = []  # Any letters entered incorrectly
        self.counter = 0  # Error counter (wrong letters)
        # Leaderboard
        self.player_name = 'UNKNOWN'
        self.leaderboard_file = 'leaderboard.txt'
        self.score_data = []  # Leaderboard file contents

    def start_new_game(self):
        self.get_random_word()  # Set new word (self.new_word)
        # print(self.new_word)  # for testing
        self.user_word = []
        self.all_user_chars = []
        self.counter = 0
        # All letters replace with _
        for x in range(len(self.new_word)):
            self.user_word.append('_')

        print(self.new_word)  # Test Autojuht
        print(self.user_word)  # Test ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']

    def get_random_word(self):
        connection = sqlite3.connect(self.database_name)   # Create connection to database
        cursor = connection.execute('SELECT * FROM words ORDER BY RANDOM() LIMIT 1')
        self.new_word = cursor.fetchone()[1]  # 0 => id, 1 => word
        connection.close()  # Close database connection

    def get_user_input(self, userinput):
        if userinput:
            user_char = userinput[:1]  # Only first letter
            if user_char.lower() in self.new_word.lower():
                self.change_user_input(user_char)  # Found letter
            else:  # Letter not found
                if user_char.upper() in self.all_user_chars:  # Check if the letter is allready in the list
                    self.counter += 1
                else:
                    self.counter += 1
                    self.all_user_chars.append(user_char.upper())

    def change_user_input(self, user_char):
        # Replace all _ with found letter
        current_word = self.chars_to_list(self.new_word)
        x = 0
        if user_char.upper() not in self.user_word:
            for c in current_word:
                if user_char.lower() == c.lower():
                    self.user_word[x] = user_char.upper()
                x += 1
        else:
            self.counter += 1

    @staticmethod
    def chars_to_list(string):
        # String to List: Test => ['T', 'e', 's', 't']
        chars = []
        chars[:0] = string
        return chars

    def get_all_user_chars(self):
        return ', '.join(self.all_user_chars)

    def set_player_name(self, name, seconds):
        line = []
        now = datetime.now().strftime('%Y-%m-%d %T')  # %H:%M:%S
        if name.strip():
            self.player_name = name.strip()

        line.append(now)  # Time
        line.append(self.player_name)  # PLayer name
        line.append(self.new_word)  # Word
        line.append(self.get_all_user_chars())  # All wrong letters
        line.append(str(seconds))  # Time in seconds example 130 s

        with open(self.leaderboard_file, 'a+', encoding='utf-8') as f:
            f.write(';'.join(line) + '\n')

    def read_leaderboard_file_contents(self):
        self.score_data = []
        empty_list = []
        all_lines = open(self.leaderboard_file, 'r', encoding='utf-8').readlines()
        for line in all_lines:
            parts = line.strip().split(';')
            empty_list.append(Leaderboard(parts[0], parts[1], parts[2], parts[3], int(parts[4])))
        self.score_data = sorted(empty_list, key=lambda x: x.time, reverse=False)

        return self.score_data
