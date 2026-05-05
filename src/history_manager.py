"""
history_manager.py
──────────────────
HistoryManager sınıfı – analiz geçmişini yönetir.
Oturum boyunca yapılan analizleri bellekte tutar ve raporlar.
"""

from datetime import datetime


class HistoryManager:
    """
    Analiz oturumunun geçmişini yöneten sınıf.
    Encapsulation: geçmiş listesi private alanda tutulur.
    """

    def __init__(self, max_size: int = 50) -> None:
        self._history: list[dict] = []     # private – dışarıdan doğrudan erişilmez
        self._max_size: int = max_size     # maksimum kayıt sayısı

    # ── Property (Encapsulation) ─────────────────────────────────────
    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def entry_count(self) -> int:
        return len(self._history)

    # ── Geçmiş işlemleri ────────────────────────────────────────────
    def add_entry(self, analysis_data: dict) -> None:
        """
        Analiz sonucunu geçmişe ekler.
        Maksimum boyut aşılırsa en eski kaydı siler (FIFO).
        """
        if not isinstance(analysis_data, dict):
            raise TypeError("Analiz verisi dict tipinde olmalıdır.")

        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "data": analysis_data,
        }

        if len(self._history) >= self._max_size:
            self._history.pop(0)  # En eski kaydı çıkar

        self._history.append(entry)

    def get_history(self) -> list[dict]:
        """Geçmiş listesinin kopyasını döndürür."""
        return list(self._history)  # kopya – orijinale müdahale edilemez

    def get_last(self) -> dict | None:
        """En son analiz kaydını döndürür."""
        return self._history[-1] if self._history else None

    def clear(self) -> None:
        """Geçmişi temizler."""
        self._history.clear()

    def export_session(self) -> str:
        """
        Oturum geçmişini okunabilir metin formatında döndürür.
        Dosyaya kaydetmek veya ekrana yazdırmak için kullanılır.
        """
        if not self._history:
            return "  Bu oturumda henüz analiz yapılmadı."

        lines = [
            "=" * 50,
            "  OTURUM GEÇMİŞİ",
            "=" * 50,
        ]

        for i, entry in enumerate(self._history, start=1):
            data = entry["data"]
            timestamp = entry["timestamp"]
            pw_len = data.get("password_length", "?")
            label = data.get("strength_label", "?")
            score = data.get("score", "?")

            lines.append(
                f"  [{i:02d}] {timestamp}  |  "
                f"Uzunluk: {pw_len}  |  "
                f"Güç: {label} ({score}/5)"
            )

        lines.append("=" * 50)
        return "\n".join(lines)

    def display_history(self) -> None:
        """Geçmişi terminale yazdırır."""
        print(self.export_session())

    def summary(self) -> dict:
        """Oturum istatistiklerini özetler."""
        if not self._history:
            return {"total": 0, "avg_score": 0, "best_score": 0}

        scores = [e["data"].get("score", 0) for e in self._history]
        return {
            "total": len(scores),
            "avg_score": round(sum(scores) / len(scores), 2),
            "best_score": max(scores),
            "worst_score": min(scores),
        }

    def __repr__(self) -> str:
        return f"HistoryManager(entries={self.entry_count}, max={self._max_size})"
