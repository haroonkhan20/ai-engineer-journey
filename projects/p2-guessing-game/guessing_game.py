
import random

def get_random_number(low=1, high=50):
    return random.randint(low, high)

def check_guess(guess, answer):
    if guess < answer:
        return "too low"
    elif guess > answer:
        return "too high"
    else:
        return "correct"

def main():
    print("=" * 35)
    print("   Number Guessing Game v3")
    print("=" * 35)

    playing = True

    while playing:
        # ← These MUST be inside while playing so they reset each game
        answer    = get_random_number()
        attempts  = 0
        max_tries = 5

        print("\nI picked a number between 1 and 50!")

        while attempts < max_tries:
            guess    = int(input(f"Guess ({attempts+1}/{max_tries}): "))
            attempts += 1
            result   = check_guess(guess, answer)

            if result == "correct":
                score = max_tries - attempts + 1
                print(f"Correct! Got it in {attempts} guess(es)!")
                print(f"Your score: {score} points!")
                break
            else:
                print(f"  Hint: {guess} is {result}!")
                if attempts == max_tries:
                    print(f"Game Over! Answer was {answer}.")

        # ← This is inside while playing, outside while attempts
        play_again = input("\nPlay again? (Y/N): ").strip().upper()
        if play_again != "Y":
            print("Thank you for playing!")
            playing = False

if __name__ == "__main__":
    main()