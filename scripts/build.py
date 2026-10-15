#!/usr/bin/env python3
"""Construye un portafolio estático con Python estándar, sin dependencias."""
import json
import os
import re
import shutil
from html import escape
from pathlib import Path
from urllib.parse import urlsplit
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
SOURCE = ROOT / 'site'
REPO = os.environ.get('GITHUB_REPOSITORY', 'Dzoro89/david-hernandez-ti')
owner, repository = REPO.split('/', 1)
BASE = os.environ.get('SITE_URL', f'https://{owner.lower()}.github.io/{repository}').rstrip('/')
GITHUB = f'https://github.com/{REPO}'
STATUS = {'en-desarrollo': ('En desarrollo', 'progress-badge'), 'planificado': ('Planificado', 'planned-badge'), 'completado': ('Completado', 'progress-badge')}

def text(value):
    return escape(str(value), quote=True)

def public_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f'El enlace público debe usar https: {value}')
    return text(value)

def evidence_url(value, prefix='../../'):
    if value.startswith('https://'):
        return public_url(value)
    if not value.startswith('assets/') or '..' in Path(value).parts or '?' in value or '#' in value:
        raise ValueError('Las evidencias locales deben estar en site/assets/.')
    if not (SOURCE / value).is_file():
        raise ValueError(f'Falta el archivo de evidencia: {value}')
    return text(prefix + value)

def badge(lab):
    label, css = STATUS[lab['status']]
    return f'<span class="badge {css}">{label}</span>'

def tags(lab):
    return ''.join(f'<span>{text(tool)}</span>' for tool in lab['tools'])

def render(template, values):
    result = template
    for key, value in values.items():
        result = result.replace('{{' + key + '}}', str(value))
    remaining = re.findall(r'\{\{[A-Z_]+\}\}', result)
    if remaining:
        raise ValueError(f'Variables sin resolver: {remaining}')
    return result

def write(path, value):
    destination = OUT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(value, encoding='utf-8')

