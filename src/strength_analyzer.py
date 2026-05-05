"""
strength_analyzer.py
────────────────────
StrengthAnalyzer sınıfı – PasswordAnalyzer'dan kalıtım (inheritance) alır.
Şifre gücünü entropi, karakter çeşitliliği ve örüntü analiziyle ölçer.
"""

import math
import re
from collections import Counter
from .password_analyzer import PasswordAnalyzer


class StrengthAnalyzer(PasswordAnalyzer):
    """
    Şifre gücünü ayrıntılı olarak analiz eden alt sınıf.
    PasswordAnalyzer'dan kalıtım alır; analyze() ve display_result()
    metotlarını override ederek Polymorphism örneği sunar.
    """

    # Zayıf / yaygın örüntüler (regex)
    COMMON_PATTERNS = [
        (r"(.)\1{2,}", "Tekrarlayan karakter dizisi"),
        (r"(012|123|234|345|456|567|678|789|890)", "Ardışık rakam dizisi"),
        (r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq)", "Ardışık harf dizisi"),
        (r"(qwerty|asdf|zxcv|qwer|asdfg)", "Klavye örüntüsü"),
        (r"^[a-zA-Z]+$", "Yalnızca harf"),
        (r"^[0-9]+$", "Yalnızca rakam"),
    ]

    def __init__(self, password: str) -> None:
        super().__init__(password)
        # Encapsulation: iç durum private alanlarla tutulur
        self._entropy: float = 0.0
        self._char_diversity: dict = {}
        self._detected_patterns: list[str] = []

    # ── Property erişimcileri (Encapsulation) ───────────────────────
    @property
    def entropy(self) -> float:
        return self._entropy

    @property
    def char_diversity(self) -> dict:
        return dict(self._char_diversity)  # kopya döndür, dışarıdan değiştirmesin

    # ── Override: Polymorphism ───────────────────────────────────────
    def analyze(self) -> dict:
        """
        Şifre analizini gerçekleştirir.
        Temel skor hesaplamayı, entropi ve örüntü kontrollerini birleştirir.
        """
        # 1. Temel skoru hesapla (üst sınıftan)
        base_score = self.calculate_score()

        # 2. Entropi hesapla
        self._entropy = self.calculate_entropy()

        # 3. Karakter çeşitliliğini belirle
        self._char_diversity = self._classify_characters()

        # 4. Zayıf örüntüleri tespit et
        self._detected_patterns = self.check_patterns()

        # 5. Örüntü cezalarını uygula
        penalty = len(self._detected_patterns)
        final_score = max(0, base_score - penalty)
        self._score = final_score

        return {
            "password_length": len(self._password),
            "score": self._score,
            "strength_label": self.get_strength_label(),
            "entropy_bits": round(self._entropy, 2),
            "char_diversity": self._char_diversity,
            "detected_patterns": self._detected_patterns,
            "feedback": self.get_feedback(),
        }

    def calculate_entropy(self) -> float:
        """
        Shannon entropisi hesaplar.
        H = -Σ p(x) * log2(p(x))
        Yüksek entropi → daha tahmin edilemez şifre.
        """
        if not self._password:
            return 0.0

        freq = Counter(self._password)
        total = len(self._password)

        entropy = 0.0
        for count in freq.values():
            prob = count / total
            entropy -= prob * math.log2(prob)

        return entropy

    def check_patterns(self) -> list[str]:
        """Şifrede zayıf örüntüleri arar, bulunanların açıklamasını döndürür."""
        found = []
        pw_lower = self._password.lower()

        for pattern, description in self.COMMON_PATTERNS:
            try:
                if re.search(pattern, pw_lower):
                    found.append(description)
            except re.error:
                # Regex hatası sessizce atlanır
                continue

        return found

    def _classify_characters(self) -> dict:
        """Şifredeki karakter türlerini sayar ve sınıflandırır."""
        pw = self._password
        diversity = {
            "lowercase": sum(1 for c in pw if c.islower()),
            "uppercase": sum(1 for c in pw if c.isupper()),
            "digits": sum(1 for c in pw if c.isdigit()),
            "special": sum(1 for c in pw if not c.isalnum()),
            "unique_chars": len(set(pw)),
        }
        return diversity

    # ── Override: Polymorphism ───────────────────────────────────────
    def display_result(self) -> None:
        """
        Analiz sonuçlarını terminale renkli ve biçimli olarak yazdırır.
        """
        result = self.analyze()
        pw_len = result["password_length"]
        label = result["strength_label"]
        score = result["score"]
        entropy = result["entropy_bits"]
        diversity = result["char_diversity"]
        patterns = result["detected_patterns"]
        feedback = result["feedback"]

        # Skor çubuğu
        bar_filled = "█" * score
        bar_empty = "░" * (5 - score)
        bar = f"[{bar_filled}{bar_empty}]"

        print("\n" + "=" * 50)
        print("  🔐 ŞİFRE GÜÇ ANALİZİ")
        print("=" * 50)
        print(f"  Uzunluk   : {pw_len} karakter")
        print(f"  Güç       : {label} {bar}  ({score}/5)")
        print(f"  Entropi   : {entropy} bit")
        print()

        print("  📊 Karakter Dağılımı:")
        print(f"    Küçük harf  : {diversity['lowercase']}")
        print(f"    Büyük harf  : {diversity['uppercase']}")
        print(f"    Rakam       : {diversity['digits']}")
        print(f"    Özel karakter: {diversity['special']}")
        print(f"    Benzersiz   : {diversity['unique_chars']}")
        print()

        if patterns:
            print("  ⚠️  Tespit Edilen Zayıf Örüntüler:")
            for p in patterns:
                print(f"    • {p}")
            print()

        print("  💡 Öneriler:")
        for tip in feedback:
            print(f"    → {tip}")
        print("=" * 50)
