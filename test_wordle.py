import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from Wordle import Wordle  # Import your Wordle implementation


class TestWordle(unittest.TestCase):

    def setUp(self):
        """Set up a mock word list and initialize Wordle for testing."""
        self.word_list = ["apple", "grape", "peach", "mango", "berry", "crane"]  # Mock word list
        self.wordle = Wordle(word_list=self.word_list, max_attempts=6)  # Use word_list

    def test_load_words(self):
        """Test loading words from a file."""
        wordle = Wordle(word_file="mock_file.txt")
        with patch("builtins.open", mock_open(read_data="apple\ngrape\npeach\n")):
            wordle.load_words()
        self.assertEqual(wordle.words, ["apple", "grape", "peach"])

    def test_set_secret_word(self):
        """Test setting a secret word."""
        self.wordle.set_secret_word("apple")
        self.assertEqual(self.wordle.secret_word, "apple")

    def test_set_invalid_secret_word(self):
        """Test setting an invalid secret word."""
        with self.assertRaises(ValueError):
            self.wordle.set_secret_word("wrongword")

    def test_evaluate_guess_exact_match(self):
        """Test feedback for an exact match."""
        self.wordle.set_secret_word("apple")
        feedback = self.wordle.evaluate_guess("apple")
        self.assertEqual(feedback, ["green", "green", "green", "green", "green"])

    def test_evaluate_guess_partial_match(self):
        """Test feedback for partial matches."""
        self.wordle.set_secret_word("apple")
        feedback = self.wordle.evaluate_guess("apric")
        self.assertEqual(feedback, ["green", "green", "gray", "gray", "gray"])

    def test_evaluate_guess_no_match(self):
        """Test feedback for no matches."""
        self.wordle.set_secret_word("apple")
        feedback = self.wordle.evaluate_guess("wrong")
        self.assertEqual(feedback, ["gray", "gray", "gray", "gray", "gray"])


    def test_game_wins(self):
        """Test the game where the player wins."""
        self.wordle.set_secret_word("apple")
        with patch("builtins.input", side_effect=["apple"]):
            with patch("sys.stdout", new_callable=StringIO) as output:
                self.wordle.play()
                self.assertIn("Congratulations! You guessed the word 'apple'", output.getvalue())

    def test_game_loses(self):
        """Test the game where the player loses."""
        self.wordle.set_secret_word("apple")  # Set the secret word for testing
        guesses = ["grape", "peach", "mango", "berry", "crane", "grape"]  # Exactly 6 guesses
        with patch("builtins.input", side_effect=guesses):  # Mock input with 6 guesses
            with patch("sys.stdout", new_callable=StringIO) as output:
                self.wordle.play()
                print(output.getvalue())  # Print the captured output
                # Check that the game ends with the correct "Game over" message
                self.assertIn("Game over! The secret word was 'apple'", output.getvalue())

    def test_invalid_guesses(self):
        """Test invalid guesses."""
        self.wordle.set_secret_word("apple")
        with patch("builtins.input", side_effect=["wrongword", "12345", "apple"]):
            with patch("sys.stdout", new_callable=StringIO) as output:
                self.wordle.play()
                output_text = output.getvalue()
                self.assertIn("Invalid guess. Make sure it's a valid 5-letter word.", output_text)
                self.assertIn("Congratulations! You guessed the word 'apple'", output_text)


    def test_secret_word_not_set(self):
        """Test behavior when no secret word is set."""
        wordle = Wordle(word_list=self.word_list, max_attempts=6)
        wordle.secret_word = None
        with patch("sys.stdout", new_callable=StringIO) as output:
            wordle.play()
            self.assertIn("Error: No words available to play the game.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
