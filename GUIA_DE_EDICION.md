# Guía para mantener tu portafolio

## Edición desde GitHub
Abre el archivo, pulsa el lápiz, edita y guarda con **Commit changes** en `main`. La publicación automática se ve en **Actions**. La primera vez puede ser necesario seleccionar **Settings → Pages → Source → GitHub Actions**.

## Completar un laboratorio
1. Documenta el trabajo real en `laboratorios/<slug>/README.md`. Puedes partir de `plantillas/laboratorio.md`.
2. Sube capturas o reportes públicos a `site/assets/evidencias/<slug>/` con **Add file → Upload files**.
3. Edita su entrada en `content/portfolio.json`: actualiza `progress` y añade enlaces en `evidence`.

Ejemplo de evidencia (requiere que el archivo ya exista):

```json
"evidence": [
  {
    "title": "Validación de la política en el cliente",
    "description": "Comprobación de la GPO aplicada en el entorno de prueba.",
    "url": "assets/evidencias/active-directory-gpo/validacion.png"
  }
]
```

El sitio admite archivos públicos locales bajo `site/assets/` o enlaces HTTPS. Las fichas enlazan a la documentación original en GitHub.

Estados admitidos: `planificado`, `en-desarrollo`, `completado`. Marca completado solo después de comprobar el resultado y publicar la evidencia. El constructor rechaza prácticas completadas sin evidencia.

## Añadir un laboratorio
Duplica un objeto de `labs`, usa un `slug` único en minúsculas y guiones, define un ID, objetivo, arquitectura, plan, estado y entregables. Crea también `laboratorios/<slug>/README.md`. El constructor crea la tarjeta y la página de detalle automáticamente.

Los filtros admitidos son `infraestructura` y `seguridad`. Mantén la sintaxis JSON, sin comentarios ni comas al final.

## Añadir una certificación profesional
Añade a `certifications` únicamente credenciales obtenidas con enlace público del emisor:

```json
{"title": "Nombre oficial", "issuer": "Entidad emisora", "issued": "Año de emisión", "verification_url": "https://enlace-del-emisor.example/credencial"}
```

Este es un ejemplo de estructura, no una credencial real. Los estudios y cursos sin certificación profesional se editan en Formación, dentro de `site/index.html` y `site/profile.html`.

## Añadir documentos
Consulta `documentos/README.md`. No publiques identificaciones, documentos familiares, salarios ni información de clientes. Usa versiones públicas de los reportes y conserva los originales completos para compartirlos de forma privada cuando corresponda.

## Actualizar el perfil
La experiencia aparece en `site/index.html` y `site/profile.html`. Si cambias datos de trayectoria, revisa ambos y sustituye el PDF cuando corresponda.

## Completar un caso profesional
La ficha de hardening de multifuncionales está en `site/case-hardening.html` y se publica en `/casos/hardening-multifuncionales/`. Sus accesos aparecen en la portada y en el perfil para RH.

Para ampliar el caso, añade el contexto, tu participación, un hallazgo concreto, el cambio aplicado y cómo se validó. Mantén los resultados y métricas vinculados a información que puedas respaldar. La ficha reserva un apartado para futuras evidencias públicas; retira nombres de clientes, direcciones, credenciales y datos internos antes de preparar una versión para publicar. Las referencias técnicas no acreditan por sí mismas la ejecución de todas las recomendaciones de una guía.

## Estructura de publicación
`scripts/build.py` combina las plantillas y los datos, y genera `_site/`. `scripts/check_site.py` comprueba rutas, anclas y variables sin resolver. El flujo `.github/workflows/pages.yml` construye y publica automáticamente. No edites `_site/`: se genera de nuevo en cada publicación.

## Regenerar el perfil PDF
El resumen público tiene su fuente en `scripts/generate_profile.py`. Para regenerarlo se necesita ReportLab y las fuentes DejaVu Sans. Esto solo afecta a la autoría del PDF: el sitio publicado y su compilación siguen sin dependencias externas.

Después de cambiar el contenido, ejecuta el generador, abre el PDF para revisar la composición y guarda el PDF actualizado junto con el código. La publicación utiliza el archivo ya generado de `site/assets/Perfil_David_Hernandez.pdf`.

## Cursos, seminarios y constancias
El catálogo `/formacion/` se genera desde `credentials` en `content/portfolio.json`. Cada entrada incluye `id`, `title`, `issuer`, `issued`, `year`, `category`, `kind`, `description`, `document_available` y, opcionalmente, `featured` y `public_file`.

- El catálogo ofrece las constancias a solicitud. Si decides habilitar un documento para descarga pública, guárdalo en `site/assets/formacion/` y registra su ruta en `public_file`.
- Usa una categoría existente: `seguridad`, `redes`, `mps`, `sistemas`, `datos` o `gestion`.
- Conserva el nombre y la fecha que figuran en el documento.
- `kind` distingue curso, seminario, certificado de formación o certificación técnica de fabricante. No conviertas un curso de preparación en una certificación profesional.
- Las cartas de respaldo del mismo curso se consideran documentación complementaria; no cuentan como una actividad adicional.
- Los elementos con `featured: true` aparecen en la portada (hasta cuatro). El catálogo completo incluye todas las entradas y admite búsqueda y filtros.

## Publicaciones académicas
La sección se genera desde `publications` en `content/portfolio.json`. Incluye título, tipo de trabajo, año, sede, todos los autores, resumen propio, referencia bibliográfica y enlaces a las fuentes.

Conserva la autoría y el tipo de publicación: artículo de congreso, reporte técnico u otro documento. Solo incorpora trabajos donde tu nombre figure como autor o coautor. El reporte completo se ofrece a solicitud; las referencias enlazan a fuentes ya publicadas.
