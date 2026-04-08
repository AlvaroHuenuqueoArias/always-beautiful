# 02 — Mapa del repositorio guía y traducción a nuestra arquitectura

## Objetivo del documento

Este documento registra qué partes del repositorio guía **Glamour Salon Management System** serán utilizadas como referencia funcional y visual para construir el módulo Storefront del proyecto Always Beautiful.

## Lectura general del repositorio guía

Según su `README.md`, screenshots y archivos principales, el repositorio guía ofrece una plataforma web con tres zonas funcionales bien diferenciadas:

### A. Área pública
- Home
- About
- Contact
- Services
- Products
- Appointment
- Cart
- Checkout
- Blog
- Gallery

### B. Área de cuenta del cliente
- My Account
- Manage Appointments
- Manage Orders
- Wishlist

### C. Área administrativa
- Admin Dashboard
- Staff Dashboard

## Archivos analizados del repositorio guía

En esta fase se han inspeccionado los siguientes archivos:

- `index.php`
- `services.php`
- `products.php`
- `appointment.php`
- `cart.php`
- `checkout.php`
- `my-account.php`
- `manage_appointments.php`
- `manage_orders.php`

## Principales aprendizajes funcionales

### `index.php`
La home del repositorio guía incluye:

- hero principal con slider,
- bloque de historia / presentación,
- preview de servicios,
- bloque comercial de beneficios o membresía,
- equipo,
- galería / trabajos,
- preview de productos,
- preview de blog.

### `services.php`
La vista de servicios incluye:

- breadcrumb,
- filtros por categoría,
- cards de servicios,
- precios estándar y member price.

### `products.php`
La vista de productos incluye:

- breadcrumb,
- filtro por precio,
- buscador,
- categorías,
- grid view,
- list view,
- paginación,
- add to cart,
- wishlist.

### `appointment.php`
La vista de reservas incluye:

- usuario autenticado,
- selección de servicio,
- fecha,
- hora,
- selección opcional de staff,
- confirmación del proceso.

### `cart.php`
El carrito incluye:

- lista de productos,
- actualización de cantidades,
- subtotal,
- total,
- eliminación de ítems,
- selección de método de pago,
- transición hacia checkout.

### `checkout.php`
El checkout guía muestra un flujo de confirmación y preparación del pago, conectado en su caso a un proveedor de pagos específico.

### `my-account.php`
La cuenta del cliente permite:

- editar información personal,
- cambiar contraseña,
- actualizar dirección.

### `manage_appointments.php`
La gestión de citas permite:

- listar reservas,
- ver fecha, hora, servicio y staff,
- cancelar reservas bajo ciertas condiciones.

### `manage_orders.php`
La gestión de órdenes permite:

- listar pedidos,
- ver estado,
- cancelar órdenes según reglas,
- descargar comprobantes.

## Traducción funcional a nuestro proyecto

La traducción base será la siguiente:

- `index.php` → `HomePage.jsx`
- `services.php` → `ServicesPage.jsx`
- `products.php` → `ProductsPage.jsx`
- `appointment.php` → `BookingPage.jsx`
- `cart.php` → `CartPage.jsx`
- `checkout.php` → `CheckoutPage.jsx`
- `my-account.php` → `AccountPage.jsx` o fase posterior
- `manage_appointments.php` → `AppointmentsPage.jsx` o fase posterior
- `manage_orders.php` → `OrdersPage.jsx` o fase posterior

## Qué sí tomamos del repositorio guía

Tomaremos del repositorio guía:

- la cobertura funcional,
- el orden de pantallas,
- la inspiración visual general,
- la jerarquía del recorrido del cliente,
- la noción de bloques para home,
- y la lógica de navegación pública/comercial.

## Qué no tomamos directamente

No tomaremos directamente:

- PHP,
- MySQL,
- PayHere,
- lógica de sesión del sistema guía,
- ni su implementación literal.

## Conclusión

El repositorio guía funciona como una referencia de producto y de experiencia, no como base tecnológica.  
Su valor para el proyecto Always Beautiful está en mostrarnos qué piezas debe tener el Storefront, cómo se relacionan entre sí y en qué orden conviene construirlas.