# 🔐 Şifre Analiz Aracı

Python ile geliştirilmiş, OOP prensiplerini kullanan bir CLI şifre analiz uygulaması.

---

## 📁 Klasör Yapısı

```
sifre_analiz_araci/
├── main.py                    # Ana giriş noktası
├── README.md
├── src/
│   ├── __init__.py
│   ├── password_analyzer.py   # Soyut temel sınıf
│   ├── strength_analyzer.py   # Güç analizi (Kalıtım)
│   ├── password_validator.py  # Kural doğrulama
│   └── history_manager.py     # Geçmiş yönetimi
├── docs/
│   └── gereksinim_analizi.md  # Gereksinim dokümanı
├── tests/
│   └── test_all.py            # Birim testleri
└── output/                    # (Boş – çıktı dosyaları için)
```

---

## ▶️ Çalıştırma

```bash
python main.py
```

---

## 🧪 Testleri Çalıştırma

```bash
python -m pytest tests/ -v
# veya
python tests/test_all.py
```

---

## 🧱 OOP Prensipleri

| Prensip | Nerede |
|---------|--------|
| **Encapsulation** | Tüm sınıflarda `_private` alanlar + `@property` |
| **Inheritance** | `StrengthAnalyzer → PasswordAnalyzer` |
| **Polymorphism** | `analyze()` ve `display_result()` override |
| **Abstraction** | `PasswordAnalyzer` ABC soyut sınıf |

---

## ✅ Gereklilikler

- Python 3.10+
- Harici kütüphane gerekmez
