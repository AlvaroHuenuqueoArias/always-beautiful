# Plantillas de Prompts para Codex — Always Beautiful

## 1. Propósito del documento

Este documento define plantillas oficiales para dar instrucciones a Codex CLI, Codex App o cualquier agente técnico que trabaje dentro del proyecto Always Beautiful.

El objetivo es evitar instrucciones vagas y asegurar que cada tarea tenga contexto, alcance, archivos permitidos, archivos prohibidos, validaciones y criterio de cierre.

---

## 2. Plantilla maestra para cualquier tarea

Usar esta plantilla antes de pedir modificaciones:

~~~text
Contexto:
Estoy en el repositorio always-beautiful, rama [NOMBRE_RAMA].
El proyecto usa React/Vite en web y FastAPI en services/api.
Debes usar git checkout, no git switch.

Objetivo:
[Explicar objetivo técnico y de negocio.]

Archivos permitidos:
- [archivo o carpeta 1]
- [archivo o carpeta 2]

Archivos prohibidos:
- [archivo o carpeta 1]
- [archivo o carpeta 2]

Reglas:
- No crear ramas nuevas.
- No hacer squash.
- No modificar archivos fuera del alcance.
- No tocar .env reales.
- No subir dist, node_modules, .DS_Store ni archivos temporales.
- No inventar datos reales.
- Documentar decisiones relevantes.

Validaciones:
- git status --short antes y después.
- npm --prefix web run build si aplica frontend.
- pytest si aplica backend.
- revisión visual de rutas afectadas si aplica.

Entrega:
1. Diagnóstico de entrada.
2. Plan de modificación.
3. Archivos que tocarás.
4. Archivos que no tocarás.
5. Cambios realizados.
6. Validaciones ejecutadas.
7. Riesgos pendientes.
8. Commit sugerido.
9. PR sugerido si aplica.
~~~

---

## 3. Plantilla de diagnóstico sin modificación

~~~text
Contexto:
Estoy en el repositorio always-beautiful, rama [NOMBRE_RAMA].

Objetivo:
Realiza solo un diagnóstico de entrada antes de modificar cualquier archivo.

Reglas obligatorias:
- No modifiques archivos.
- No hagas git add.
- No hagas commit.
- No hagas push.
- No crees ramas.
- No borres archivos.
- No muevas assets.
- No instales dependencias.

Comandos permitidos:
- git rev-parse --abbrev-ref HEAD
- git status --short
- git log --oneline --graph --decorate -10
- git diff --stat
- tree . -a -I 'node_modules|.git|.venv|venv|__pycache__|dist|build|coverage|.pytest_cache|*.pyc|*.sqlite3|.DS_Store'

Entrega:
1. Rama actual.
2. Estado Git.
3. Archivos modificados.
4. Archivos nuevos.
5. Riesgos.
6. Archivos sensibles detectados.
7. Próximo paso recomendado.

No modifiques nada.
~~~

---

## 4. Plantilla para Storefront

~~~text
Contexto:
Estoy en always-beautiful, rama feature/storefront-home-services.
La rama debe cerrarse como avance avanzado pausable, no como Storefront 100%.

Objetivo:
[Explicar ajuste específico del Storefront.]

Archivos permitidos:
- web/src/pages/public/[archivo].jsx
- web/src/components/shared/[archivo].jsx
- web/src/components/storefront/[archivo].jsx
- web/src/data/storefront/[archivo].js
- web/src/index.css solo si es necesario y con alcance limitado

