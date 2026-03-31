# LexiCode – Proje Fikri ve Analizi

## Problem: Ne çözüyorum?

Geleneksel İngilizce öğrenme uygulamaları genel kitleye hitap eder ve genellikle ezbere dayalı, metin yoğunluklu arayüzlere sahiptir. Bu durum, özellikle **disleksili bireyler** için öğrenme sürecini ciddi oranda zorlaştırır. Mevcut platformlarda:

- Disleksi dostu yazı tipi, satır aralığı, kontrast gibi erişilebilirlik seçenekleri yoktur.
- Bilişim teknolojileri (CS) alanına özgü mesleki İngilizce terminolojisine odaklanan bir müfredat bulunmaz.
- Yapay zeka destekli, cesaretlendirici ve yargılamayan bir geri bildirim mekanizması eksiktir.

## Kullanıcı: Bu uygulamayı kim kullanacak?

- **Disleksili bireyler:** İngilizce öğrenirken okuma ve anlama güçlüğü yaşayan, erişilebilir bir arayüze ihtiyaç duyan kişiler.
- **CS öğrencileri ve yazılımcılar:** Mesleki İngilizcesini (API, Recursion, Polymorphism vb.) geliştirmek isteyen bilgisayar bilimleri öğrencileri ve teknoloji profesyonelleri.
- **Genel öğrenciler:** Günlük İngilizceyi kalıp cümleler ve bağlam içinde öğrenmek isteyenler.

## AI'ın Rolü: Yapay zeka bu çözümde ne yapıyor?

Projede yapay zeka (Claude API), klasik bir chatbot gibi değil, **"cesaretlendirici ve disleksi dostu bir İngilizce öğretmeni"** rolünü üstlenir:

1. **Hata Ayıklama (Correction):** Kullanıcının kurduğu cümleleri yargılamadan inceler, hataları açıklar ve basit yapısal formüller (S+V+O) ile düzeltir.
2. **Bağlam Üretimi (Generation):** Öğrenilen CS veya günlük kelimeleri doğrudan sektörel bağlamda (yazılım geliştirme süreçleri gibi) cümle içinde örneklendirir.
3. **Etkileşim (Dialog):** Kullanıcıyla o kelime üzerinden kısa ve motive edici mini diyaloglar kurarak pratik yapma imkânı sağlar.
4. **Güvenli Çalışma:** API anahtarı olmadığında uygulama çökme yerine zarif bir fallback mesajı döndürür; kullanıcı deneyimi kesintisiz devam eder.

## Rakip Durum: Benzer çözümler var mı? Benimki nasıl farklı?

| Rakip | Güçlü Yönü | Eksik Yönü |
|---|---|---|
| **Duolingo / Memrise** | Oyunlaştırma, geniş dil desteği | Disleksiye özel UX yok, CS terminolojisi yok |
| **Quizlet** | Flaş kart tabanlı ezber | AI diyalogu yok, zihin haritası yok |
| **Notion AI** | Genel metin üretimi | Ders/kelime odaklı soru üretimi yok |

**LexiCode'un farkı:**
- Kelimeleri **Zihin Haritası (Mindmap)** ile görselleştirir.
- Sadece **"Yazılım/CS"** ve **"Günlük"** olmak üzere iki net kategoriye odaklanır.
- AI geri bildirimlerini disleksili bireylerin motivasyonunu yüksek tutacak şekilde **özel bir tonda** (prompt engineering ile) sunar.
- **Erişilebilirlik paneli:** Yazı boyutu, satır aralığı, yüksek kontrast modu — tek tıkla.
- **Tek EXE kurulum:** Kullanıcı hiçbir teknik bilgiye ihtiyaç duymadan Windows'ta kurar, çalıştırır.

## Başarı Kriteri: Bu proje başarılı olursa ne değişecek?

- Bir kullanıcı, klasik yöntemlerle ezberlemekte zorlandığı teknik bir yazılım terimini (örn: *Recursion*, *Polymorphism*), LexiCode üzerinden görsel olarak bağdaştırır.
- AI Tutor ile pratik yaparak kelimeyi cümlede kullanabilir hale gelir.
- Bu kelimeyi bir dokümantasyonda okuduğunda anlamını hatırlayabilir.
- Disleksili bir öğrenci, uygulamayı **30 saniye içinde kurup** erişilebilirlik ayarlarını kişiselleştirerek rahatça kullanmaya başlar.

---

## 🌍 Anlamlı Problem Önerileri

| Alan | Örnek Fikirler |
|---|---|
| **Eğitim** | Öğrencilere kişiselleştirilmiş ödev yardımı, dil öğrenimi, soru üretici |
| **Sağlık** | Semptom takibi, ilaç hatırlatıcı, sağlıklı tarif önerisi |
| **Çevre** | Karbon ayak izi hesaplama, geri dönüşüm rehberi |
| **Toplum** | Yaşlılar için teknoloji yardımcısı, engelli erişimi desteği |
| **Verimlilik** | QR kartvizit, not özetleyici, toplantı asistanı, CV analizi |

> **LexiCode** bu tabloda **Eğitim** ve **Toplum** (engelli erişimi desteği) kategorilerinin kesişiminde yer alır.