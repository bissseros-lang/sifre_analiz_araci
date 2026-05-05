# Gereksinim Analizi Dokümanı
## Şifre Analiz Aracı — v1.0

---

## 1. Proje Özeti

Bu proje, kullanıcıların girdikleri şifreleri güç, kural uyumu ve örüntü açısından analiz etmelerine olanak tanıyan bir komut satırı (CLI) uygulamasıdır. Python dili ile nesne yönelimli programlama (OOP) prensipleri kullanılarak geliştirilmiştir.

---

## 2. Paydaşlar

| Paydaş | Rolü |
|--------|------|
| Son kullanıcı | Şifre analizi yapmak isteyen bireyler |
| Geliştirici | Uygulamayı tasarlayan ve kodlayan kişi |

---

## 3. İşlevsel Gereksinimler

| No | Gereksinim | Öncelik |
|----|-----------|---------|
| FR-01 | Kullanıcı şifresini gizli (masked) olarak girebilmeli | Yüksek |
| FR-02 | Sistem şifrenin uzunluğunu, karakter çeşitliliğini analiz etmeli | Yüksek |
| FR-03 | Sistem Shannon entropisi hesaplamalı | Orta |
| FR-04 | Sistem tekrarlayan, ardışık ve klavye örüntülerini tespit etmeli | Orta |
| FR-05 | Sistem 0-5 arası güç skoru ve güç etiketi üretmeli | Yüksek |
| FR-06 | Kural tabanlı doğrulama (min uzunluk, büyük harf, rakam vb.) yapılabilmeli | Yüksek |
| FR-07 | Analiz geçmişi oturum boyunca saklanabilmeli | Düşük |
| FR-08 | Oturum özet istatistikleri görüntülenebilmeli | Düşük |
| FR-09 | Kullanıcıya iyileştirme önerileri sunulmalı | Orta |

---

## 4. İşlevsel Olmayan Gereksinimler

| No | Gereksinim |
|----|-----------|
| NFR-01 | Uygulama Python 3.10+ ile çalışmalı |
| NFR-02 | Harici kütüphane bağımlılığı olmamalı (yalnızca standart kütüphane) |
| NFR-03 | Her modül 1000 satırı aşmamalı |
| NFR-04 | Tüm public metotlar docstring içermeli |
| NFR-05 | Kullanıcı hataları try-catch ile yönetilmeli |

---

## 5. OOP Tasarım Kararları

### 5.1 Sınıf Hiyerarşisi

```
PasswordAnalyzer  (soyut temel sınıf — ABC)
    └── StrengthAnalyzer  (somut alt sınıf — Kalıtım)

PasswordValidator  (bağımsız sınıf — kural motoru)
HistoryManager     (bağımsız sınıf — geçmiş yönetimi)
```

### 5.2 OOP Prensiplerinin Uygulanması

| Prensip | Nasıl uygulandı |
|---------|----------------|
| **Encapsulation** | Tüm iç alanlar `_private` olarak tanımlandı; dış erişim `@property` ile sağlandı |
| **Inheritance** | `StrengthAnalyzer`, `PasswordAnalyzer`'dan türetildi |
| **Polymorphism** | `analyze()` ve `display_result()` alt sınıfta override edildi |
| **Abstraction** | `PasswordAnalyzer` ABC olarak tanımlandı; `analyze()` ve `display_result()` soyut metot |

---

## 6. Hata Yönetimi Stratejisi

- Kullanıcı boş şifre girerse uyarı mesajı gösterilir, program çökmez.
- Geçersiz menü seçimlerinde yeniden giriş istenir.
- `KeyboardInterrupt` (Ctrl+C) yakalanır, temiz çıkış sağlanır.
- `HistoryManager.add_entry()` yanlış tip veri gelirse `TypeError` fırlatır.
- `PasswordValidator.check_rule()` bilinmeyen kural adında `ValueError` fırlatır.
- Regex hataları `check_patterns()` içinde sessizce atlanır.

---

## 7. Modül Açıklamaları

| Dosya | İçerik |
|-------|--------|
| `src/password_analyzer.py` | Soyut temel sınıf |
| `src/strength_analyzer.py` | Güç analizi (kalıtım, polymorphism) |
| `src/password_validator.py` | Kural tabanlı doğrulama |
| `src/history_manager.py` | Oturum geçmiş yönetimi |
| `main.py` | CLI giriş noktası |
| `tests/test_all.py` | Birim testleri |

---

## 8. Git Commit Planı (Örnek)

| # | Commit Mesajı |
|---|--------------|
| 1 | `init: proje klasör yapısı ve boş dosyalar oluşturuldu` |
| 2 | `feat: PasswordAnalyzer soyut sınıfı eklendi` |
| 3 | `feat: StrengthAnalyzer ve PasswordValidator eklendi` |
| 4 | `feat: HistoryManager ve main.py CLI döngüsü eklendi` |
| 5 | `test: birim testleri eklendi` |
| 6 | `docs: gereksinim analizi ve README eklendi` |

---


