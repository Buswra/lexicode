# LexiCode — Kullanıcı Akışı (User Flow)

> Kullanıcı uygulamayı açtığında ne görür, ne yapar, sonuç ne olur? Adım adım:

---

## 1. Kurulum ve İlk Açılış

- Kullanıcı `LexiCode-Setup.exe` dosyasını çift tıklar.
- Kurulum sihirbazı açılır → "İleri → İleri → Kur" → masaüstüne kısayol oluşturulur.
- Kullanıcı masaüstündeki **LexiCode** ikonuna tıklar.
- Uygulama penceresi açılır, ana ekran yüklenir.

## 2. Ana Ekran — Mod Seçimi

- Ekranda iki ana mod butonu görünür: **🖥️ CS İngilizcesi** ve **💬 Günlük İngilizce**.
- Kullanıcı birini seçer.
- Alt kısımda kategori (chips) ve seviye (A1–C1) filtreleri belirir.
- *Erişilebilirlik paneli (♿)* ekranın köşesinde yer alır — yazı boyutu, satır aralığı, yüksek kontrast ayarları buradan yapılır.

## 3. Kelime Kartı İnceleme

- Ekranda bir **flashcard** görünür: kelimenin İngilizcesi, fonetik yazımı, emojisi ve örnek cümlesi.
- Kullanıcı kartı **tıklayarak çevirir** → Türkçe anlam ve ek bilgi gösterilir.
- 🔊 **Seslendir** butonuna basarak kelimeyi İngilizce veya Türkçe dinler.
- Ses ayarları: kadın/erkek ses, hız seçimi (Yavaş / Doğal / Akıcı).

## 4. Öğrendim veya Sonra

- Kullanıcı **"Öğrendim ✓"** butonuna basarsa: kelime öğrenildi olarak kaydedilir, XP kazanılır.
- **"Sonra →"** butonuna basarsa: kelime tekrar listesine eklenir.
- Ekrandaki ilerleme noktaları (dots) güncellenir, bir sonraki kart gösterilir.

## 5. Arama ve Sıralama

- Üst kısımdaki **arama kutusu**na kelime yazarak istediği kelimeye hızlıca ulaşır.
- **Sıralama** seçeneğiyle: alfabetik, seviyeye göre veya kategoriye göre listeyi düzenler.

## 6. Zihin Haritası

- Kullanıcı **Mindmap** sekmesine geçer.
- Kelimelerin birbiriyle ilişkileri görsel bir ağ yapısında gösterilir.
- Öğrenilen kelimeler yeşil, tekrar edilecekler turuncu, yeniler gri renkte kodlanır.

## 7. Quiz / Sınav

- Kullanıcı **Quiz** sekmesine geçer.
- 5 soruluk çoktan seçmeli bir sınav başlar.
- Her soru için **15 saniyelik zamanlayıcı** çalışır.
- Doğru yanaıtta ✅ geri bildirim + konfeti animasyonu, yanlışta ❌ ve doğru cevap gösterilir.
- Sınav bitiminde toplam skor, kazanılan XP ve performans özeti gösterilir.

## 8. AI Tutor ile Pratik

- Kullanıcı **AI Tutor** sekmesine geçer.
- Metin kutusuna kendi cümlesini yazar ve gönderir.
- AI üç modda yanıt verir:
  - **Düzelt:** Hatayı formülle (S+V+O) açıklar.
  - **Üret:** Kelimeyi CS bağlamında cümle içinde kullanır.
  - **Diyalog:** Kelime üzerinden mini konuşma simülasyonu yapar.

## 9. İlerleme Takibi

- Kullanıcı **Analytics** sekmesine geçer.
- Görünen bilgiler: toplam XP, günlük streak, mevcut seviye, en zor kelimeler.
- Kazanılan **rozetler** (11 farklı başarı) popup animasyonuyla gösterilir.
- **Öğrenme geçmişi** listesinden hangi kelimeyi ne zaman öğrendiğini görür.
- **CSV Dışa Aktar** butonuyla ilerleme verisini indirir.

---

## Özet Akış Diyagramı

```
Kur → Aç → Mod Seç → Kelime Kartı → Seslendir → Öğrendim/Sonra
                                                       ↓
                              Mindmap ← Quiz ← AI Tutor → Analytics
```