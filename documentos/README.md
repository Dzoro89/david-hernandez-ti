# Documentos públicos

El perfil profesional descargable está en `site/assets/Perfil_David_Hernandez.pdf`.

Para añadir reportes o constancias al sitio:
1. Prepara una versión apta para publicación: sin datos de terceros, firmas, identificaciones, domicilios particulares ni datos confidenciales de clientes.
2. Carga el archivo en `site/assets/documentos/` usando **Add file → Upload files**.
3. Añade una entrada a `documents` en `content/portfolio.json`, por ejemplo:

```json
{"title": "Reporte del laboratorio AD/GPO", "url": "assets/documentos/reporte-ad-gpo.pdf"}
```

Publica solo reportes que ya existan. Los documentos aparecen automáticamente en la sección Documentos después de una compilación y despliegue correctos.

Las constancias académicas completas y referencias pueden compartirse de forma privada durante un proceso de selección. El sitio público no necesita expedientes personales.
