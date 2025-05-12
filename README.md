# DentixPro 🦷

DentixPro es un sistema de gestión de citas para consultorios dentales. Permite a los usuarios agendar y visualizar sus citas, mientras que los administradores pueden gestionarlas con privilegios de edición, cancelación y supervisión.

## 🚀 Tecnologías utilizadas

### Frontend
- React
- JavaScript
- Tailwind CSS

### Backend
- Flask (Python)
- MongoDB

## 👥 Roles del sistema

- **Usuario**:
  - Registro e inicio de sesión
  - Agendar citas
  - Consultar historial de citas

- **Administrador**:
  - Ver todas las citas
  - Cancelar o actualizar citas existentes

## 🛠️ Instalación y ejecución local

### Requisitos previos
- Node.js y npm
- Python 3.10+
- Entorno virtual de Python (`venv`)
- MongoDB local o remoto

### Clonar el repositorio

```bash
git clone https://github.com/ChrisUBS/DentixPro
cd DentixPro
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
# Activar entorno virtual
# En Windows
venv\Scripts\activate
# En Unix/Mac
source venv/bin/activate

pip install -r requirements.txt
python server.py
```

## 📂 Estructura del proyecto

```bash
DentixPro/
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── package.json
│   ├── src/
│   └── ...
└── README.md
```

## ✅ Funcionalidades principales

- Registro e inicio de sesión
- Gestión de citas (crear, ver, actualizar, cancelar)
- Interfaz diferenciada por rol (usuario / administrador)

## 📬 Contacto
- Christian Uriel Bonilla Suárez: [christian.bonilla@uabc.edu.mx](mailto:christian.bonilla@uabc.edu.mx)
- Erick Manuel Rodríguez López: [e1291222@uabc.edu.mx](mailto:e1291222@uabc.edu.mx)

## 🪪 Licencia

Este proyecto está bajo la licencia GNU GPL (General Public License).
