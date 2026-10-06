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

## Yeni gün: yeni haberler

Yeni haber listesi `data.json` içindeki `stories` dizisine girer ve `selected` boşaltılır. Bu dosyayı hazırladığımda aynı şekilde depoya yüklersin.

## Notlar

- `#edit` adresi gizli değildir ama zararsızdır: sayfa depoyu değiştiremez, yalnızca seni yeni bir `data.json` indirmeye götürür. Siteyi yalnızca depoya commit atabilen kişi değiştirebilir.
- Link önizlemesi (WhatsApp, Slack) sabit başlığı gösterir: "Gulf Morning Brief". Haber sayısı yalnızca tarayıcı sekmesinde güncellenir.
- Sayfayı bilgisayarda çift tıklayıp açarsan `data.json` okunamaz. Yerelde denemek için klasörde `python3 -m http.server` çalıştırıp `http://localhost:8000` adresini aç.
