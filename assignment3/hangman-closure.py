def make_hangman(secret_word):
  guesses = []
  secret_word = secret_word.lower()

  def hangman_closure(letter):
    guesses.append(letter.lower())

    display_word = "".join([char if char in guesses else "_" for char in secret_word])
    print(f"Word: {display_word}")
    if all(char in guesses for char in secret_word):
       return True
    return False
  
  return hangman_closure()

if __name__ == "__main__":
  print("--- Welcome to Closure Hangman ---")
  target = input("Enter the secret word to begin: ").strip()
  play_round = make_hangman(target)
  game_won = False

  while not game_won:
    guess = input("Guess a letter: ").strip()

    if len(guess) != 1:
      print("Please enter only one letter at a time.")
      continue

    game_won = play_round(guess)

  print("Congratulations! You guessed the word!")