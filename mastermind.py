import itertools as it
import random

number_of_pegs = 5
colors = ["Red", "Blue", "Green", "Black", "Yellow", "Orange", "White", "Brown"]
possible_combinations = None
guess_automatically = False

def main():
    setup()
    number_of_guesses = 1

    while (len(possible_combinations) > 1):
        print("There are", len(possible_combinations), "remaining guesses")

        if guess_automatically:
            guess = choose_guess()
            print("Please guess", " ".join(guess))
        else:
            guess = get_guess_from_player()
            if guess == ["Show"]:
                for possible_combination in possible_combinations:
                    print(" ".join(possible_combination))
                print()
                continue

        result = get_result_from_player()
        eliminate_guesses(guess, result)
        print()
        number_of_guesses += 1

    if len(possible_combinations) == 0:
        print("No possible guesses remain...")
        print("Something wrong happened somewhere")
        return

    print("The answer is", " ".join(possible_combinations[0]))
    print("This took", number_of_guesses, "guesses")


def get_guess_from_player():
    guess = input("Enter what you guessed (or 'show'): ").strip().title().split()
    return guess



def setup():
    global possible_combinations, guess_automatically
    print("Game parameters:")
    print("     Pegs: ", number_of_pegs)
    print("     Colors: ", end = "")
    for color in colors:
        print(color, end=" ")
    print("\n     Guessing automatically: ", guess_automatically)
    print("\n\n")
    possible_combinations = generate_all_combinations()


def choose_guess():
    global possible_combinations
    choice = random.randint(0, len(possible_combinations))
    guess = possible_combinations.pop(choice)
    return guess

def get_result_from_player():
    print("Please enter the result of the guess:")
    number_of_blacks = int(input("# of blacks: "))
    number_of_whites = int(input("# of whites: "))
    return (number_of_blacks, number_of_whites)

def generate_all_combinations():
    return list(it.product(colors, repeat=number_of_pegs))


# Remove any possible combinations that don't create the result given
# Treat the guess as the correct answer
def eliminate_guesses(guess, given_result):
    global possible_combinations
    correct_guesses = []
    for combination in possible_combinations:
        result = evaluate_guess(guess, combination)
        if result == given_result:
            correct_guesses.append(combination)

    possible_combinations = correct_guesses

# First return is when the correct color is in the correct location
# Second return is correct color in wrong location
def evaluate_guess(guess, answer):
    number_correct_all = 0
    number_correct_color = 0
    guess_colors = {}
    answer_colors = {}
    
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            number_correct_all += 1
        else:
            guess_colors.setdefault(guess[i], 0)
            answer_colors.setdefault(answer[i], 0)

            guess_colors[guess[i]] += 1
            answer_colors[answer[i]] += 1

    for color, count in guess_colors.items():
        answer_count = answer_colors.get(color, 0)
        overlap = min(count, answer_count)
        number_correct_color += overlap

    return (number_correct_all, number_correct_color)

if __name__ == "__main__":
    main()