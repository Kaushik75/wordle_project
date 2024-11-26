import random


class Wordle:
    def __init__(self, word_file=None, max_attempts=6, word_list=None):
        """
        Initialize the Wordle game.

        :param word_file: Path to the file containing the word list (optional).
        :param max_attempts: Maximum number of attempts allowed.
        :param word_list: List of words provided directly for testing (optional).
        """
        self.word_file = word_file
        self.max_attempts = max_attempts
        self.secret_word = None

        if word_list:
            self.words = word_list
        elif word_file:
            self.load_words()
        else:
            raise ValueError("Either word_file or word_list must be provided.")

    def load_words(self):
        """Load the list of secret words from a file."""
        try:
            with open(self.word_file, 'r') as file:
                self.words = [line.strip() for line in file if len(line.strip()) == 5]
            self.secret_word = random.choice(self.words)
        except FileNotFoundError:
            # print("Error: Word file not found.")
            self.words = []
            self.secret_word = None

    def set_secret_word(self, word):
        """Set the secret word explicitly (for testing)."""
        if word in self.words:
            self.secret_word = word
        else:
            raise ValueError(f"'{word}' is not a valid word in the word list.")

    def evaluate_guess(self, guess):
        """Evaluate the player's guess and return feedback."""
        feedback = ['gray'] * 5  # Default feedback
        secret_word_list = list(self.secret_word)  # Copy of the secret word

        # Green feedback for correct positions
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                feedback[i] = 'green'
                secret_word_list[i] = None  # Mark as used

        # Yellow feedback for correct letters in the wrong positions
        for i, letter in enumerate(guess):
            if feedback[i] == 'gray' and letter in secret_word_list:
                feedback[i] = 'yellow'
                secret_word_list[secret_word_list.index(letter)] = None  # Mark as used

        return feedback

    def play(self):
        """Main game loop."""
        if not self.words or not self.secret_word:
            print("Error: No words available to play the game.")
            return

        print("Welcome to Wordle! Guess the 5-letter word.")
        attempts = 0

        while attempts < self.max_attempts:
            guess = input(f"Attempt {attempts + 1}/{self.max_attempts}: ").strip().lower()
            # print(f"DEBUG: Guess #{attempts + 1} - {guess}")
            # Validate guess
            if len(guess) != 5 or guess not in self.words:
                print("Invalid guess. Make sure it's a valid 5-letter word.")
                continue

            # Evaluate guess
            feedback = self.evaluate_guess(guess)
            print("Feedback:", feedback)

            if guess == self.secret_word:
                print(f"Congratulations! You guessed the word '{self.secret_word}' in {attempts + 1} attempts!")
                return

            attempts += 1

        # Game over message
        print(f"Game over! The secret word was '{self.secret_word}'.")


if __name__ == "__main__":
    # Path to your word list file
    word_file = "/Users/kaushikverukonda/PycharmProjects/asari_project/trainlist"

    # Create a Wordle game instance
    wordle_game = Wordle(word_file=word_file, max_attempts=6)

    # Start the game
    wordle_game.play()