def build():
    public_url(BASE)
    data = json.loads((ROOT / 'content/portfolio.json').read_text(encoding='utf-8'))
    labs = data['labs']
    slugs = set()
    for lab in labs:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', lab['slug']) or lab['slug'] in slugs:
            raise ValueError('Slug de laboratorio inválido o duplicado.')
        slugs.add(lab['slug'])
        if lab['status'] not in STATUS or lab['filter'] not in ('infraestructura', 'seguridad'):
            raise ValueError('Estado o categoría desconocidos.')
        if lab['status'] == 'completado' and not lab['evidence']:
            raise ValueError('Un laboratorio completado requiere evidencia pública.')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(SOURCE / 'assets', OUT / 'assets')
    for name in ('styles.css', 'app.js'):
        shutil.copyfile(SOURCE / name, OUT / name)
    cards = []
    template = (SOURCE / 'lab.html').read_text(encoding='utf-8')
    for lab in labs:
        slug = lab['slug']
        cards.append(f'''<article class="lab-card" data-category="{text(lab['filter'])}"><div class="lab-card-top"><span class="lab-id">{text(lab['id'])}</span>{badge(lab)}</div><p class="lab-area">{text(lab['area']).upper()}</p><h3>{text(lab['title'])}</h3><p>{text(lab['summary'])}</p><div class="tags">{tags(lab)}</div><a class="lab-card-link" href="laboratorios/{slug}/"><span>Ver ficha y plan de validación</span><span aria-hidden="true">↗</span><span class="sr-only">: {text(lab['title'])}</span></a></article>''')
        architecture = ''.join(f'<article class="architecture-node"><span>{index:02d}</span><h3>{text(node["name"])}</h3><p>{text(node["detail"])}</p></article>' for index, node in enumerate(lab['architecture'], 1))
        plan = ''.join(f'<li><h3>{text(step["title"])}</h3><p>{text(step["detail"])}</p><p class="validation-note"><strong>Evidencia prevista:</strong> {text(step["validation"])}</p></li>' for step in lab['plan'])
        if lab['evidence']:
            evidence = ''.join(f'<a class="evidence-item" href="{evidence_url(item["url"])}" target="_blank" rel="noopener noreferrer"><strong>{text(item["title"])} ↗</strong><p>{text(item["description"])}</p></a>' for item in lab['evidence'])
        else:
            evidence = '<div class="evidence-empty"><strong>Aún no hay evidencias de ejecución publicadas.</strong><p>Las capturas, bitácoras y resultados se incorporarán aquí conforme avance la práctica. El plan y la arquitectura son una propuesta de trabajo.</p></div>'
        values = {'BASE': text(BASE), 'TITLE': text(lab['title']), 'DESCRIPTION': text(lab['summary']), 'SLUG': slug, 'ID': text(lab['id']), 'AREA': text(lab['area']).upper(), 'SUMMARY': text(lab['summary']), 'TOOLS': tags(lab), 'BADGE': badge(lab), 'PROGRESS': text(lab['progress']), 'UPDATED': text(data['updated']), 'GITHUB': text(f'{GITHUB}/tree/main/laboratorios/{slug}'), 'CONTEXT': text(lab['context']), 'OBJECTIVE': text(lab['objective']), 'ARCHITECTURE': architecture, 'PLAN': plan, 'EVIDENCE': evidence, 'DELIVERABLES': ''.join(f'<li>{text(item)}</li>' for item in lab['deliverables'])}
        write(f'laboratorios/{slug}/index.html', render(template, values))
    credentials = data.get('credentials', [])
    credential_ids = set()
    credential_cards = []
    for item in credentials:
        if item['id'] in credential_ids or item['category'] not in ('seguridad', 'redes', 'mps', 'sistemas', 'datos', 'gestion'):
            raise ValueError('Credencial duplicada o categoría desconocida.')
        credential_ids.add(item['id'])
        if item.get('public_file'):
            file_url = evidence_url(item['public_file'], prefix='../')
            action = f'<a href="{file_url}" target="_blank" rel="noopener noreferrer">Consultar constancia ↗<span class="sr-only">: {text(item["title"])}</span></a>'
        else:
            request_url = 'mailto:dave989172@gmail.com?subject=' + quote('Solicitud de constancia: ' + item['title'])
            action = f'<a href="{text(request_url)}">Solicitar constancia ↗<span class="sr-only">: {text(item["title"])}</span></a>'
        credential_cards.append(f'<article class="credential-card" data-category="{text(item["category"])}"><div class="credential-card-top"><span>{text(item["kind"])}</span><time>{text(item["year"])}</time></div><h2>{text(item["title"])}</h2><p class="credential-issuer">{text(item["issuer"])}</p><p>{text(item["description"])}</p><div class="credential-date">Fecha en la constancia: {text(item["issued"])}</div><div class="credential-actions">{action}</div></article>')
    featured = [item for item in credentials if item.get('featured')][:4]
    preview_links = ''.join(f'<a class="training-preview-link" href="formacion/"><span>{text(item["issuer"].split(" / ")[0])} · {text(item["year"])}</span><strong>{text(item["title"])} ↗</strong></a>' for item in featured)
    preview = f'<article class="documented-training"><span class="mini-label">FORMACIÓN TÉCNICA DOCUMENTADA</span><h3>{len(credentials)} actividades con constancia</h3><p>Seguridad, redes, plataformas MPS, sistemas, nube, datos y gestión.</p><div class="training-preview-list">{preview_links}</div><a class="button dark-button" href="formacion/">Explorar todas las constancias ↗</a></article>'
    publication_cards = []
    for item in data.get('publications', []):
        links = ''.join(f'<a href="{evidence_url(link["url"], prefix="")}" target="_blank" rel="noopener noreferrer">{text(link["label"])} ↗</a>' for link in item['links'])
        if item.get('document_available'):
            request_url = 'mailto:dave989172@gmail.com?subject=' + quote('Solicitud de reporte: ' + item['title'])
            links += f'<a href="{text(request_url)}">Solicitar reporte completo ↗</a>'
        authors = ' · '.join(text(author) for author in item['authors'])
        publication_cards.append(f'<article class="publication-card" id="{text(item["id"])}"><div class="publication-top"><span>{text(item["kind"])}</span><span>{text(item["year"])}</span></div><h3>{text(item["title"])}</h3><p class="publication-venue">{text(item["venue"])}</p><p>{text(item["summary"])}</p><details class="publication-authors"><summary>Consultar autoría y referencia <span aria-hidden="true">+</span></summary><p>{authors}</p><p>{text(item["reference"])}</p></details><div class="publication-links">{links}</div></article>')
    certifications = []
    for item in data['certifications']:
        certifications.append(f'<a class="credential-link" href="{public_url(item["verification_url"])}" target="_blank" rel="noopener noreferrer"><strong>{text(item["title"])} ↗</strong><span>{text(item["issuer"])} · {text(item["issued"])}</span></a>')
    cert_html = ''.join(certifications) or '<h3>Credenciales verificables</h3><p>Las certificaciones se publicarán con su nombre oficial, entidad emisora y enlace de validación.</p><div class="certification-note">SIN CREDENCIALES PUBLICADAS POR EL MOMENTO</div>'
    documents = []
    for item in data['documents']:
        documents.append(f'<a href="{evidence_url(item["url"], prefix="")}" target="_blank" rel="noopener noreferrer">{text(item["title"])} ↗</a>')
    docs_html = '<div class="published-documents">' + ''.join(documents) + '</div>' if documents else ''
    write('index.html', render((SOURCE / 'index.html').read_text(encoding='utf-8'), {'BASE': text(BASE), 'LAB_CARDS': ''.join(cards), 'CERTIFICATIONS': cert_html, 'CREDENTIAL_PREVIEW': preview, 'PUBLICATIONS': ''.join(publication_cards), 'DOCUMENTS': docs_html}))
    write('formacion/index.html', render((SOURCE / 'training.html').read_text(encoding='utf-8'), {'BASE': text(BASE), 'CREDENTIAL_COUNT': str(len(credentials)), 'CREDENTIAL_CARDS': ''.join(credential_cards), 'EXTRA_CERTIFICATIONS': ''.join(certifications)}))
    write('perfil/index.html', render((SOURCE / 'profile.html').read_text(encoding='utf-8'), {'BASE': text(BASE), 'CREDENTIAL_COUNT': str(len(credentials))}))
    write('casos/hardening-multifuncionales/index.html', render((SOURCE / 'case-hardening.html').read_text(encoding='utf-8'), {'BASE': text(BASE)}))
    (OUT / 'downloads').mkdir()
    shutil.copyfile(ROOT / 'plantillas/laboratorio.md', OUT / 'downloads/plantilla-laboratorio.md')
    write('.nojekyll', '')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    urls = [BASE + '/', BASE + '/perfil/', BASE + '/formacion/', BASE + '/casos/hardening-multifuncionales/'] + [BASE + '/laboratorios/' + lab['slug'] + '/' for lab in labs]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{text(url)}</loc></url>' for url in urls) + '</urlset>\n')
    write('404.html', f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Página no encontrada | David Hernández</title><link rel="stylesheet" href="{text(BASE)}/styles.css"></head><body><main class="wrap section"><p class="eyebrow">404 / RUTA NO ENCONTRADA</p><h1>Volvamos al<br>portafolio.</h1><p>La dirección que abriste no está disponible.</p><a class="button dark-button" href="{text(BASE)}/">Ir al inicio ↗</a></main></body></html>')
    print(f'Sitio construido: {len(urls)} páginas principales en {OUT}')

if __name__ == '__main__':
    build()
