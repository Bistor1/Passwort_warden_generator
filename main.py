# Standard library modules:
# - secrets:  produces cryptographically secure random numbers (safe for passwords!)
#             Use this instead of the older "random" module, which is meant for
#             games/simulations and is guessable.
# - string:   ready-made collections of characters like digits or letters

import secrets
import string


def generate_password(length: int = 20) -> str:
    """Generate a random password.

    length: how many characters the password should have (default 20).
    Returns the password as a text string.
    """

    # Refuse tiny passwords so we can still guarantee at least one character
    # from each category below (4 categories => minimum of 4 positions).
    if length < 4:
        raise ValueError("Length must be at least 4")

    # The full pool of characters any password position may come from:
    # lowercase + uppercase letters, digits, and a set of special symbols.
    alphabet = (
        string.ascii_letters          # abc...XYZ
        + string.digits               # 0123456789
        + "!@#$%^&*()-_=+[]{};:,.<>?"  # special symbols
    )

    # Problem: picking every character from the pool alone can accidentally
    # produce a password with NO digits or NO symbols (bad for sites that
    # demand them). So first lock in one guaranteed character per category...
    required = [
        secrets.choice(string.ascii_lowercase),                        # one lowercase
        secrets.choice(string.ascii_uppercase),                        # one uppercase
        secrets.choice(string.digits),                                 # one digit
        secrets.choice("!@#$%^&*()-_=+[]{};:,.<>?"),                  # one symbol
    ]

    # ...and fill the remaining positions with random picks from the full pool.
    remaining = [secrets.choice(alphabet) for _ in range(length - len(required))]

    # Join guaranteed + random characters together (guaranteed ones are
    # currently at the front, which looks suspicious -> shuffle next).
    password = required + remaining

    # Shuffle: rearrange all characters into a truly random order.
    # This is Fisher-Yates shuffling done with secure randomness:
    # walk from the end of the list to the beginning, and on each step swap
    # the current item with a randomly chosen earlier one (randbelow => 0..i).
    # Doing it backwards ensures every position gets mixed in fairly.
    pool = list(password)
    for i in reversed(range(len(pool))):
        j = secrets.randbelow(i + 1)       # random index from 0 up to and including i
        pool[i], pool[j] = pool[j], pool[i]  # swap the two characters (Python tuple trick)

    return "".join(pool)


def main() -> None:
    """Interactive part: ask the user how long, print a password."""
    try:
        length_str = input("Desired password length [20]: ").strip()  # .strip() removes leading/trailing spaces
        # Convert to number only if the user actually typed something;
        # an empty answer means "use the default of 20".
        length = int(length_str) if length_str else 20
        print(generate_password(length))
    except ValueError as e:
        # Raised when input() got text that is not a number (e.g. "abc")
        # or when generate_password refuses a too-small value (< 4).
        print(f"Invalid input: {e}")


# Only run main() when this file itself was started with python,
# NOT when it is imported as a module into another script.
if __name__ == "__main__":
    main()
