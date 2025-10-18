# 🎓 Proyecto Auth0 ITM — Sistema de Autenticación con Flask

Este proyecto implementa un sistema de autenticación usando **Auth0** en una aplicación **Flask (Python)**.  
Permite a los usuarios **iniciar sesión, cerrar sesión y modificar su información personal**, almacenando los datos en la sección `user_metadata` de Auth0.

---

## 🚀 Objetivos del Proyecto

1. **Configurar el formulario de login** con Auth0.
2. **Personalizar el Universal Login** con el logo e identidad visual del ITM.
3. **Crear una sección de perfil** para modificar datos del usuario:
   - Tipo de documento  
   - Número de documento  
   - Dirección  
   - Teléfono
4. **Consumir la API de Auth0** para actualizar el `user_metadata`.
5. **Versionar y documentar** todo el proceso, incluyendo un diagrama de flujo.

---

## 🧠 Tecnologías Utilizadas

- **Python 3**
- **Flask**
- **Authlib**
- **Auth0**
- **dotenv**
- **HTML / CSS**
- **Git & GitHub**

---

## ⚙️ Instalación y Configuración

### 1️⃣ Clonar el repositorio

git clone https://github.com/luismunoz2502/proyecto-auth0-itm.git
cd proyecto-auth0-itm

2️⃣ Crear entorno virtual
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
3️⃣ Instalar dependencias
pip install flask authlib python-dotenv
4️⃣ Crear archivo .env
Crea un archivo llamado .env en la raíz del proyecto con la siguiente estructura:
AUTH0_CLIENT_ID=TU_CLIENT_ID
AUTH0_CLIENT_SECRET=TU_CLIENT_SECRET
AUTH0_DOMAIN=tu-dominio.auth0.com
APP_SECRET_KEY=una-clave-super-secreta-larga-123456789
AUTH0_MANAGEMENT_API_TOKEN=TU_TOKEN_DE_API
💡 El token de API se genera desde el Dashboard de Auth0 en Applications → APIs → Auth0 Management API → Test → Copy Token.
