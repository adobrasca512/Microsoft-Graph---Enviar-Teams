import msal
import requests

# Configuración
CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
AUTHORITY_URL = 'https://login.microsoftonline.com/tenant'
SCOPE = ["https://graph.microsoft.com/.default"]  # Los permisos necesarios
MAX_PAGE_SIZE = 999  # Tamaño máximo de la página

# Crear una instancia del cliente
app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY_URL
)

# Obtener el token de autenticación
result = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" in result:
    ACCESS_TOKEN = result['access_token']
    url = 'https://graph.microsoft.com/v1.0/users'

    # Encabezado de autorización con el token de acceso
    headers = {
        'Authorization': 'Bearer {}'.format(ACCESS_TOKEN),
        'Content-Type': 'application/json',
        'ConsistencyLevel': 'eventual'  # Agregar el encabezado necesario
    }

    # Lista para almacenar los datos de los usuarios
    datos_usuarios = []

    # Realizar la solicitud GET a Microsoft Graph API de forma paginada
    while url:
        response = requests.get(url, headers=headers, params={'$top': MAX_PAGE_SIZE, '$select': 'id,displayName,mail,jobTitle,department,companyName,officeLocation'})
        if response.status_code == 200:
            # Agregar los datos de los usuarios de la página actual
            users = response.json()['value']
            datos_usuarios.extend(users)
            print(datos_usuarios)
            # Obtener la URL de la próxima página si existe
            next_link = response.json().get('@odata.nextLink')
            url = next_link
        else:
            # Manejar errores
            error = {
                'error': 'Error al obtener los usuarios',
                'status_code': response.status_code,
                'message': response.text
            }
            print(error)
else:
    # Manejar errores
    error = {
        'error': result.get("error"),
        'error_description': result.get("error_description")
    }
    print(error)
