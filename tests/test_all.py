"""
tests/test_all.py
─────────────────
Şifre Analiz Aracı – Birim testleri.
Tüm sınıfların temel işlevleri test edilir.
"""

import sys
import os
import unittest

# Proje kök dizinini Python yoluna ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.strength_analyzer import StrengthAnalyzer
from src.password_validator import PasswordValidator
from src.history_manager import HistoryManager


class TestPasswordValidator(unittest.TestCase):
    """PasswordValidator sınıfı birim testleri."""

    def setUp(self):
        self.validator = PasswordValidator(
            min_length=8,
            require_upper=True,
            require_lower=True,
            require_digit=True,
            require_special=True,
        )

    def test_strong_password_passes_all_rules(self):
        results = self.validator.validate("StrongP@ss1")
        failed = [r for r in results if not r["passed"]]
        self.assertEqual(len(failed), 0)

    def test_short_password_fails_min_length(self):
        self.assertFalse(self.validator.check_rule("Ab1!", "min_length"))

    def test_no_uppercase_fails(self):
        self.assertFalse(self.validator.check_rule("weakpass1!", "uppercase"))

    def test_is_valid_true(self):
        self.assertTrue(self.validator.is_valid("StrongP@ss1"))

    def test_is_valid_false(self):
        self.assertFalse(self.validator.is_valid("weak"))

    def test_invalid_rule_raises(self):
        with self.assertRaises(ValueError):
            self.validator.check_rule("test", "nonexistent_rule")


class TestStrengthAnalyzer(unittest.TestCase):
    """StrengthAnalyzer sınıfı birim testleri."""

    def test_strong_password_high_score(self):
        analyzer = StrengthAnalyzer("Tr0ub4dor&3")
        result = analyzer.analyze()
        self.assertGreaterEqual(result["score"], 3)

    def test_weak_password_low_score(self):
        analyzer = StrengthAnalyzer("abc")
        result = analyzer.analyze()
        self.assertLessEqual(result["score"], 2)

    def test_entropy_positive(self):
        analyzer = StrengthAnalyzer("TestPass123!")
        result = analyzer.analyze()
        self.assertGreater(result["entropy_bits"], 0)

    def test_empty_password_entropy_zero(self):
        analyzer = StrengthAnalyzer("")
        self.assertEqual(analyzer.calculate_entropy(), 0.0)

    def test_pattern_detection_repetitive(self):
        analyzer = StrengthAnalyzer("aaabbb")
        patterns = analyzer.check_patterns()
        self.assertTrue(len(patterns) > 0)

    def test_analyze_returns_dict(self):
        analyzer = StrengthAnalyzer("SomePassword1!")
        result = analyzer.analyze()
        self.assertIsInstance(result, dict)
        self.assertIn("score", result)
        self.assertIn("strength_label", result)
        self.assertIn("entropy_bits", result)

    def test_encapsulation_no_direct_score_change(self):
        """_score doğrudan dışarıdan değiştirilemez (property koruması)."""
        analyzer = StrengthAnalyzer("Test123!")
        analyzer.analyze()
        original_score = analyzer.score
        # Dışarıdan score değiştirilemez (property sadece getter)
        with self.assertRaises(AttributeError):
            analyzer.score = 99
        self.assertEqual(analyzer.score, original_score)


class TestHistoryManager(unittest.TestCase):
    """HistoryManager sınıfı birim testleri."""

    def setUp(self):
        self.manager = HistoryManager(max_size=5)
        self.sample_data = {
            "password_length": 10,
            "score": 3,
            "strength_label": "İyi",
            "entropy_bits": 3.2,
        }

    def test_add_and_retrieve(self):
        self.manager.add_entry(self.sample_data)
        self.assertEqual(self.manager.entry_count, 1)

    def test_max_size_enforced(self):
        for _ in range(10):
            self.manager.add_entry(self.sample_data)
        self.assertLessEqual(self.manager.entry_count, 5)

    def test_clear_removes_all(self):
        self.manager.add_entry(self.sample_data)
        self.manager.clear()
        self.assertEqual(self.manager.entry_count, 0)

    def test_get_last_returns_latest(self):
        self.manager.add_entry(self.sample_data)
        last = self.manager.get_last()
        self.assertIsNotNone(last)
        self.assertEqual(last["data"]["score"], 3)

    def test_empty_history_returns_none(self):
        self.assertIsNone(self.manager.get_last())

    def test_invalid_entry_raises(self):
        with self.assertRaises(TypeError):
            self.manager.add_entry("bu string, dict değil")

    def test_summary_correct(self):
        self.manager.add_entry({**self.sample_data, "score": 4})
        self.manager.add_entry({**self.sample_data, "score": 2})
        summary = self.manager.summary()
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["best_score"], 4)
        self.assertEqual(summary["worst_score"], 2)

    def test_get_history_returns_copy(self):
        """Dönen liste orijinal geçmişi etkilememelidir."""
        self.manager.add_entry(self.sample_data)
        history_copy = self.manager.get_history()
        history_copy.clear()
        self.assertEqual(self.manager.entry_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
