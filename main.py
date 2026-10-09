# secrets:  produces cryptographicaly secure random numbers (safer for passwords, random can be guessed, but I don't know how  [lol]  )
# string:   ready-made collections of characters like digits and letters

import secrets
import string

def generate_password(length: int = 20) -> str:
    # minimum length of 6 charakters
    if length < 6:
        raise ValueError("Length must be at least 6")

    # full pool 
    # lower- and uppercase letters, digits, and few special symbols
    alphabet = (
        string.ascii_letters                    # abc  ...  XYZ
        + string.digits                         # 0123456789
        + "!@#$%^&*()-_=+[]{};:,.<>?"           # special symbols
    )

    # le problem: 
    # picking every character from the pool alone could produce a password with NO digits or symbols
    #
    # !!!  UNSAFE  !!!
    #
    # lock one character per category in

    required = [
        secrets.choice(string.ascii_lowercase),                        # one lowercase
        secrets.choice(string.ascii_uppercase),                        # one uppercase
        secrets.choice(string.digits),                           # one digit
        secrets.choice("!@#$%^&*()-_=+[]{};:,.<>?"),             # one symbol
    ]

    # fill remaining positions with SecretS from full pool
    
    
    remaining = [secrets.choice(alphabet) for _ in range(length - len(required))]
    # add them
    password = required + remaining

    # Shuffle

    
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
