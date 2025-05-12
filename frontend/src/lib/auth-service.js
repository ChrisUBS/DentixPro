
// Usuarios predefinidos
const predefinedUsers = [
  {
    id: "admin",
    name: "Administrador",
    email: "admin@dental.com",
    password: "admin123",
    role: "admin"
  },
  {
    id: "user1",
    name: "Juan Pérez",
    email: "juan@ejemplo.com",
    password: "password123",
    role: "user"
  }
];

// Inicializar usuarios en localStorage si no existen
export const initializeUsers = () => {
  const users = localStorage.getItem('dentalUsers');
  if (!users) {
    localStorage.setItem('dentalUsers', JSON.stringify(predefinedUsers));
  }
};

// Obtener todos los usuarios
export const getUsers = () => {
  const users = localStorage.getItem('dentalUsers');
  return users ? JSON.parse(users) : [];
};

// Autenticar usuario
export const loginUser = (email, password) => {
  const users = getUsers();
  const user = users.find(u => u.email === email && u.password === password);
  
  if (user) {
    // Guardar sesión del usuario
    const session = {
      userId: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      loggedInAt: new Date().toISOString()
    };
    
    localStorage.setItem('dentalCurrentSession', JSON.stringify(session));
    return session;
  }
  
  return null;
};

// Registrar nuevo usuario
export const registerUser = (userData) => {
  const users = getUsers();
  
  // Verificar si el email ya existe
  if (users.some(user => user.email === userData.email)) {
    return { success: false, message: "El correo electrónico ya está registrado" };
  }
  
  const newUser = {
    id: Date.now().toString(),
    ...userData,
    role: "user" // Por defecto, todos los nuevos usuarios son clientes
  };
  
  users.push(newUser);
  localStorage.setItem('dentalUsers', JSON.stringify(users));
  
  return { success: true, user: newUser };
};

// Obtener sesión actual
export const getCurrentSession = () => {
  const session = localStorage.getItem('dentalCurrentSession');
  return session ? JSON.parse(session) : null;
};

// Cerrar sesión
export const logoutUser = () => {
  localStorage.removeItem('dentalCurrentSession');
};

// Verificar si el usuario es administrador
export const isAdmin = () => {
  const session = getCurrentSession();
  return session && session.role === 'admin';
};
