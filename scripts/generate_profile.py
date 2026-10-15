#!/usr/bin/env python3
"""Regenera el perfil público descargable. Requiere reportlab (solo autoría)."""
from html import escape
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'site/assets/Perfil_David_Hernandez.pdf'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DejaVu', str(FONT_DIR / 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', str(FONT_DIR / 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold')
INK = colors.HexColor('#173337')
MUTED = colors.HexColor('#596b65')
LINE = colors.HexColor('#cdd8cd')
MINT = colors.HexColor('#c5e6c9')
PAPER = colors.HexColor('#f9faf5')
WIDTH, HEIGHT = A4
LEFT = 39
RIGHT_X = 389
LEFT_WIDTH = 320
RIGHT_WIDTH = WIDTH - RIGHT_X - LEFT

c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle('David Hernández Trinidad - Perfil profesional')
c.setAuthor('David Hernández Trinidad')
c.setSubject('Liderazgo TI, infraestructura, seguridad de la información y MPS')

def paragraph(value, x, y, width, size=9, leading=13, color=MUTED, space=8, bold=False):
    style = ParagraphStyle('body', fontName='DejaVu-Bold' if bold else 'DejaVu', fontSize=size,
                           leading=leading, textColor=color, alignment=TA_LEFT)
    p = Paragraph(value, style)
    _, height = p.wrap(width, 1000)
    if y - height < 47:
        raise ValueError(f'Contenido fuera del área de lectura: {value[:80]}')
    p.drawOn(c, x, y - height)
    return y - height - space

def heading(label, x, y, width):
    c.setStrokeColor(LINE)
    c.setLineWidth(.5)
    c.line(x, y, x + width, y)
    return paragraph(escape(label), x, y-12, width, 7.4, 10, INK, 11, True)

def bullet(value, x, y, width):
    c.setFillColor(colors.HexColor('#719063'))
    c.circle(x+2, y-5, 1.5, fill=1, stroke=0)
    return paragraph(value, x+12, y, width-12, 8.6, 12.4, MUTED, 7)

c.setFillColor(PAPER)
c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
c.setFillColor(INK)
c.rect(0, HEIGHT-118, WIDTH, 118, fill=1, stroke=0)
c.setFillColor(MINT)
c.setFont('DejaVu', 7.5)
c.drawString(LEFT, HEIGHT-31, 'PERFIL PROFESIONAL / EXPERIENCIA TÉCNICA Y VISIÓN DE NEGOCIO')
c.setFillColor(colors.white)
c.setFont('DejaVu-Bold', 23)
c.drawString(LEFT, HEIGHT-65, 'David Hernández Trinidad')
c.setFont('DejaVu', 9.2)
c.setFillColor(MINT)
c.drawString(LEFT, HEIGHT-87, 'Liderazgo TI | Infraestructura | Seguridad de la información | MPS')
c.setFont('DejaVu', 8)
c.drawString(LEFT, HEIGHT-104, 'Estado de México / CDMX  |  dave989172@gmail.com')
c.linkURL('mailto:dave989172@gmail.com', (LEFT+174, HEIGHT-109, LEFT+330, HEIGHT-98), relative=0)

y = paragraph('Profesional con <b>12 años de trayectoria en TI</b> y alrededor de <b>5 años acumulados en funciones de ciberseguridad</b>. Experiencia en infraestructura, accesos, vulnerabilidades, monitoreo y continuidad. Coordino equipos y proveedores para conectar controles técnicos con la operación del servicio.', LEFT, HEIGHT-137, WIDTH-2*LEFT, 9.5, 14, MUTED, 20)
metric_y = y
metrics = [('25+', 'servidores Windows/Linux', 'unas 15 cuentas empresariales'),
           ('132+', 'clientes corporativos', 'alcance del servicio coordinado'),
           ('12 años', 'de trayectoria en TI', 'Alldora: junio 2014 - agosto 2026')]
col_width = (WIDTH - 2*LEFT) / 3
for index, (value, label, context) in enumerate(metrics):
    x = LEFT + index * col_width
    c.setFillColor(INK)
    c.setFont('DejaVu', 23)
    c.drawString(x, metric_y-21, value)
    c.setFont('DejaVu-Bold', 7.6)
    c.drawString(x, metric_y-37, label)
    c.setFont('DejaVu', 6.5)
    c.setFillColor(MUTED)
    c.drawString(x, metric_y-50, context)

body_y = metric_y - 75
y_left = heading('EXPERIENCIA PROFESIONAL', LEFT, body_y, LEFT_WIDTH)
y_left = paragraph('Alldora Latinoamérica', LEFT, y_left, LEFT_WIDTH, 12, 16, INK, 3, True)
y_left = paragraph('Junio 2014 - Agosto 2026', LEFT, y_left, LEFT_WIDTH, 7.6, 11, MUTED, 5)
y_left = paragraph('Líder de Soluciones MPS. Evolución desde soporte técnico hacia coordinación y liderazgo de soluciones, operación y servicios.', LEFT, y_left, LEFT_WIDTH, 8.8, 12.8, INK, 11)
for item in [
    'Administración y soporte de más de 25 servidores Windows/Linux: virtualización, respaldos, actualizaciones y conectividad.',
    'Identidades, usuarios, grupos y permisos en Active Directory y Microsoft Entra ID; validaciones de autenticación y accesos.',
    'Hardening, parchado, vulnerabilidades y certificados TLS/SSL; coordinación de remediaciones con redes y fabricantes.',
    'Apoyo al monitoreo y análisis de eventos con Wazuh, Splunk y CrowdStrike Falcon; atención y seguimiento de incidentes.',
    'Coordinación de equipos y proveedores, ventanas de cambio, recuperación, pruebas y documentación de resultados.',
    'Pruebas de concepto, despliegues y soporte MPS: nddPrint, Lexmark CPM/CFM, PaperCut y Xerox Workplace Cloud.',
    'PowerShell, Python y Bash para apoyar validaciones, administración y automatización operativa.'
]:
    y_left = bullet(item, LEFT, y_left, LEFT_WIDTH)
y_left = heading('INDICADORES DE LA OPERACIÓN', LEFT, y_left-6, LEFT_WIDTH)
for item in [
    '<b>≈95%</b> de cobertura de monitoreo de la base instalada.',
    '<b>&gt;91%</b> de cumplimiento promedio mensual de SLA.',
    '<b>99%</b> de primeras respuestas dentro del objetivo.'
]:
    y_left = bullet(item, LEFT, y_left, LEFT_WIDTH)
y_left = paragraph('Indicadores operativos de servicio y atención; el monitoreo corresponde a la base instalada.', LEFT, y_left, LEFT_WIDTH, 7, 10, MUTED, 0)

y_right = heading('FORMACIÓN / UNITEC', RIGHT_X, body_y, RIGHT_WIDTH)
y_right = paragraph('Maestría en Seguridad de Tecnologías de la Información', RIGHT_X, y_right, RIGHT_WIDTH, 9.1, 13, INK, 5, True)
y_right = paragraph('2020-2023<br/>Estudios concluidos.<br/>Titulación en proceso.', RIGHT_X, y_right, RIGHT_WIDTH, 8, 11.5, MUTED, 13)
y_right = paragraph('Ingeniería en Sistemas Computacionales', RIGHT_X, y_right, RIGHT_WIDTH, 9.1, 13, INK, 5, True)
y_right = paragraph('2017-2020<br/>Estudios concluidos.<br/>Titulación en proceso.', RIGHT_X, y_right, RIGHT_WIDTH, 8, 11.5, MUTED, 16)
y_right = heading('HERRAMIENTAS Y PRÁCTICAS', RIGHT_X, y_right, RIGHT_WIDTH)
for item in [
    '<b>Virtualización e identidad:</b> VMware, Hyper-V, Active Directory, Entra ID y Microsoft 365.',
    '<b>Seguridad:</b> Wazuh, Splunk, CrowdStrike Falcon, CVE/CVSS y TLS/SSL.',
    '<b>Gestión y automatización:</b> Freshservice, PowerShell, Python, Bash y SLA/KPI.',
    '<b>Marcos:</b> ISO/IEC 27001, NIST CSF, MITRE ATT&amp;CK, ITIL y Scrum.'
]:
    y_right = paragraph(item, RIGHT_X, y_right, RIGHT_WIDTH, 7.7, 11.2, MUTED, 8)
y_right = heading('FORMACIÓN COMPLEMENTARIA', RIGHT_X, y_right-3, RIGHT_WIDTH)
y_right = paragraph('Redes, ciberseguridad, liderazgo y soluciones MPS. Cursos detallados en el portafolio; constancias pendientes de incorporar.', RIGHT_X, y_right, RIGHT_WIDTH, 7.7, 11.2, MUTED, 13)
y_right = heading('IDIOMAS', RIGHT_X, y_right, RIGHT_WIDTH)
y_right = paragraph('Español nativo.<br/>Inglés intermedio, con lectura técnica avanzada.', RIGHT_X, y_right, RIGHT_WIDTH, 7.7, 11.2, MUTED, 0)

if min(y_left, y_right) < 47:
    raise ValueError('La composición rebasa el margen inferior.')
c.setStrokeColor(LINE)
c.line(LEFT, 37, WIDTH-LEFT, 37)
c.setFont('DejaVu', 6.7)
c.setFillColor(INK)
c.drawString(LEFT, 24, 'linkedin.com/in/dhernandez89')
c.linkURL('https://www.linkedin.com/in/dhernandez89/', (LEFT, 19, LEFT+160, 31), relative=0)
url = 'https://dzoro89.github.io/david-hernandez-ti/'
c.drawRightString(WIDTH-LEFT, 24, url)
c.linkURL(url, (WIDTH-LEFT-222, 19, WIDTH-LEFT, 31), relative=0)
c.showPage()
c.save()
print(f'Perfil PDF creado: {OUTPUT}; márgenes inferiores de columnas: {y_left:.1f}, {y_right:.1f} pt')
