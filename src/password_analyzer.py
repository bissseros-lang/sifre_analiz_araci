"""
password_analyzer.py
────────────────────
Soyut temel sınıf: PasswordAnalyzer
Tüm analiz sınıfları bu sınıftan türetilir (Kalıtım / Inheritance).
"""

from abc import ABC, abstractmethod


class PasswordAnalyzer(ABC):
    """
    Şifre analiz hiyerarşisinin soyut temel sınıfı.
    Polymorphism: alt sınıflar analyze() ve display_result()
    metotlarını kendi ihtiyaçlarına göre override eder.
    """

    # Güç seviyesi sabitleri
    STRENGTH_LABELS = {
        0: "Çok Zayıf",
        1: "Zayıf",
        2: "Orta",
        3: "İyi",
        4: "Güçlü",
        5: "Çok Güçlü",
    }

    def __init__(self, password: str) -> None:
        """
        Encapsulation: _password özel (private) olarak saklanır.
        Dışarıdan doğrudan erişim engellenmiştir.
        """
        self._password: str = password   # private alan
        self._score: int = 0             # private skor alanı

    # ── Property: Encapsulation ──────────────────────────────────────
    @property
    def password(self) -> str:
        """Şifreyi döndürür (masked getter – isteğe bağlı loglama için)."""
        return self._password

    @property
    def score(self) -> int:
        """Analiz skorunu döndürür."""
        return self._score

    # ── Soyut metotlar (alt sınıflar zorunlu olarak implement etmeli) ─
    @abstractmethod
    def analyze(self) -> dict:
        """Şifreyi analiz eder, sonuçları dict olarak döndürür."""
        ...

    @abstractmethod
    def display_result(self) -> None:
        """Analiz sonucunu terminale biçimli olarak yazdırır."""
        ...

    # ── Ortak yardımcı metotlar ──────────────────────────────────────
    def calculate_score(self) -> int:
        """
        Temel skor hesaplama mantığı.
        Alt sınıflar bunu çağırıp üstüne ekleyebilir.
        """
        pw = self._password
        score = 0

        if len(pw) >= 8:
            score += 1
        if len(pw) >= 12:
            score += 1
        if any(c.isupper() for c in pw):
            score += 1
        if any(c.islower() for c in pw):
            score += 1
        if any(c.isdigit() for c in pw):
            score += 1
        if any(not c.isalnum() for c in pw):
            score += 1

        # Skoru 0-5 aralığına normalize et
        self._score = min(score, 5)
        return self._score

    def get_strength_label(self) -> str:
        """Skora karşılık gelen güç etiketini döndürür."""
        # Güç etiketini belirlemek için 5 üzerinden skor kullanılır
        index = min(self._score, 5)
        return self.STRENGTH_LABELS[index]

    def get_feedback(self) -> list[str]:
        """Genel iyileştirme önerileri listesi döndürür."""
        feedback = []
        pw = self._password

        if len(pw) < 8:
            feedback.append("En az 8 karakter kullanın.")
        if not any(c.isupper() for c in pw):
            feedback.append("En az bir büyük harf ekleyin (A-Z).")
        if not any(c.islower() for c in pw):
            feedback.append("En az bir küçük harf ekleyin (a-z).")
        if not any(c.isdigit() for c in pw):
            feedback.append("En az bir rakam ekleyin (0-9).")
        if not any(not c.isalnum() for c in pw):
            feedback.append("En az bir özel karakter ekleyin (!@#$%^&* vb.).")

        if not feedback:
            feedback.append("Şifreniz tüm temel kriterleri karşılıyor!")

        return feedback

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(score={self._score}, strength='{self.get_strength_label()}')"
        )
