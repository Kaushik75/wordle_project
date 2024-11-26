from collections import defaultdict
import random
from collections import Counter
import matplotlib.pyplot as plt


class Wordle:
    def __init__(self, word_list_file, max_guesses=6):
        with open(word_list_file, 'r') as file:
            self.word_list = [line.strip() for line in file.readlines()]
        self.secret_word = random.choice(self.word_list)
        self.max_guesses = max_guesses

    def set_secret_word(self, secret_word):
        self.secret_word = secret_word

    def provide_feedback(self, guess):
        feedback = []
        secret_word_count = Counter(self.secret_word)
        for i, char in enumerate(guess):
            if char == self.secret_word[i]:
                feedback.append("green")
                secret_word_count[char] -= 1
            elif char in self.secret_word and secret_word_count[char] > 0:
                feedback.append("yellow")
                secret_word_count[char] -= 1
            else:
                feedback.append("gray")
        return feedback


class WordleSolver:
    def __init__(self, word_list_file):
        with open(word_list_file, 'r') as file:
            self.word_list = [line.strip() for line in file.readlines()]
        self.remaining_words = self.word_list.copy()
        self.letter_frequencies = self.calculate_letter_frequencies()

    def calculate_letter_frequencies(self):
        """
        Calculate the frequency of each letter in each position among the remaining words.
        """
        position_frequencies = [Counter() for _ in range(5)]
        for word in self.remaining_words:
            for i, letter in enumerate(word):
                position_frequencies[i][letter] += 1
        return position_frequencies

    def guess_word(self, feedback_history):
        if not feedback_history:
            return self.best_initial_guess()

        last_guess, feedback = feedback_history[-1]
        self.filter_words(last_guess, feedback)

        if self.remaining_words:
            self.letter_frequencies = self.calculate_letter_frequencies()
            return self.select_best_word()
        else:
            return None

    def best_initial_guess(self):
        """
        Use letter frequencies to calculate the best initial guess dynamically.
        """
        best_word = ""
        best_score = 0
        for word in self.remaining_words:
            score = sum(self.letter_frequencies[i][letter] for i, letter in enumerate(word))
            if score > best_score:
                best_word = word
                best_score = score
        return best_word

    def select_best_word(self):
        """
        Select the best word from the remaining list based on letter frequencies.
        """
        best_word = ""
        best_score = 0
        for word in self.remaining_words:
            score = sum(self.letter_frequencies[i][letter] for i, letter in enumerate(word))
            if score > best_score:
                best_word = word
                best_score = score
        return best_word

    def filter_words(self, last_guess, feedback):
        """
        Filter words based on feedback, mimicking the logic from the Medium article.
        """
        new_word_list = []
        for word in self.remaining_words:
            valid = True
            for i, (char, color) in enumerate(zip(last_guess, feedback)):
                if color == "green":
                    # Letter must be in the correct position
                    if word[i] != char:
                        valid = False
                        break
                elif color == "yellow":
                    # Letter must be in the word but not in this position
                    if char not in word or word[i] == char:
                        valid = False
                        break
                elif color == "gray":
                    # Letter must not be in the word at all, unless it's marked as green/yellow elsewhere
                    if char in word and char not in [g[0] for g in zip(last_guess, feedback) if g[1] in ("green", "yellow")]:
                        valid = False
                        break
            if valid:
                new_word_list.append(word)
        self.remaining_words = new_word_list


def run_simulations(word_list_file, num_simulations=100):
    attempts_per_word = []

    with open(word_list_file, 'r') as file:
        word_list = [line.strip() for line in file.readlines()]

    for _ in range(num_simulations):
        secret_word = random.choice(word_list)
        wordle = Wordle(word_list_file=word_list_file)
        wordle.set_secret_word(secret_word)
        solver = WordleSolver(word_list_file=word_list_file)

        feedback_history = []
        for attempt in range(wordle.max_guesses):
            guess = solver.guess_word(feedback_history)
            if not guess:
                attempts_per_word.append(wordle.max_guesses + 1)  # Failed to guess within max attempts
                break

            feedback = wordle.provide_feedback(guess)
            feedback_history.append((guess, feedback))

            if all(color == "green" for color in feedback):
                attempts_per_word.append(attempt + 1)
                break
        else:
            attempts_per_word.append(wordle.max_guesses + 1)  # Solver failed to find the secret word

    return attempts_per_word


def plot_histogram(attempts_per_word):
    plt.figure(figsize=(10, 6))
    plt.hist(attempts_per_word, bins=range(1, max(attempts_per_word) + 2), align='left', rwidth=0.8)
    plt.title('Distribution of Attempts Per Word')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Frequency')
    plt.xticks(range(1, max(attempts_per_word) + 2))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


# Run Simulations and Plot Histogram
if __name__ == "__main__":
    word_list_file = "trainlist"
    num_simulations = 1000  # Number of words to simulate

    attempts_per_word = run_simulations(word_list_file, num_simulations)
    plot_histogram(attempts_per_word)
    print("Average Attempts: ", sum(attempts_per_word) / len(attempts_per_word))
