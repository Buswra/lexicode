# LexiCode — Görev Listesi (tasks.md)

> `prd.md` dosyasına bakılarak uygulama adım adım geliştirmek için oluşturulmuş görev listesidir.
> Cursor Agent modunda kullanım: *"tasks.md dosyasındaki görevlere bakarak birinci görevden başla."*

---

## Temel Geliştirme Görevleri

### ✅ Görev 1: Proje yapısını oluştur, Flask backend'i kur
- [x] Flask uygulaması (`features/app.py`), config dosyası, SQLite şeması
- [x] API endpoint'leri: `/api/health`, `/api/words`, `/api/stats`
- [x] Kelime veritabanları: `words.py` (günlük), `words_cs.py` (CS)
- [x] Test altyapısı: `features/tests/test_api.py`

### ✅ Görev 2: Kelime kartları ekranını oluştur (Flashcards UI)
- [x] Kart ön yüz: kelime, fonetik, emoji, örnek cümle
- [x] Kart çevirme animasyonu → arka yüz: Türkçe anlam
- [x] Kategori/seviye filtreleme, CS/Günlük mod seçimi
- [x] "Öğrendim" / "Sonra" butonları ve ilerleme noktaları

### ✅ Görev 3: Seslendirme (TTS) sistemini entegre et
- [x] edge-tts ile İngilizce/Türkçe neural ses desteği
- [x] Kadın/Erkek ses ve hız ayarı (Yavaş/Doğal/Akıcı)
- [x] Tarayıcı speechSynthesis fallback

### ✅ Görev 4: Quiz/Sınav sistemini yap
- [x] 5 soruluk çoktan seçmeli quiz, skor ve XP hesaplama
- [x] Doğru/yanlış geri bildirimi ve sonuç ekranı
- [x] 15 saniyelik zamanlayıcı ve konfeti animasyonu

### ✅ Görev 5: AI Tutor (Claude API) entegrasyonunu kur
- [x] Cümle düzeltme, örnek üretme, mini diyalog endpoint'leri
- [x] API anahtarı yoksa güvenli fallback mekanizması

### ✅ Görev 6: Zihin Haritası (Mindmap) ekranını oluştur
- [x] Kelimeleri kategoriye göre grid'de göster
- [x] Kelime ilişkileri ve öğrenme durumu renklendirmesi

### ✅ Görev 7: İlerleme ve rozet sistemini ekle
- [x] XP, streak, seviye sistemi (A1→C1)
- [x] 11 farklı rozet ve popup animasyonu
- [x] Analitik ekranı, günlük hedef ayarlama

### ✅ Görev 8: Masaüstü uygulamasına (PySide6) dönüştür
- [x] PySide6 + QtWebEngine shell, Flask thread'de çalışır
- [x] Otomatik boş port bulma, pencere boyutu/başlık ayarı

### ✅ Görev 9: EXE olarak paketle ve installer oluştur
- [x] PyInstaller ile EXE üretimi (`LexiCode.spec`)
- [x] Inno Setup ile tek tık kurulum (`LexiCode-Setup.exe`)
- [x] Masaüstü kısayolu ve Başlat menüsü girişi

### ✅ Görev 10: UI/UX ve erişilebilirlik iyileştirmeleri
- [x] Kelime arama kutusu ve sıralama seçenekleri
- [x] Öğrenme geçmişi ekranı ve CSV dışa aktarma
- [x] Yükleniyor animasyonu (spinner)
- [x] Tema geçişine yumuşak animasyon
- [x] Yazı boyutu, satır aralığı, yüksek kontrast ayarları (erişilebilirlik paneli ♿)

### ✅ Görev 11: Uygulama ikonu tasarla ve ekle
- [x] Projeye özgü ikon oluşturma (`assets/lexicode.ico`)
- [x] PyInstaller ve Inno Setup'a ikon entegrasyonu

---

## 🔄 Gelecek İterasyon Fikirleri

- [ ] Kart çevirme animasyonuna 3D derinlik efekti ekle
- [ ] Öğrenilen kelimelerde yeşil tik ikonu göster
- [ ] Mobil görünümü düzelt, dar ekranda kartlar taşmasın
- [ ] Heceleri renkli gösterme özelliğini aç/kapat yapılabilir yap
