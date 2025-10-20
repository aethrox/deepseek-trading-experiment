# Trading Bot Glossary

## Trading Terms

**Backtest**  
Geçmiş verilerde stratejiyi test etme. Gerçek para kullanmadan "geçmişte ne olurdu?" sorusunu cevaplar.

**Signal**  
Alım/satım kararı. BUY (1), SELL (-1), HOLD (0).

**Position**  
Açık işlem. Position = 1 → Elinde BTC var, Position = 0 → Nakit.

**Entry Price**  
Alış fiyatı. BTC'yi kaça aldın.

**Exit Price**  
Satış fiyatı. BTC'yi kaça sattın.

**P&L (Profit & Loss)**  
Kar/Zarar. Exit - Entry fiyatı farkı.

**Paper Trading**  
Sanal para ile gerçek piyasada test. Risk yok.

---

## Technical Terms

**API (Application Programming Interface)**  
Programların birbirleriyle konuşma yolu. Bybit'ten veri çekmek için kullanılır.

**API Key**  
Şifre gibi. API'ye erişim için gerekli.

**Candle (Mum)**  
Belirli zaman dilimindeki fiyat hareketi. Open, High, Low, Close, Volume içerir.

**OHLCV**  
Open (Açılış), High (En yüksek), Low (En düşük), Close (Kapanış), Volume (Hacim).

**Interval**  
Mum aralığı. 60 = 1 saatlik mumlar.

---

## Strategy Terms

**Momentum**  
Fiyat yönünü takip etme. Yükseliyorsa al, düşüyorsa sat.

**Volatility**  
Fiyat dalgalanması. Yüksek volatilite = çok hareketli piyasa.

**Support/Resistance**  
Destek: Fiyatın düşmeyi durdurduğu seviye.  
Direnç: Fiyatın yükselmeyi durdurduğu seviye.

**Volume**  
İşlem hacmi. Kaç BTC alınıp satıldığı.

**Contrarian**  
Kalabalığın tersine işlem. Düşüşte al, yükselişte sat.

---

## AI/LLM Terms

**Prompt**  
LLM'e gönderdiğin soru/talimat.

**Temperature**  
Cevap çeşitliliği. 0.0 = her zaman aynı cevap, 1.0 = yaratıcı/rastgele.

**Token**  
Metin parçası. API maliyeti token sayısına göre hesaplanır.

**Completion**  
LLM'nin verdiği cevap.

---

## Code Terms

**DataFrame (df)**  
Pandas kütüphanesinde tablo yapısı. Excel gibi.

**CSV**  
Virgülle ayrılmış dosya formatı. Veri saklamak için kullanılır.

**Loop (for/while)**  
Tekrarlayan işlem. Her saati teker teker test etmek için.

**Try/Except**  
Hata yakalama. API hatası olursa program çökmesin diye.

---

## Risk Terms

**Capital**  
Sermaye. Başlangıç paran.

**Drawdown**  
En büyük düşüş. Sermayenin en çok ne kadar eridiği.

**Win Rate**  
Kazanan işlem yüzdesi. 5/10 işlem kazandıysa %50.

**Risk/Reward**  
Risk-getiri oranı. Ne kadar risk alıp ne kadar kazanç hedefliyorsun.