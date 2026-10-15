# David Hernández | TI & Ciberseguridad

Portafolio profesional de **David Hernández Trinidad**: liderazgo TI, infraestructura, ciberseguridad y soluciones MPS.

Incluye una portada adaptable a móvil, experiencia ampliable, laboratorios con fichas propias, formación y certificaciones, documentos, contacto y un resumen imprimible para Recursos Humanos.

## Accesos públicos

- [Abrir portafolio](https://dzoro89.github.io/david-hernandez-ti/)
- [Resumen profesional para RH](https://dzoro89.github.io/david-hernandez-ti/perfil/)
- [Laboratorios y bitácora técnica](https://dzoro89.github.io/david-hernandez-ti/#laboratorios)
- [Catálogo de formación y constancias](https://dzoro89.github.io/david-hernandez-ti/formacion/)
- [Publicaciones y trabajo académico](https://dzoro89.github.io/david-hernandez-ti/#publicaciones)

## Publicación

1. Abre **Settings → Pages** en este repositorio.
2. En **Build and deployment → Source**, selecciona **GitHub Actions** si todavía no está seleccionado.
3. En **Actions → Publicar portafolio**, ejecuta **Run workflow** o vuelve a ejecutar la publicación.
4. Abre el enlace que devuelve el paso **Publicar sitio** o el entorno `github-pages`.

Cada cambio en `main` vuelve a construir y publicar el sitio. La dirección canónica se obtiene de GitHub Pages; el código no depende del repositorio anterior.

## Cómo actualizar

| Contenido | Archivo |
| --- | --- |
| Presentación y experiencia | `site/index.html` |
| Perfil para RH | `site/profile.html` |
| Laboratorios, certificados y documentos | `content/portfolio.json` |
| Diseño | `site/styles.css` |
| Navegación, filtros y copiar correo | `site/app.js` |
| PDF profesional | `site/assets/Perfil_David_Hernandez.pdf` |
| Documentación de cada laboratorio | `laboratorios/<nombre>/README.md` |
| Guía de mantenimiento | `GUIA_DE_EDICION.md` |

## Ejecución local

Solo requiere Python 3. No hay dependencias de ejecución, fuentes externas, formularios, cuentas de visitantes ni analítica.

```bash
python3 scripts/build.py
python3 scripts/check_site.py
```

El resultado se genera en `_site/`. Puede alojarse en cualquier servicio de archivos estáticos. Para otro dominio, define `SITE_URL` al construir.

## Criterios del contenido

- La experiencia profesional se presenta separada de las prácticas de laboratorio. Los indicadores de SLA, primeras respuestas y monitoreo corresponden a la operación del servicio; el monitoreo se refiere a la base instalada.
- VMware está en desarrollo; AD/GPO, Wazuh y hardening están planificados.
- Ningún laboratorio se muestra como completado sin evidencia publicada.
- La maestría (2020-2023) y la ingeniería (2017-2020), ambas de UNITEC, se presentan como estudios concluidos con titulación en proceso.
- El catálogo conserva el tipo y la fecha de cada constancia. Los cursos de Cisco Networking Academy se distinguen de una certificación profesional CCNA. Las cartas de respaldo no duplican cursos. No se inventan credenciales, vigencia, resultados ni métricas.
- No se publican datos de clientes, información familiar ni detalles de procesos de contratación.
