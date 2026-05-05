"""
password_validator.py
─────────────────────
PasswordValidator sınıfı – kural tabanlı şifre doğrulama.
StrengthAnalyzer tarafından kullanılır (bağımlılık / dependency).
"""


class PasswordValidator:
    """
    Şifre doğrulama kurallarını yönetir.
    Encapsulation: kurallar private alanlarda tutulur,
    getter/setter metotlarıyla erişilir.
    """

    def __init__(
        self,
        min_length: int = 8,
        require_upper: bool = True,
        require_lower: bool = True,
        require_digit: bool = True,
        require_special: bool = False,
    ) -> None:
        # Private alanlar (Encapsulation)
        self._min_length: int = min_length
        self._require_upper: bool = require_upper
        self._require_lower: bool = require_lower
        self._require_digit: bool = require_digit
        self._require_special: bool = require_special

        # Kural tanımları: (kural_adı, açıklama, kontrol_fonksiyonu)
        self._rules: list[tuple] = self._build_rules()

    # ── Getter / Setter (Encapsulation) ────────────────────────────
    @property
    def min_length(self) -> int:
        return self._min_length

    @min_length.setter
    def min_length(self, value: int) -> None:
        if value < 1:
            raise ValueError("Minimum uzunluk en az 1 olmalıdır.")
        self._min_length = value
        self._rules = self._build_rules()  # kuralları güncelle

    # ── Kural yönetimi ──────────────────────────────────────────────
    def _build_rules(self) -> list[tuple]:
        """
        Aktif kurallara göre kural listesi oluşturur.
        Her kural: (kural_adı, açıklama, lambda kontrol fonksiyonu)
        """
        rules = [
            (
                "min_length",
                f"En az {self._min_length} karakter",
                lambda pw: len(pw) >= self._min_length,
            ),
        ]

        if self._require_upper:
            rules.append((
                "uppercase",
                "En az bir büyük harf",
                lambda pw: any(c.isupper() for c in pw),
            ))

        if self._require_lower:
            rules.append((
                "lowercase",
                "En az bir küçük harf",
                lambda pw: any(c.islower() for c in pw),
            ))

        if self._require_digit:
            rules.append((
                "digit",
                "En az bir rakam",
                lambda pw: any(c.isdigit() for c in pw),
            ))

        if self._require_special:
            rules.append((
                "special",
                "En az bir özel karakter (!@#$%^&* vb.)",
                lambda pw: any(not c.isalnum() for c in pw),
            ))

        return rules

    def get_rules(self) -> list[dict]:
        """Kural listesini okunabilir dict formatında döndürür."""
        return [
            {"name": name, "description": desc}
            for name, desc, _ in self._rules
        ]

    def check_rule(self, password: str, rule_name: str) -> bool:
        """Belirli bir kuralın geçip geçmediğini döndürür."""
        for name, _, check_fn in self._rules:
            if name == rule_name:
                return check_fn(password)
        raise ValueError(f"'{rule_name}' adında bir kural bulunamadı.")

    def validate(self, password: str) -> list[dict]:
        """
        Tüm kuralları şifreye uygular.
        Her kural için geçti/kaldı bilgisini döndürür.
        """
        results = []
        for name, desc, check_fn in self._rules:
            try:
                passed = check_fn(password)
            except Exception as e:
                passed = False
                desc = f"{desc} [Hata: {e}]"

            results.append({
                "name": name,
                "description": desc,
                "passed": passed,
                "icon": "✓" if passed else "✗",
            })

        return results

    def is_valid(self, password: str) -> bool:
        """Şifre tüm kuralları geçiyorsa True döndürür."""
        return all(r["passed"] for r in self.validate(password))

    def display_validation(self, password: str) -> None:
        """Doğrulama sonuçlarını terminale biçimli olarak yazdırır."""
        results = self.validate(password)
        passed_count = sum(1 for r in results if r["passed"])
        total = len(results)

        print("\n  📋 Kural Kontrol Sonuçları:")
        print(f"  ({passed_count}/{total} kural karşılandı)")
        print()

        for r in results:
            status = "✓" if r["passed"] else "✗"
            print(f"    {status} {r['description']}")

    def __repr__(self) -> str:
        return (
            f"PasswordValidator("
            f"min_length={self._min_length}, "
            f"rules={len(self._rules)})"
        )
