"""
Unit Tests for Task 1: Password Generator
Auspify Technologies - Python Developer Internship
"""

import os
import sys
import unittest
import string

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from password_generator import (
    calculate_entropy,
    evaluate_strength,
    build_character_pool,
    generate_single_password,
    generate_batch,
)


class TestPasswordGenerator(unittest.TestCase):
    def test_entropy_calculation(self):
        self.assertEqual(calculate_entropy("", 26), 0.0)
        self.assertEqual(calculate_entropy("abc", 0), 0.0)
        entropy = calculate_entropy("password123", 62)
        self.assertGreater(entropy, 0.0)

    def test_strength_evaluation(self):
        weak_rating, _ = evaluate_strength("abc", 26)
        self.assertEqual(weak_rating, "Weak")

        strong_pwd = "P@ssw0rd!12345678"
        rating, desc = evaluate_strength(strong_pwd, 94)
        self.assertIn(rating, ["Strong", "Very Strong"])
        self.assertTrue(len(desc) > 0)

    def test_character_pool_and_ambiguous_filter(self):
        # Pool with all characters
        pool_all, _ = build_character_pool(exclude_ambiguous=False)
        self.assertTrue(any(c in pool_all for c in "il1Lo0O"))

        # Pool with ambiguous characters excluded
        pool_no_ambig, _ = build_character_pool(exclude_ambiguous=True)
        for ambig in "il1Lo0O":
            self.assertNotIn(ambig, pool_no_ambig)

    def test_password_length_and_categories(self):
        length = 20
        pwd, strength, desc = generate_single_password(
            length=length,
            include_upper=True,
            include_lower=True,
            include_digits=True,
            include_symbols=True,
            exclude_ambiguous=False
        )
        self.assertEqual(len(pwd), length)
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.islower() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))
        self.assertTrue(any(c in string.punctuation for c in pwd))

    def test_digits_only(self):
        pwd, _, _ = generate_single_password(
            length=10,
            include_upper=False,
            include_lower=False,
            include_digits=True,
            include_symbols=False
        )
        self.assertEqual(len(pwd), 10)
        self.assertTrue(pwd.isdigit())

    def test_batch_generation(self):
        count = 5
        batch = generate_batch(count=count, length=12)
        self.assertEqual(len(batch), count)
        for pwd, strength, desc in batch:
            self.assertEqual(len(pwd), 12)
            self.assertIsInstance(strength, str)
            self.assertIsInstance(desc, str)

    def test_invalid_category_selection(self):
        with self.assertRaises(ValueError):
            generate_single_password(
                length=10,
                include_upper=False,
                include_lower=False,
                include_digits=False,
                include_symbols=False
            )

    def test_length_less_than_guaranteed(self):
        # 4 categories requested but length requested is 2
        with self.assertRaises(ValueError):
            generate_single_password(
                length=2,
                include_upper=True,
                include_lower=True,
                include_digits=True,
                include_symbols=True
            )


if __name__ == "__main__":
    unittest.main()

