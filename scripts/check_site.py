#!/usr/bin/env python3
"""Verifica enlaces locales, anclas y recursos del sitio generado."""
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / '_site'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.errors = []
        self.has_title = False
        self.has_h1 = False
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'title':
            self.has_title = True
        if tag == 'h1':
            self.has_h1 = True
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f'ID duplicado: {attrs["id"]}')
            self.ids.add(attrs['id'])
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('Imagen sin texto alternativo.')
        if tag == 'a' and attrs.get('target') == '_blank' and 'noopener' not in attrs.get('rel', ''):
            self.errors.append('Enlace externo sin noopener.')

def check():
    pages = {}
    errors = []
    for path in ROOT.rglob('*.html'):
        source = path.read_text(encoding='utf-8')
        parser = Page()
        parser.feed(source)
        pages[path.resolve()] = parser
        if re.search(r'\{\{[A-Z_]+\}\}', source):
            errors.append(f'{path}: variable de plantilla pendiente.')
        if parser.lang != 'es' or not parser.has_title or not parser.has_h1:
            errors.append(f'{path}: falta idioma, título o encabezado principal.')
        errors.extend(f'{path}: {error}' for error in parser.errors)
    for path, page in pages.items():
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                if parts.scheme and parts.scheme not in ('https', 'mailto', 'data'):
                    errors.append(f'{path}: protocolo no permitido: {link}')
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not target.is_relative_to(ROOT.resolve()):
                errors.append(f'{path}: ruta fuera del sitio: {link}')
                continue
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{path}: recurso inexistente: {link}')
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f'{path}: ancla inexistente: {link}')
    if not (ROOT / 'assets/Perfil_David_Hernandez.pdf').read_bytes().startswith(b'%PDF-'):
        errors.append('El perfil descargable no es un PDF válido.')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Validación correcta: {len(pages)} páginas HTML; enlaces, anclas, recursos y PDF revisados.')

if __name__ == '__main__':
    check()
