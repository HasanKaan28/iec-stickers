# IEC Sticker Seti

IUS Engineering Club için çizilmiş 101 özgün sticker. Site: https://hasankaan28.github.io/iec-stickers/

- Stickerları seç, adet ver.
- Site seçimi A4 kâğıda en az sayfa tutacak şekilde yerleştirir (MaxRects, gerekirse 90° döndürerek) ve stickerlar arasında makasla kesim payı bırakır.
- **Yazdır / PDF** ile doğrudan yazdır. Ölçek %100 (Gerçek boyut), kenar boşluğu Yok, kâğıt A4. Sayfanın altındaki 50 mm çizgiyle ölçüyü kontrol et.
- Seçim adres çubuğunda saklanır; **Seçim linkini kopyala** ile başkasına gönderebilirsin.

## Yeniden üretmek

```bash
python src/gen.py src/stickers.json   # stickerları yeniden çizer (isteğe bağlı)
python src/build_site.py .            # index.html'i üretir
```
