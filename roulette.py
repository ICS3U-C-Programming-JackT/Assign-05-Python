#!/usr/bin/env python3
# Created By: Jack Turcotte
# Date: May 14th, 2025

# Roulette game in python

import os
import random
import time
import constants


# === Color Print Function ===
def c_print(text, color="white", end="\n", flush=False, rgb=None):
    named_colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "blue": (0, 128, 255),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
        "gray": (128, 128, 128),
        "black": (0, 0, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 105, 180),
    }

    # Use custom RGB or fallback to named color
    if rgb:
        r, g, b = rgb
    else:
        r, g, b = named_colors.get(color.lower(), (255, 255, 255))

    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end, flush=flush)


# === Redraw Terminal ===
def redraw_terminal():
    # Clear and rewrite terminal
    os.system("clear")
    c_print("-----------------|JackRoulette|-----------------")


# === Prompt Continue ===
def prompt_continue():
    for i in constants.CONTINUE_MSG:
        c_print(i, "yellow", end="", flush=True)
        time.sleep(0.1)
    input("")


def item_activate(item):
    for i in constants.ITEMS:
        if i["name"].lower() == item.lower():
            c_print(f"🜲 {i['activation_line']}", "blue")
            break


# === Shop ===
def open_shop(user_money):
    print("\n🛒 Welcome to the Shop! Choose one item to aid your next bet.")
    available = random.sample(constants.ITEMS, 3)

    prices = {}
    for item in available:
        base_price = item["price_fraction"] * user_money
        modifier = random.randint(-10, 10)
        final_price = max(1, round(base_price + modifier))
        prices[item["name"].lower()] = final_price

        print(f"\n- {item['name']}")
        print(f"  Effect: {item['effect']}")
        print(f"  {item['description']}")
        print(f"  💸 Price: ${final_price}")

    choice = (
        input("\nEnter the name of the item you want to buy (or press Enter to skip): ")
        .strip()
        .lower()
    )

    redraw_terminal()

    if choice == "":
        print("You walk away empty-handed... for now.")
        return "N/A", user_money

    if choice in prices:
        price = prices[choice]
        if user_money >= price:
            user_money -= price
            print(f"You purchased '{choice.title()}' for ${price}.")
            return choice, user_money
        else:
            print("You can't afford that. Maybe next round.")
            return "N/A", user_money
    else:
        print("That item isn't for sale right now.")
        return "N/A", user_money


