"""
Task 1: Password Generator
Auspify Technologies - Python Developer Internship

Features:
- Customizable password length with validation
- Include/exclude uppercase, lowercase, numbers, and special symbols
- Option to exclude ambiguous characters (l, 1, I, o, 0, O)
- Cryptographically secure generation using Python's `secrets` module
- Password strength analyzer (Weak, Moderate, Strong, Very Strong)
- Generate multiple passwords at once
- Save generated passwords to a file
- CLI and argument support
"""

import sys
import string
import secrets
import math
from typing import List, Dict, Tuple


def calculate_entropy(password: str, pool_size: int) -> float:
    """Calculates password information entropy in bits."""
    if not password or pool_size <= 0:
        return 0.0
    return len(password) * math.log2(pool_size)


def evaluate_strength(password: str, pool_size: int) -> Tuple[str, str]:
    """
    Evaluates password strength based on length, complexity, and entropy.
    Returns (rating, description).
    """
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    types_count = sum([has_lower, has_upper, has_digit, has_symbol])
    entropy = calculate_entropy(password, pool_size)

    if length < 8 or types_count < 2 or entropy < 35:
        return "Weak", "Vulnerable to quick brute-force attacks."
    elif length < 12 or types_count < 3 or entropy < 55:
        return "Moderate", "Fair security for casual, low-risk accounts."
    elif length < 16 or types_count < 4 or entropy < 75:
        return "Strong", "Recommended for sensitive personal accounts."
    else:
        return "Very Strong", "Excellent entropy, highly resistant to brute force."


def build_character_pool(
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False
) -> Tuple[str, List[str]]:
    """
    Constructs the character pool and guaranteed character sets.
    """
    ambiguous = set("il1Lo0O")
    
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if exclude_ambiguous:
        upper = "".join(c for c in upper if c not in ambiguous)
        lower = "".join(c for c in lower if c not in ambiguous)
        digits = "".join(c for c in digits if c not in ambiguous)
        symbols = "".join(c for c in symbols if c not in ambiguous)

    pool = ""
    guaranteed = []

    if include_upper and upper:
        pool += upper
        guaranteed.append(secrets.choice(upper))
    if include_lower and lower:
        pool += lower
        guaranteed.append(secrets.choice(lower))
    if include_digits and digits:
        pool += digits
        guaranteed.append(secrets.choice(digits))
    if include_symbols and symbols:
        pool += symbols
        guaranteed.append(secrets.choice(symbols))

    return pool, guaranteed


def generate_single_password(
    length: int,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False
) -> Tuple[str, str, str]:
    """
    Generates a secure password and returns (password, strength_label, description).
    """
    pool, guaranteed = build_character_pool(
        include_upper, include_lower, include_digits, include_symbols, exclude_ambiguous
    )

    if not pool:
        raise ValueError("At least one character category must be selected!")

    if length < len(guaranteed):
        raise ValueError(f"Password length must be at least {len(guaranteed)} to include all selected character types.")

    # Fill remaining characters securely
    remaining_length = length - len(guaranteed)
    password_chars = guaranteed + [secrets.choice(pool) for _ in range(remaining_length)]
    
    # Shuffle to eliminate predictable prefix
    secrets.SystemRandom().shuffle(password_chars)
    password = "".join(password_chars)

    strength, desc = evaluate_strength(password, len(pool))
    return password, strength, desc


def generate_batch(count: int, **kwargs) -> List[Tuple[str, str, str]]:
    """Generates multiple passwords with the given parameters."""
    return [generate_single_password(**kwargs) for _ in range(count)]


def print_banner():
    banner = r"""
==================================================================
        AUSPIFY TECHNOLOGIES - PYTHON INTERNSHIP PROGRAM
                   TASK 1: PASSWORD GENERATOR
==================================================================
    * Cryptographically Secure (secrets module)
    * Custom Character Sets & Ambiguity Filters
    * Strength & Entropy Evaluation
    * Batch Generation & Export Capability
==================================================================
"""
    print(banner)


def get_yes_no(prompt: str, default: bool = True) -> bool:
    default_str = "[Y/n]" if default else "[y/N]"
    while True:
        choice = input(f"{prompt} {default_str}: ").strip().lower()
        if not choice:
            return default
        if choice in ['y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
        print("Invalid input. Please enter 'y' or 'n'.")


def interactive_cli():
    print_banner()

    while True:
        try:
            print("\n--- Password Configuration ---")
            
            # Step 1: Password length
            while True:
                length_input = input("Enter password length (minimum 4, recommended 16) [16]: ").strip()
                if not length_input:
                    length = 16
                    break
                try:
                    length = int(length_input)
                    if length < 4:
                        print("Length must be at least 4 characters for safety.")
                        continue
                    if length > 256:
                        print("Length cannot exceed 256 characters.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid whole number.")

            # Step 2: Include letters, numbers, symbols
            print("\nSelect character types:")
            inc_upper = get_yes_no("  Include uppercase letters (A-Z)?", True)
            inc_lower = get_yes_no("  Include lowercase letters (a-z)?", True)
            inc_digits = get_yes_no("  Include digits (0-9)?", True)
            inc_symbols = get_yes_no("  Include special symbols (!@#$...)?", True)
            exc_ambig = get_yes_no("  Exclude ambiguous characters (l, 1, I, o, 0, O)?", False)

            if not any([inc_upper, inc_lower, inc_digits, inc_symbols]):
                print("\nError: You must select at least one character type! Please try again.")
                continue

            # Step 5: Multiple passwords
            while True:
                count_input = input("\nHow many passwords do you want to generate? [1]: ").strip()
                if not count_input:
                    count = 1
                    break
                try:
                    count = int(count_input)
                    if count < 1 or count > 50:
                        print("Please enter a count between 1 and 50.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")

            # Step 3 & 4: Generate & Display
            print("\n" + "=" * 60)
            print(f"Generated {count} Secure Password{'s' if count > 1 else ''}:")
            print("=" * 60)

            results = generate_batch(
                count=count,
                length=length,
                include_upper=inc_upper,
                include_lower=inc_lower,
                include_digits=inc_digits,
                include_symbols=inc_symbols,
                exclude_ambiguous=exc_ambig
            )

            for idx, (pwd, strength, desc) in enumerate(results, start=1):
                print(f"[{idx}] {pwd}")
                print(f"    Strength: {strength.upper()} | Note: {desc}")

            print("=" * 60)

            # Option to save to file
            if get_yes_no("\nWould you like to save these passwords to a text file?", False):
                filename = input("Enter filename [passwords.txt]: ").strip() or "passwords.txt"
                try:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"\n--- Generated {count} Password(s) (Length: {length}) ---\n")
                        for idx, (pwd, strength, _) in enumerate(results, start=1):
                            f.write(f"{idx}. {pwd} (Strength: {strength})\n")
                    print(f"Saved successfully to '{filename}'!")
                except Exception as e:
                    print(f"Error saving file: {e}")

        except Exception as err:
            print(f"Unexpected error: {err}")

        # Continue or exit
        if not get_yes_no("\nDo you want to generate more passwords?", True):
            print("\nThank you for using the Auspify Password Generator! Goodbye!\n")
            break


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("Usage: python password_generator.py")
        print("Launches interactive CLI for secure password generation.")
        return
    interactive_cli()


if __name__ == "__main__":
    main()
