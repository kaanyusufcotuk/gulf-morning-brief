# Gulf Morning Brief: GitHub Pages sürümü

Sayfalar: `index.html` (canlı site) ve `edit.html` (editör). Veriler: `data.json` (yayındaki haberler + seçim) ve `candidates.json` (son aramanın sonuçları). Sayfa her açılışta `data.json`'u okur.

## İlk kurulum

1. github.com'da **New repository** → ad: `gulf-morning-brief`, **Public**.
2. Dosyaları yükle, **Commit changes**.
3. **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main`, klasör `/ (root)` → **Save**.
4. 1–2 dakika sonra site: `https://<kullanıcı-adın>.github.io/gulf-morning-brief/`

## GitHub erişim anahtarı (bir kez)

Editör, arama yapmak ve seçimleri yayınlamak için bir anahtar ister. Anahtar sadece o tarayıcıda saklanır.

1. https://github.com/settings/personal-access-tokens/new adresini aç.
2. **Repository access** → *Only select repositories* → `gulf-morning-brief`.
3. **Permissions** → **Actions: Read and write**, **Contents: Read and write**.
4. Oluşan `github_pat_…` anahtarını edit sayfasındaki kutuya yapıştırıp **Save**'e bas.

## Tarih seçip arama yapma

`edit.html` sayfasındaki **New search** kutusundan tarih aralığı seçip **Search**'e bas. Site, GitHub Actions üzerinde her ülke için Google News araması yapar (en fazla 14 gün, ~1 dakika). Sonuçlar `candidates.json`'a yazılır ve edit sayfasındaki listenin yerine geçer.

Anahtar olmadan da arama yapılabilir: depoda **Actions → Search news → Run workflow**, tarihleri gir. Bitince edit sayfasını yenile.

## Seçim yapma

Haberleri işaretle ya da işaretini kaldır. Her değişiklik birkaç saniye sonra otomatik olarak `data.json`'a commit edilir; canlı link yaklaşık bir dakika içinde güncellenir. Ayrı bir yükleme adımı yok.

Yeni aramanın sonuçlarında ilk haberi işaretlediğin anda canlı site o tarih aralığına geçer.

## inflow.bio linkleri

İşaretlenen her haberin altında bir **inflow.bio linki** kutusu çıkar:

1. **Copy original link** ile haberin orijinal linkini kopyala.
2. inflow.bio panelinde bu linkle yeni bir link oluştur.
3. Oluşan inflow.bio linkini kutuya yapıştır; kutudan çıkınca otomatik yayınlanır.

Canlı sitede o haber inflow.bio linkiyle açılır. Kutu boş kalırsa orijinal link kullanılır. inflow.bio'nun açık bir API'si olmadığı için bu adım elle yapılıyor.

## Günlük mesaj

Alttaki çubuktaki **Copy brief** düğmesi, işaretli haberlerden paylaşılmaya hazır mesajı panoya kopyalar: selamlama, tarih aralığı ("10-11 October"), sonra bayraklı ülke başlıkları altında `📌 başlık link` satırları. Ülke sırası: Suudi Arabistan, BAE, Katar, Umman, Kuveyt, Bahreyn, Irak; haberi seçilmemiş ülke atlanır. Her haberde inflow.bio linki varsa o, yoksa orijinal link kullanılır; kopyalarken kaç haberin inflow.bio linki eksik olduğu gösterilir.

## Notlar

- Siteyi yalnızca depoya yazma izni olan bir anahtarla değiştirmek mümkün. `edit.html` adresini bilen biri anahtar olmadan bir şey yayınlayamaz.
- Arama kodu: `scripts/search_news.py`, iş akışı: `.github/workflows/search.yml`.
- Link önizlemesi (WhatsApp, Slack) sabit başlığı gösterir: "Gulf Morning Brief". Haber sayısı yalnızca tarayıcı sekmesinde güncellenir.
- Sayfayı bilgisayarda çift tıklayıp açarsan `data.json` okunamaz. Yerelde denemek için klasörde `python3 -m http.server` çalıştırıp `http://localhost:8000` adresini aç.