def roulette(bet, item):
    # === Print item info if it exists ===
    item_data = (
        next((i for i in constants.ITEMS if i["name"].lower() == item.lower()), None)
        if item != "N/A"
        else ""
    )

    if item_data != "":
        c_print(f"[{item_data['name']}] — {item_data['effect']}", "cyan")
        c_print(item_data["description"], "white")
        c_print(f"🜲 {item_data['activation_line']}", "blue")
    else:
        item = "N/A"  # Disable item effects if it's invalid

    # === Handle loaded dice ===
    if item == "loaded dice":
        while True:
            try:
                excluded = int(
                    input(
                        "Which number do you want to remove? (1-{}): ".format(
                            constants.WHEEL_MAX
                        )
                    )
                )
                if excluded not in range(1, 5):
                    raise ValueError
                break
            except ValueError:
                c_print(
                    "Please enter a number between 1 and {}.".format(
                        constants.WHEEL_MAX
                    ),
                    "red",
                )
        c_print(f"You've disabled {excluded} from the spin.", "yellow")

        losing_number = random.randint(1, constants.WHEEL_MAX)
        while losing_number == excluded:
            losing_number = random.randint(1, constants.WHEEL_MAX)
    else:
        losing_number = random.randint(1, constants.WHEEL_MAX)

    # === Spinning effect ===
    spin_duration = random.randint(40, 60)
    current_number = 1

    for i in range(spin_duration):
        redraw_terminal()
        c_print("Spinning...", color="yellow")
        c_print("####|00{}|####".format(current_number), color="magenta")
        time.sleep(0.05)
        current_number = (
            current_number + 1 if current_number < constants.WHEEL_MAX else 1
        )

    landed_number = current_number

    # === Determine Win or Loss ===
    redraw_terminal()

    lost = landed_number == losing_number

    # Paranoia Charm: Skip if losing number is yours
    if item == "paranoia charm" and lost:
        item_activate(item)
        c_print(f"Losing number was: {losing_number}", "white")
        return 0

    if lost:
        c_print("LOSE |00{}| LOSE".format(landed_number), color="red")
        c_print("The wheel lands on the cursed number.", color="red")

        if item == "ghost bet":
            earnings = -int(bet * 0.75)
        elif item == "dealer's guilt":
            earnings = 0
        elif item == "all or nothing":
            earnings = -int(bet * 2.0)
        elif item == "omen of doubt":
            if random.random() <= 0.10:
                c_print("Somehow, you keep your money...", "yellow")
                earnings = 0
            else:
                earnings = -int(bet * 1.5)
        else:
            earnings = -int(bet * 1.5)
    else:
        c_print("WIN  |00{}|  WIN".format(landed_number), color="green")
        c_print("Luck smiles at you... for now.", color="green")

        if item == "the doubler":
            earnings = int(bet * 1.0)
        elif item == "all or nothing":
            earnings = int(bet * 1.0)
        else:
            earnings = int(bet * 0.5)

    # === Wager Echo: 50% of outcome again ===
    if item == "wager echo":
        item_activate(item)
        earnings += int(earnings * 0.5)

    # === Echo Bet: Double win if win ===
    if item == "echo bet" and earnings > 0:
        item_activate(item)
        earnings += earnings

    # === Fortune's Favor: Re-spin on loss (20% chance) ===
    if item == "fortune's favor" and lost and random.random() <= 0.5:
        item_activate(item)
        return roulette(bet, item)

    # === Show Final Results ===
    c_print(f"Losing number was: {losing_number}", color="white")
    c_print(f"You {'lost' if earnings < 0 else 'won'} ${abs(earnings)}", color="cyan")
    prompt_continue()
    return earnings


