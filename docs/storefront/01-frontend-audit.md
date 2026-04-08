# 01 — Auditoría del frontend actual

## Objetivo de esta auditoría

El propósito de este documento es registrar el estado real del frontend actual del proyecto Always Beautiful antes de iniciar la construcción del módulo Storefront.

## Estructura actual observada

La carpeta `web/` del proyecto contiene actualmente:

- `index.html`
- `package.json`
- `vite.config.js`
- `src/App.jsx`
- `src/main.jsx`
- `src/index.css`
- componentes enfocados en métricas administrativas
- dataset sintético orientado a panel administrativo

## Diagnóstico general

El frontend actual no corresponde todavía a un Storefront público en construcción.  
Corresponde a una aplicación React/Vite orientada principalmente al **Admin Panel**.

Esta conclusión se sustenta en los siguientes puntos:

### 1. Punto de entrada único
El archivo `main.jsx` renderiza directamente el componente `App`, sin sistema de rutas ni layouts separados.

### 2. Contenedor principal orientado a administración
El archivo `App.jsx` consume el endpoint:

`/admin/dashboard`

y construye una interfaz centrada en:

- métricas,
- reservas del día,
- órdenes recientes,
- indicadores financieros,
- rendimiento profesional,
- tendencias,
- y resumen ejecutivo.

### 3. Componentes especializados en analítica
Los componentes importados actualmente son:

- `EcommercePerformance`
- `ExecutiveInsights`
- `ProfessionalPerformance`
- `TrendSnapshot`

Todos ellos responden a una lógica administrativa y analítica, no a una lógica comercial pública orientada al cliente final.

### 4. Hoja de estilos con semántica de dashboard
El archivo `index.css` está estructurado alrededor de clases como:

- `.dashboard-shell`
- `.sidebar-panel`
- `.main-panel`
- `.metric-block`
- `.panel-card`

lo que confirma que la semántica visual actual está diseñada para un panel interno y no para una experiencia pública tipo Storefront.

## Conclusión técnica principal

El frontend actual sí es reutilizable, pero no debe seguir creciendo como si fuera una sola aplicación monolítica centrada en `App.jsx`.

La decisión correcta es:

- conservar el Admin Panel existente,
- encapsularlo como una zona propia,
- y abrir una nueva capa pública dentro del mismo frontend.

## Qué se conserva

Se conservarán:

- Vite,
- React,
- base actual del proyecto `web/`,
- parte del sistema visual actual,
- tokens de color,
- componentes administrativos,
- lógica de consumo del dashboard administrativo.

## Qué debe migrar más adelante

Deberá migrarse o reorganizarse:

- `App.jsx`, que dejará de ser el contenedor único de toda la aplicación;
- la hoja de estilos global, que deberá separarse entre estilos compartidos, admin y storefront;
- la estructura de carpetas del frontend, que deberá crecer por dominios y responsabilidades.

## Qué no debe tocarse todavía

No deben tocarse todavía:

- los contratos actuales del dashboard administrativo,
- la lógica backend de `/admin/dashboard`,
- los componentes analíticos ya construidos,
- ni la estructura de los módulos backend.

## Decisión arquitectónica derivada de esta auditoría

A partir de esta auditoría, se concluye que la evolución correcta del frontend será:

- mantener una sola aplicación `web/`,
- pero separar internamente:
  - área pública Storefront,
  - área administrativa Admin.

Esa separación se realizará en fases posteriores mediante rutas, layouts, páginas y componentes específicos.