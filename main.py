import secrets
import string


def generate_password(length: int = 20) -> str:
    """Generate a random password."""
    if length < 4:
        raise ValueError("Length must be at least 4")

    alphabet = (
        string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
    )

    # Guarantee at least one character from each basic category.
    required = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+[]{};:,.<>?"),
    ]

    remaining = [secrets.choice(alphabet) for _ in range(length - len(required))]
    password = required + remaining

    # Shuffle so the guaranteed characters are not always first.
    pool = list(password)
    for i in reversed(range(len(pool))):
        j = secrets.randbelow(i + 1)
        pool[i], pool[j] = pool[j], pool[i]
    return "".join(pool)


def main() -> None:
    try:
        length_str = input("Desired password length [20]: ").strip()
        length = int(length_str) if length_str else 20
        print(generate_password(length))
    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
