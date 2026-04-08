# 00 — Alcance del módulo Storefront

## Propósito del módulo

El módulo Storefront representa la futura experiencia pública del proyecto Always Beautiful. Su objetivo es ofrecer una interfaz visual orientada al cliente final para exhibir servicios, productos, reservas y procesos de compra, tomando como referencia funcional y visual el repositorio guía **Glamour Salon Management System**, pero adaptado completamente a nuestro stack oficial basado en **React + Vite** para el frontend y **FastAPI** para el backend.

## Fundamentación del módulo

El repositorio guía demuestra una separación clara entre:

- experiencia pública del cliente,
- experiencia de cuenta del usuario,
- y experiencia administrativa.

Esa organización se observa tanto en su `README.md` como en su estructura de pantallas y screenshots, donde aparecen vistas como:

- Home,
- Services,
- Products,
- Appointment,
- Cart,
- Checkout,
- My Account,
- Manage Appointments,
- Manage Orders,
- Admin Dashboard.

Por lo tanto, este módulo no nace desde una improvisación visual, sino desde una referencia funcional concreta que será reinterpretada bajo la arquitectura real del proyecto Always Beautiful.

## Objetivo del MVP del Storefront

La primera versión funcional del Storefront deberá construir una base pública sólida y coherente, centrada en:

- Home pública,
- vista de servicios,
- vista de productos,
- carrito,
- checkout visual inicial,
- y shell visual de reservas.

## Qué sí entra en esta etapa inicial

En la etapa inicial del módulo Storefront sí entran:

- definición arquitectónica del frontend público,
- separación conceptual entre admin y área pública,
- diseño de estructura de rutas,
- modelado de páginas públicas principales,
- definición de placeholders visuales,
- preparación para consumo de datos reales o ficticios.

## Qué no entra todavía en esta etapa inicial

En esta fase aún no entran:

- integración completa con pagos reales,
- integración completa con shipping real,
- autenticación pública definitiva del cliente,
- gestión completa de cuenta del cliente,
- imágenes finales de producción,
- endurecimiento productivo del frontend.

## Relación con el backend actual

El módulo Storefront se apoyará progresivamente sobre módulos backend ya existentes o avanzados dentro del proyecto:

- catalog,
- cart,
- orders,
- booking,
- schedule,
- payments,
- shipping.

Sin embargo, durante sus primeras fases podrá utilizar datos ficticios, mocks y adapters temporales con el fin de construir primero la experiencia visual y de navegación sin bloquear el avance por dependencias todavía incompletas.

## Criterio de implementación

La implementación del módulo Storefront seguirá estos principios:

1. no destruir el Admin Panel existente;
2. no mezclar responsabilidades públicas y administrativas en un mismo componente monolítico;
3. traducir la cobertura funcional del repositorio guía a nuestro stack real;
4. mantener una lógica de crecimiento modular compatible con GitFlow.

## Resultado esperado de este módulo

Al finalizar sus primeras fases, el proyecto deberá contar con una base pública visible, ordenada, navegable y profesional, capaz de evolucionar más adelante hacia una experiencia completa de reserva, compra y cuenta de cliente.