# === Game Loop ===
def game():
    user_money = 100  # Starting cash
    game_won = True  # Initialize for when game ends

    while True:
        redraw_terminal()

        # Determine intensity for dialogue
        intensity = 0
        if user_money > 800:
            intensity = 5
        elif user_money > 500:
            intensity = 4
        elif user_money > 300:
            intensity = 3
        elif user_money > 200:
            intensity = 2
        else:
            intensity = 1

        # Valid choices for dialogue options
        choices = []
        for intens, text in constants.DIALOGUE:
            if intens == intensity:
                choices.append(text)

        # Pick random message and display it
        chosen = choices[random.randint(0, len(choices) - 1)]
        c_print(f"{chosen}", color="gray")

        # Display currency
        c_print(f"Your current money: ${user_money}", color="cyan")

        # Try catch to prevent errors
        try:

            c_print(
                "\nDo you want to visit the shop before placing your bet? (y/n)",
                color="yellow",
            )
            shop_choice = input("> ").strip().lower()
            item = "N/A"
            
            if shop_choice == "y":
                item_bought, money = open_shop(user_money)
                found_item = False
                for item_in_dict in constants.ITEMS:
                    if item_bought.lower() == item_in_dict["name"].lower():
                        found_item = True
                if found_item == True:
                    item = item_bought
                    user_money = money
                else:
                    item = "N/A"


                        
            else:
                c_print(
                    "You ignore the strange merchant lingering in the corner...",
                    color="gray",
                )
                time.sleep(2)
                redraw_terminal()

            chosen = choices[random.randint(0, len(choices) - 1)]
            c_print(f"{chosen}", color="gray")
            c_print(f"Your current money: ${user_money}", color="cyan")

            # Get user bet
            user_bet_input = input("Enter your bet for this round: ").strip()
            user_bet = user_bet_input

            if user_bet_input in constants.CHEATS:
                user_money += constants.CHEATS[user_bet_input]
                if constants.CHEATS[user_bet_input] == 0:
                    user_money = 0
                raise ValueError("Hacking the mainframe...")
            else:
                # If not a number of any kind, raise value error
                if not user_bet_input.isdigit():
                    raise ValueError("Bet must be a positive whole number.")
                user_bet = int(user_bet_input)

            # If user bet is invalid, raise value error
            if user_bet < 0:
                raise ValueError("Bet must be greater than or equal to zero.")
            if user_bet > user_money:
                raise ValueError("You can't bet more than you have.")

            # Run roulette and update money
            earnings = roulette(user_bet, item)  # if you have item system
            user_money += earnings

            # End sequence given user has lost or won
            if user_money <= 0:
                # Lose dialogue
                game_won = False
                redraw_terminal()
                time.sleep(1)
                c_print(
                    "The moment it happens, everything goes quiet. The world feels heavy, like time itself is holding its breath.",
                    color="red",
                )
                time.sleep(2)
                c_print(
                    "You feel the weight of the loss sink deep, as if the universe itself has turned its back on you.",
                    color="red",
                )
                time.sleep(2)
                c_print(
                    "Your vision blurs as the coins slip through your fingers, lost forever to the cruel whims of fate.",
                    color="magenta",
                )
                time.sleep(2)
                c_print(
                    "But there's no time to dwell. You have to pick yourself up... there's always another round.",
                    color="magenta",
                )
                time.sleep(2)
                c_print("The loss stings, but it's not the end. Not yet.", color="red")
                break  # Exit secondary game loop
            if user_money >= 1000:
                # Win dialogue
                game_won = True
                redraw_terminal()
                time.sleep(1)
                c_print(
                    "The world feels like it slows down, your heart racing as the realization hits you...",
                    color="cyan",
                )
                time.sleep(2)
                c_print(
                    "Your hands tremble as the coins spill into your pockets, your dreams now one step closer.",
                    color="cyan",
                )
                time.sleep(2)
                c_print(
                    "You breathe deeply, the tension of the game melting away into a flood of triumph.",
                    color="yellow",
                )
                time.sleep(2)
                c_print(
                    "For a moment, it's as if the universe itself acknowledges your victory. This is your time.",
                    color="green",
                )
                time.sleep(2)
                c_print(
                    f"You're one step closer to the life you've always imagined...",
                    color="green",
                )
                break  # Exit secondary game loop
        # Exception linked to value error, ve = error msg
        except ValueError as ve:
            c_print(f"Error: {ve}", color="red")
            time.sleep(1.5)

    # Prompt restart when game is over
    restart = "n"
    if game_won == True:

        # Once the game finishes
        restart = input("Do you quit while you're ahead? (y/n): ").strip().lower()
    else:

        # Once the game finishes
        restart = (
            input("Will you succumb to the power of the mighty wheel? (y/n): ")
            .strip()
            .lower()
        )

    # Return restart
    return False if restart == "y" else True


# === Tutorial ===
def tutorial():
    c_print(constants.STARTING_MSG, "cyan")
    tut = input("Would you like a tutorial? (y/n): ").strip().lower()
    if tut == "y":
        for i in constants.TUTORIAL:
            c_print(i, "white")
            time.sleep(0.8)
        confirm = input("Does that sound good? (y/n): ").strip().lower()
        if confirm == "n":
            c_print("Oh well, times-a ticking, let's get started!", "yellow")
        else:
            c_print("Perfect! Let's do this!", "green")
    else:
        c_print("Let's get this party started!", "green")

    c_print("Traveling to the casino", "magenta", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        c_print(".", "magenta", end="", flush=True)
    time.sleep(1)


# === Main ===
def main():
    tutorial()

    # While loop to loop while player wants to restart
    while True:
        # Start game
        re = game()
        if re == False:

            # If they decide not to restart
            c_print("Farewell friend, may the odds be forever in your favour", "gray")
            time.sleep(1)
            c_print("And remember, 99% of gamblers quit before they win big...", "gray")
            break  # Exit primary game loop


if __name__ == "__main__":
    main()
