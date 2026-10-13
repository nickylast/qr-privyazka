#!/usr/bin/env python3
"""Сборка страницы из src/page.html.

index.html                  автономная страница: GitHub Pages и офлайн-файл (JSZip встроен)
dist/claude-artifact.html   версия для Claude: без оболочки документа, JSZip с CDN

Запуск: python3 build.py
"""
import pathlib

root = pathlib.Path(__file__).resolve().parent
page = (root / 'src' / 'page.html').read_text(encoding='utf-8')
lib = (root / 'vendor' / 'jszip.min.js').read_text(encoding='utf-8')
assert '</script' not in lib.lower(), 'JSZip нельзя встроить: в нём есть </script'

head, body = page.split('<!--HEAD-END-->', 1)
cdn = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>'
inline = '<script>/* JSZip 3.10.1, MIT license, https://stuk.github.io/jszip/ */\n' + lib + '\n</script>'

standalone = (
    '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="color-scheme" content="light dark">\n'
    '<meta name="description" content="Привязка QR-кодов экземпляров к шаблону «Состав грузомест»: '
    'сканирование, проверка дублей и количества, готовый файл для загрузки.">\n'
    + head.strip() + '\n</head>\n<body>\n' + body.replace('<!--JSZIP-->', inline).strip() + '\n</body>\n</html>\n'
)
artifact = head.strip() + '\n' + body.replace('<!--JSZIP-->', cdn).strip() + '\n'

(root / 'index.html').write_text(standalone, encoding='utf-8')
(root / 'dist').mkdir(exist_ok=True)
(root / 'dist' / 'claude-artifact.html').write_text(artifact, encoding='utf-8')
print(f'index.html: {len(standalone):,} символов; dist/claude-artifact.html: {len(artifact):,} символов')
