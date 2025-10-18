import os
from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlencode
import requests

# Cargar variables de entorno desde .env
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)

# Clave secreta (para sesiones)
app.secret_key = os.getenv('APP_SECRET_KEY')

# Configurar OAuth con Auth0
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/openid-configuration"
)

# ---------- RUTA PRINCIPAL ----------
@app.route('/')
def home():
    user = session.get('user')
    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ITM - Auth0 Application</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                max-width: 600px;
                width: 100%;
                text-align: center;
            }}
            h1 {{ color: #00875A; }}
            .btn {{
                background: #00875A;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 8px;
                margin: 5px;
                display: inline-block;
            }}
            .btn:hover {{ background: #006644; }}
            .btn-logout {{ background: #dc3545; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Instituto Tecnológico Metropolitano</h1>
            <p>Sistema de Autenticación con Auth0</p>
            {"".join([f'''
                <div>
                    <h2>¡Bienvenido, {user['userinfo']['name']}! 👋</h2>
                    <p><strong>📧 Email:</strong> {user['userinfo']['email']}</p>
                    <p><strong>🆔 User ID:</strong> {user['userinfo']['sub']}</p>
                    <a href="/profile" class="btn">📝 Modificar Mis Datos</a>
                    <a href="/logout" class="btn btn-logout">🚪 Cerrar Sesión</a>
                </div>
            ''' if user else '''
                <a href="/login" class="btn">🔐 Iniciar Sesión con Auth0</a>
            '''])}
        </div>
    </body>
    </html>
    '''
    return html


# ---------- LOGIN / LOGOUT ----------
@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route('/callback')
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?"
        + urlencode({
            "returnTo": url_for("home", _external=True),
            "client_id": os.getenv("AUTH0_CLIENT_ID"),
        }, quote_via=quote_plus)
    )


# ---------- PERFIL ----------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))

    metadata = user.get('userinfo', {}).get('user_metadata', {}) or {}

    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Modificar Datos</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #00B388, #00875A);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            form {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
                width: 400px;
            }}
            h2 {{ text-align: center; color: #00875A; }}
            label {{ display: block; margin-top: 10px; font-weight: bold; }}
            input, select {{
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}
            button {{
                background: #00875A;
                color: white;
                border: none;
                padding: 10px;
                width: 100%;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 15px;
            }}
            button:hover {{ background: #006644; }}
            a {{
                display: block;
                text-align: center;
                margin-top: 10px;
                text-decoration: none;
                color: #00875A;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <form method="POST" action="/update_profile">
            <h2>Modificar mis datos</h2>
            
            <label>Tipo de documento:</label>
            <select name="tipo_doc" required>
                <option value="">Seleccionar...</option>
                <option value="CC" {"selected" if metadata.get("tipo_doc") == "CC" else ""}>Cédula</option>
                <option value="TI" {"selected" if metadata.get("tipo_doc") == "TI" else ""}>Tarjeta de Identidad</option>
                <option value="CE" {"selected" if metadata.get("tipo_doc") == "CE" else ""}>Cédula de Extranjería</option>
            </select>

            <label>Número de documento:</label>
            <input type="text" name="numero_doc" value="{metadata.get('numero_doc', '')}" required>

            <label>Dirección:</label>
            <input type="text" name="direccion" value="{metadata.get('direccion', '')}">

            <label>Teléfono:</label>
            <input type="text" name="telefono" value="{metadata.get('telefono', '')}">

            <button type="submit">Guardar Cambios</button>
            <a href="/">← Volver</a>
        </form>
    </body>
    </html>
    '''
    return html


# ---------- NUEVA RUTA: ACTUALIZAR DATOS EN AUTH0 ----------
@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Actualizar user_metadata en Auth0"""
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))

    user_id = user['userinfo']['sub']
    url = f"https://{os.getenv('AUTH0_DOMAIN')}/api/v2/users/{user_id}"

    headers = {
        "Authorization": f"Bearer {os.getenv('AUTH0_MGMT_TOKEN')}",
        "Content-Type": "application/json"
    }

    data = {
        "user_metadata": {
            "tipo_doc": request.form.get("tipo_doc"),
            "numero_doc": request.form.get("numero_doc"),
            "direccion": request.form.get("direccion"),
            "telefono": request.form.get("telefono")
        }
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        return f"<h2>✅ Datos actualizados correctamente en Auth0.</h2><a href='/profile'>Volver</a>"
    else:
        return f"<h2>❌ Error al actualizar los datos: {response.text}</h2><a href='/profile'>Volver</a>"


# ---------- EJECUCIÓN ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
