# 03 — Checklist de datos requeridos para el módulo Storefront

## Objetivo del documento

Este documento registra toda la información que será necesaria solicitar progresivamente para construir el módulo Storefront de forma coherente, aun cuando parte del backend o de los datos reales del negocio siga en estado ficticio o parcial.

## Bloque A — Datos ya recibidos del proyecto actual

En esta fase ya fueron compartidos y analizados los siguientes elementos del proyecto actual:

- `git log --oneline --graph --all`
- `tree -a` del repositorio
- `web/package.json`
- `web/src/App.jsx`
- `web/src/main.jsx`
- `web/src/index.css`
- `web/vite.config.js`

## Bloque B — Datos ya recibidos del repositorio guía

En esta fase ya fueron compartidos y analizados:

- `README.md`
- listado de `screenshots/`
- `index.php`
- `services.php`
- `products.php`
- `appointment.php`
- `cart.php`
- `checkout.php`
- `my-account.php`
- `manage_appointments.php`
- `manage_orders.php`

## Bloque C — Datos que se solicitarán más adelante para el Storefront

Los siguientes datos no son requeridos aún para cerrar esta rama documental, pero sí serán necesarios en las próximas fases del módulo:

### 1. Servicios reales o ficticios
Se solicitará:

- nombre del servicio,
- categoría,
- descripción corta,
- precio base,
- precio promocional o especial si aplica,
- duración estimada,
- profesional asociado si corresponde.

### 2. Productos reales o ficticios
Se solicitará:

- nombre del producto,
- categoría,
- precio,
- descripción corta,
- estado de stock,
- imagen placeholder o referencia futura.

### 3. Profesionales ficticios o reales
Se solicitará:

- nombre,
- rol,
- especialidad,
- breve descripción,
- imagen placeholder,
- disponibilidad general.

### 4. Disponibilidad ficticia para booking
Se solicitará:

- horarios base,
- días disponibles,
- restricciones simples,
- slots de ejemplo,
- y relación entre servicio y profesional.

### 5. Branding del Storefront
Se solicitará:

- colores definitivos o preliminares,
- tono visual,
- estilo de marca,
- logo provisional o final,
- criterios de elegancia / boutique / premium / minimalista.

### 6. Prioridades del MVP
Se solicitará definir qué entra primero dentro del módulo:

- Home
- Services
- Products
- Booking
- Cart
- Checkout
- Account
- Orders
- Appointment history

## Para qué se usarán esos datos

Esos datos serán utilizados para construir:

- cards visuales,
- filtros,
- textos de interfaz,
- placeholders,
- datasets,
- mocks,
- navegación comercial,
- y estados realistas del Storefront.

## Importante

La solicitud futura de estos datos no significa reabrir ni cerrar inmediatamente todos los módulos backend del proyecto.  
Su objetivo principal será alimentar la capa visual y funcional del Storefront mientras algunos módulos backend continúan en estado parcial, ficticio o pendiente de datos reales.

## Conclusión

Este checklist existe para evitar improvisación.  
Cada dato solicitado en fases posteriores tendrá una finalidad concreta dentro del frontend público y permitirá construir una experiencia más creíble, ordenada y cercana al comportamiento real del negocio.