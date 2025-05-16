CONTINUE_MSG = "Press enter to continue:"

STARTING_MSG = """
You've entered a world where chance is king and risk is the price of power. 
Start with a modest sum, claw your way to $1000, and bend fortune to your will... 
If it doesn't break you first…"""

TUTORIAL = [
    "You start with a fixed amount of money.",
    "Your goal is to reach $1000.",
    "Each round, place a bet of your choosing.",
    "There's a 1 in 4 chance to lose your bet.",
    "You can buy buffs to reduce your odds of losing or manipulate the outcome.",
    "Winning adds cash. Losing subtracts a lot more.",
    "Spend wisely, bet strategically.",
]

DIALOGUE = [
    (1, "The dealer eyes you up and down, ready to spin the wheel."),
    (1, "A hush falls over the table as you place your bet."),
    (3, "You feel a twinge in your gut. Something's off this round."),
    (4, "The wheel groans louder than before — like it knows your odds."),
    (3, "Your hands shake as the stack of cash gets smaller."),
    (5, "Every click of the wheel hits like a heartbeat in your skull."),
    (4, "A cold breeze drifts in. You swear you see the dealer grin."),
    (3, "You feel your luck's about to shift. You just don't know which way."),
    (2, "It's too quiet. Like the room's holding its breath."),
    (5, "You're one bet away from something — you just don't know what."),
]

CHEATS = {
    "EzWin": 1000,
    "Boost": 300,
    "LoseGame": 0,
}

ITEMS = [
    {
        "name": "Loaded Dice",
        "effect": "Avoid a number of your choice.",
        "description": "Tampered and twisted. Luck has a favorite tonight.",
        "price_fraction": 0.10,
        "activation_line": "The dice hum softly. Reality tips in your favor.",
    },
    {
        "name": "Fortune's Favor",
        "effect": "50% chance to re-spin if you lose.",
        "description": "She's watching you. Just this once.",
        "price_fraction": 0.15,
        "activation_line": "A second chance stirs behind the curtain.",
    },
    {
        "name": "Echo Bet",
        "effect": "If you win, win again for free.",
        "description": "A whisper in time. A second chance disguised as déjà vu.",
        "price_fraction": 0.40,
        "activation_line": "The win echoes — once more, just like before.",
    },
    {
        "name": "The Doubler",
        "effect": "2x instead of 1.5x if you win.",
        "description": "A mirror bet placed in a world just beside ours.",
        "price_fraction": 0.25,
        "activation_line": "Your shadow bets beside you — and doubles it.",
    },
    {
        "name": "Ghost Bet",
        "effect": "Lose only 50% of your bet if you lose.",
        "description": "It was never really there to begin with.",
        "price_fraction": 0.20,
        "activation_line": "Your loss fades like a ghost in fog.",
    },
    {
        "name": "Dealer's Guilt",
        "effect": "Refunds your bet if you lose.",
        "description": "Even the house feels shame. Occasionally.",
        "price_fraction": 0.3,
        "activation_line": "The dealer sighs and returns your chips.",
    },
    {
        "name": "All or nothing",
        "effect": "+100% reward, -200% loss.",
        "description": "Turn the tables.",
        "price_fraction": 0.35,
        "activation_line": "The stakes stretch thin — too far to turn back.",
    },
    {
        "name": "Paranoia Charm",
        "effect": "Skip bet if losing number is yours.",
        "description": "Don't bet now.",
        "price_fraction": 0.20,
        "activation_line": "Something tells you not to play. You listen.",
    },
    {
        "name": "Wager Echo",
        "effect": "Apply 50% of the outcome again.",
        "description": "A ghost of the outcome circles back.",
        "price_fraction": 0.35,
        "activation_line": "The result lingers... then returns, half-formed.",
    },
]

WHEEL_MAX = 4
