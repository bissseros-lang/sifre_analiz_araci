"""
main.py
───────
Şifre Analiz Aracı – Ana CLI giriş noktası.
Kullanıcı etkileşimi, menü döngüsü ve hata yönetimi burada bulunur.
"""

import sys
import getpass

# Proje kök dizinini Python yoluna ekle (importlar için)
sys.path.insert(0, __import__("os").path.dirname(__file__))

from src.strength_analyzer import StrengthAnalyzer
from src.password_validator import PasswordValidator
from src.history_manager import HistoryManager


# ─── Yardımcı fonksiyonlar ────────────────────────────────────────────

def print_banner() -> None:
    """Uygulama başlık ekranını yazdırır."""
    print("\n" + "=" * 50)
    print("  🔐 ŞİFRE ANALİZ ARACI  v1.0")
    print("  OOP ile geliştirilmiş – Python")
    print("=" * 50)


def print_menu() -> None:
    """Ana menüyü gösterir."""
    print("\n  MENÜ")
    print("  ─────────────────────────────")
    print("  [1] Yeni şifre analizi yap")
    print("  [2] Kural doğrulaması görüntüle")
    print("  [3] Oturum geçmişini görüntüle")
    print("  [4] Geçmiş özetini görüntüle")
    print("  [5] Geçmişi temizle")
    print("  [0] Çıkış")
    print("  ─────────────────────────────")


def get_password_input() -> str:
    """
    Kullanıcıdan şifre alır.
    Önce gizli giriş dener, başarısız olursa açık giriş kullanır.
    """
    try:
        pw = getpass.getpass("  Şifreyi girin (gizli): ")
    except Exception:
        # getpass desteklenmiyor olabilir (örn. bazı IDE'ler)
        pw = input("  Şifreyi girin: ")

    return pw.strip()


def validate_menu_choice(choice: str, valid_options: list[str]) -> bool:
    """Menü seçiminin geçerli olup olmadığını kontrol eder."""
    return choice in valid_options


# ─── Ana işlem fonksiyonları ─────────────────────────────────────────

def run_analysis(history: HistoryManager) -> None:
    """
    Şifre analizi yapar.
    StrengthAnalyzer (Polymorphism) ve HistoryManager kullanır.
    """
    try:
        password = get_password_input()

        if not password:
            print("\n  ⚠️  Şifre boş bırakılamaz!")
            return

        # Polymorphism: StrengthAnalyzer, PasswordAnalyzer'ı override eder
        analyzer = StrengthAnalyzer(password)
        analyzer.display_result()

        # Sonucu geçmişe kaydet
        result = analyzer.analyze()
        history.add_entry(result)
        print(f"\n  ✓ Analiz geçmişe eklendi. (Toplam: {history.entry_count})")

    except KeyboardInterrupt:
        print("\n\n  Analiz iptal edildi.")
    except ValueError as ve:
        print(f"\n  ⚠️  Değer hatası: {ve}")
    except Exception as e:
        print(f"\n  ⚠️  Beklenmedik hata: {e}")


def run_validation() -> None:
    """Kural tabanlı doğrulama yapar ve sonuçları gösterir."""
    try:
        password = get_password_input()

        if not password:
            print("\n  ⚠️  Şifre boş bırakılamaz!")
            return

        # Doğrulayıcıyı özel kurallarla oluştur
        validator = PasswordValidator(
            min_length=8,
            require_upper=True,
            require_lower=True,
            require_digit=True,
            require_special=True,
        )

        validator.display_validation(password)

        if validator.is_valid(password):
            print("\n  ✅ Şifre tüm kuralları karşılıyor!")
        else:
            print("\n  ❌ Şifre bazı kuralları karşılamıyor.")

    except KeyboardInterrupt:
        print("\n\n  Doğrulama iptal edildi.")
    except Exception as e:
        print(f"\n  ⚠️  Beklenmedik hata: {e}")


def show_summary(history: HistoryManager) -> None:
    """Oturum özetini gösterir."""
    summary = history.summary()

    if summary["total"] == 0:
        print("\n  Bu oturumda henüz analiz yapılmadı.")
        return

    print("\n" + "=" * 50)
    print("  📈 OTURUM ÖZETİ")
    print("=" * 50)
    print(f"  Toplam analiz   : {summary['total']}")
    print(f"  Ortalama skor   : {summary['avg_score']} / 5")
    print(f"  En iyi skor     : {summary['best_score']} / 5")
    print(f"  En düşük skor   : {summary['worst_score']} / 5")
    print("=" * 50)


# ─── Ana döngü ───────────────────────────────────────────────────────

def main() -> None:
    """
    Uygulamanın ana döngüsü.
    Menü yönetimi, kullanıcı girişi ve hata yönetimi burada sağlanır.
    """
    print_banner()

    # Geçmiş yöneticisini oluştur (oturum boyunca kullanılır)
    history = HistoryManager(max_size=50)

    valid_options = ["0", "1", "2", "3", "4", "5"]

    while True:
        try:
            print_menu()
            choice = input("  Seçiminiz: ").strip()

            if not validate_menu_choice(choice, valid_options):
                print("\n  ⚠️  Geçersiz seçim. Lütfen 0-5 arasında bir sayı girin.")
                continue

            if choice == "0":
                print("\n  Güvenli günler! 👋\n")
                sys.exit(0)

            elif choice == "1":
                run_analysis(history)

            elif choice == "2":
                run_validation()

            elif choice == "3":
                history.display_history()

            elif choice == "4":
                show_summary(history)

            elif choice == "5":
                confirm = input("\n  Geçmişi silmek istediğinizden emin misiniz? (e/h): ")
                if confirm.lower() == "e":
                    history.clear()
                    print("  ✓ Geçmiş temizlendi.")
                else:
                    print("  İptal edildi.")

        except KeyboardInterrupt:
            print("\n\n  Ctrl+C ile çıkıldı. Güvenli günler! 👋\n")
            sys.exit(0)
        except EOFError:
            # Pipe ile çalışıldığında oluşabilir
            sys.exit(0)
        except Exception as e:
            # Beklenmedik hatalar programı çökertmez
            print(f"\n  ⚠️  Beklenmedik hata: {e}")
            print("  Program devam ediyor...")


if __name__ == "__main__":
    main()
