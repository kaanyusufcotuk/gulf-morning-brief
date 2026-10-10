# Gulf Morning Brief: GitHub Pages sürümü

İki dosya: `index.html` (sayfa) ve `data.json` (haberler + seçim). Sayfa her açılışta `data.json`'u okur.

## İlk kurulum

1. github.com'da **New repository** → ad: `gulf-morning-brief`, **Public**.
2. **Add file → Upload files** ile `index.html` ve `data.json`'u yükle, **Commit changes**.
3. **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main`, klasör `/ (root)` → **Save**.
4. 1–2 dakika sonra site: `https://<kullanıcı-adın>.github.io/gulf-morning-brief/`

## Her gün: seçim yapıp yayınlama

1. `https://<kullanıcı-adın>.github.io/gulf-morning-brief/#edit` adresini aç (editör görünümü).
2. İstediğin haberleri işaretle. İşaretler bu tarayıcıda taslak olarak saklanır.
3. **Download data.json**'a bas.
4. Depoda **Add file → Upload files** ile indirilen `data.json`'u yükle (aynı adlı dosyanın üzerine yazar), **Commit changes**.
5. 1–2 dakika sonra herkes yeni seçimi görür (sayfayı yenilemek gerekebilir).

## Yeni gün: tarih seçip arama yapma

Edit sayfasındaki **New search** kutusundan tarih aralığı seçip **Search**'e basınca site, GitHub Actions üzerinde her ülke için Google News araması yapar (en fazla 14 gün, ~1 dakika). Sonuçlar `candidates.json` dosyasına yazılır ve edit sayfasındaki listenin yerine geçer. Canlı site, yeni `data.json`'u yükleyene kadar eski seçimi göstermeye devam eder.

İlk seferde sayfa bir **GitHub erişim anahtarı** ister (anahtar sadece o tarayıcıda saklanır):

1. https://github.com/settings/personal-access-tokens/new adresini aç.
2. **Repository access** → *Only select repositories* → `gulf-morning-brief`.
3. **Permissions** → **Actions: Read and write**, **Contents: Read**.
4. Oluşan `github_pat_…` anahtarını edit sayfasındaki kutuya yapıştırıp **Save**'e bas.

Anahtar olmadan da arama yapılabilir: depoda **Actions → Search news → Run workflow**, tarihleri gir. Bitince edit sayfasını yenile.

Arama kodu: `scripts/search_news.py`, iş akışı: `.github/workflows/search.yml`.

## Notlar

- `#edit` adresi gizli değildir ama zararsızdır: sayfa depoyu değiştiremez, yalnızca seni yeni bir `data.json` indirmeye götürür. Siteyi yalnızca depoya commit atabilen kişi değiştirebilir.
- Link önizlemesi (WhatsApp, Slack) sabit başlığı gösterir: "Gulf Morning Brief". Haber sayısı yalnızca tarayıcı sekmesinde güncellenir.
- Sayfayı bilgisayarda çift tıklayıp açarsan `data.json` okunamaz. Yerelde denemek için klasörde `python3 -m http.server` çalıştırıp `http://localhost:8000` adresini aç.
