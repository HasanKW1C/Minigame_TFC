import random
words = ["python", "computer", "programming", "website", "technology", "database"]

chosen_word = random.choice(words)
word_display = ["_" for _ in chosen_word]
attempts = 10

print("Welcome to hangman.")

while attempts > 0 and "_" in word_display:
    print("\n" +  " ".join(word_display))
    guess = input("Guess a letter: ").lower()
    if guess in chosen_word:
        for index, letter in enumerate(chosen_word):
            if letter == guess:
                word_display[index] = guess
    else:
        print("The word does not contain that letter")
        attempts -= 1
        print("You have " + str(attempts) + " attempts left")

if "_" not in word_display:
    print("You win.")
else:
    print("You lose.")
    print("The word was " + chosen_word)