Archivos prohibidos:
- services/api/*
- web/src/pages/admin/*
- web/src/mockAdminData.js
- web/package.json
- web/package-lock.json
- web/src/main.jsx salvo autorización explícita

Reglas:
- No modificar el Dashboard administrativo.
- No cambiar colores base sin autorización.
- No cambiar dimensiones desktop aprobadas.
- No inventar datos reales.
- No integrar pagos, IA, WhatsApp ni AWS.
- Mantener separación entre Storefront público y Admin.

Validación:
- npm --prefix web run build
- revisar /
- revisar /services
- revisar /products
- revisar /booking
- revisar /cart
- revisar /checkout
- revisar /admin

Entrega:
1. Diagnóstico.
2. Cambios realizados.
3. Validaciones.
4. Riesgos.
5. Commit sugerido.
~~~

---

## 5. Plantilla para footer y páginas legales iniciales

~~~text
Contexto:
Estoy en always-beautiful, rama feature/storefront-home-services.

Objetivo:
Afinar la franja inferior institucional del Storefront y preparar placeholders formales para Términos y Política de Privacidad.

Archivos permitidos:
- web/src/components/shared/PublicFooter.jsx
- web/src/index.css
- web/src/pages/public/PrivacyPolicyPage.jsx si debe crearse
- web/src/pages/public/TermsPage.jsx si debe crearse
- web/src/App.jsx solo si es estrictamente necesario registrar rutas nuevas

Archivos prohibidos:
- services/api/*
- web/src/pages/admin/*
- web/src/main.jsx
- web/src/mockAdminData.js
- web/package.json
- web/package-lock.json

Reglas:
- No escribir documentos legales definitivos.
- Crear placeholders formales y revisables.
- No inventar RUT, razón social, dirección, correo real ni datos personales.
- No alterar el Dashboard.
- No modificar diseño desktop aprobado salvo la franja inferior.

Validación:
- npm --prefix web run build
- revisar /
- revisar /privacy
- revisar /terms
- revisar /admin

Entrega:
1. Diagnóstico previo.
2. Archivos modificados.
3. Cambios realizados.
4. Riesgos.
5. Validaciones ejecutadas.
6. Commit sugerido.
~~~

---

## 6. Plantilla para responsive móvil y tablet

~~~text
Contexto:
Estoy en always-beautiful, rama feature/storefront-home-services.

Objetivo:
Implementar una primera capa responsive profesional para Storefront en móvil y tablet.

Archivos permitidos:
- web/src/index.css
- web/src/components/shared/PublicHeader.jsx
- web/src/components/shared/PublicFooter.jsx
- web/src/components/shared/FloatingAssistantButton.jsx
- web/src/pages/public/HomePage.jsx solo si es imprescindible
- web/src/pages/public/ServicesPage.jsx solo si es imprescindible

Archivos prohibidos:
- services/api/*
- web/src/pages/admin/*
- web/src/mockAdminData.js
- web/package.json
- web/package-lock.json

Reglas:
- No modificar dimensiones desktop aprobadas.
- No cambiar colores base.
- No rehacer componentes completos.
- Solo agregar media queries y ajustes controlados.
- Evitar que el botón flotante tape CTAs.
- No romper /admin.

Breakpoints sugeridos:
- móvil: max-width 640px
- tablet: 641px a 1024px
- desktop: desde 1025px

Validación:
- npm --prefix web run build
- revisar /
- revisar /services
- revisar /products
- revisar /booking
- revisar /cart
- revisar /checkout
- revisar /admin

Entrega:
1. Diagnóstico.
2. Cambios realizados.
3. Archivos tocados.
4. Validaciones.
5. Riesgos pendientes.
6. Commit sugerido.
~~~

---

## 7. Plantilla para documentación

~~~text
Contexto:
Estoy en always-beautiful, rama [NOMBRE_RAMA].

Objetivo:
Crear o actualizar documentación técnica del proyecto.

Archivos permitidos:
- docs/[ruta]
- README.md si corresponde
- AGENTS.md si corresponde
- .github/pull_request_template.md si corresponde

Archivos prohibidos:
- services/api/*
- web/src/*
- web/package.json
- web/package-lock.json

Reglas:
- No modificar código.
- No instalar dependencias.
- No cambiar ramas.
- Mantener español formal.
- Diferenciar entre estado cerrado, parcial, mock, futuro y pendiente.

Validación:
- git status --short
- revisión manual del Markdown

Entrega:
1. Archivos modificados.
2. Resumen.
3. Riesgos.
4. Commit sugerido.
~~~

---

## 8. Plantilla para APIs externas

~~~text
Contexto:
Estoy en always-beautiful, rama [NOMBRE_RAMA].

Objetivo:
Diseñar o integrar una API externa en modo sandbox.

API objetivo:
- [Mercado Pago / PayPal / Canva / WhatsApp / AWS / otra]

Reglas:
- No usar credenciales productivas.
- No pegar tokens en código.
- No modificar .env reales.
- Actualizar solo .env.example cuando corresponda.
- Crear adaptador interno.
- Documentar configuración.
- Crear tests si aplica.
- No enviar pagos reales.
- No activar producción sin aprobación.

Entrega:
1. Documentación requerida.
2. Variables necesarias.
3. Archivos a crear o modificar.
4. Riesgos.
5. Validaciones.
6. Commit sugerido.
~~~

---

## 9. Plantilla para IA

~~~text
Contexto:
Estoy en always-beautiful, rama [NOMBRE_RAMA].

Objetivo:
Diseñar o implementar una parte controlada de la capa de IA.

Alcance:
- [assistant endpoint / memoria corta / reglas / LangGraph / recomendaciones / WhatsApp]

Reglas:
- No implementar todo el sistema de IA en una sola tarea.
- No usar datos reales sensibles.
- No prometer efectos médicos, cosméticos o científicos sin fuentes.
- Comenzar por reglas determinísticas antes de Machine Learning.
- Separar IA conversacional de recomendación de productos.

Entrega:
1. Diseño técnico.
2. Archivos propuestos.
3. Riesgos.
4. Validaciones.
5. Commit sugerido.
~~~

---

## 10. Regla final

Si una tarea no puede expresarse con contexto, objetivo, archivos permitidos, archivos prohibidos y validaciones, no debe ejecutarse todavía.
