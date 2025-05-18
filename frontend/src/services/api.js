// src/services/api.js
import axios from 'axios';

// Configuración para acceder a variables de entorno en React
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Obtener token JWT del almacenamiento local
const getToken = () => {
    return localStorage.getItem('authToken');
};

// Crear instancia de axios con URL base
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Interceptor para añadir token JWT a cada petición
api.interceptors.request.use((config) => {
    const token = getToken();
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Interceptor para manejar errores comunes
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Manejar error 401 (no autorizado)
        if (error.response && error.response.status === 401) {
            // Si el token expiró, limpiar el almacenamiento y redirigir a login
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            // La redirección se manejará en el componente con un hook personalizado
        }
        return Promise.reject(error);
    }
);

// Servicio para autenticación
export const authService = {
    // Iniciar sesión con email y contraseña
    login: async (email, password) => {
        try {
            const response = await api.post('/auth/login', { email, password });
            // Guardar token en localStorage
            if (response.data.access_token) {
                localStorage.setItem('authToken', response.data.access_token);
                // Guardar información del usuario
                if (response.data.user) {
                    localStorage.setItem('user', JSON.stringify(response.data.user));
                }
            }
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Registrar nuevo usuario
    signup: async (userData) => {
        try {
            const response = await api.post('/auth/signup', userData);
            // Guardar token en localStorage para login automático
            if (response.data.access_token) {
                localStorage.setItem('authToken', response.data.access_token);
                if (response.data.user) {
                    localStorage.setItem('user', JSON.stringify(response.data.user));
                }
            }
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Cerrar sesión
    logout: () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        // Si usas React Router, podrías redirigir aquí con useNavigate
    },

    // Verificar estado de autenticación
    checkAuth: async () => {
        try {
            const response = await api.get('/users/me');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Obtener datos del usuario actual (desde localStorage o API)
    getCurrentUser: () => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },
};

// Servicio para usuarios
export const userService = {
    // Obtener información del usuario actual
    getCurrentUser: async () => {
        try {
            const response = await api.get('/users/me');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Actualizar información del usuario actual
    updateProfile: async (userData) => {
        try {
            const response = await api.put('/users/me', userData);
            // Actualizar información en localStorage
            if (response.data && response.data.user) {
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Cambiar contraseña del usuario actual
    changePassword: async (currentPassword, newPassword) => {
        try {
            const response = await api.put('/users/me/password', {
                current_password: currentPassword,
                new_password: newPassword
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Obtener citas del usuario actual
    getUserDates: async (page = 1, pageSize = 10, status) => {
        try {
            let url = `/users/me/dates?page=${page}&page_size=${pageSize}`;
            if (status) {
                url += `&status=${status}`;
            }
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // MÉTODOS DE ADMINISTRADOR

    // Obtener todos los usuarios (admin)
    getAllUsers: async (page = 1, pageSize = 10, rol) => {
        try {
            let url = `/users?page=${page}&page_size=${pageSize}`;
            if (rol) {
                url += `&rol=${rol}`;
            }
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Obtener usuario por ID (admin)
    getUserById: async (userId) => {
        try {
            const response = await api.get(`/users/${userId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Actualizar usuario (admin)
    updateUser: async (userId, userData) => {
        try {
            const response = await api.put(`/users/${userId}`, userData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Resetear contraseña de usuario (admin)
    resetUserPassword: async (userId, newPassword) => {
        try {
            const response = await api.put(`/users/${userId}/reset-password`, {
                new_password: newPassword
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

// Servicio para citas (dates)
export const dateService = {
    // Crear una nueva cita
    createDate: async (dateData) => {
        try {
            const response = await api.post('/dates', dateData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Cancelar una cita
    cancelDate: async (dateId) => {
        try {
            const response = await api.delete(`/dates/${dateId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // MÉTODOS DE ADMINISTRADOR

    // Obtener todas las citas (admin)
    getAllDates: async (page = 1, pageSize = 10, filters = {}) => {
        try {
            const { status, dateFrom, dateTo } = filters;
            let url = `/admin/dates?page=${page}&page_size=${pageSize}`;

            if (status) {
                url += `&status=${status}`;
            }
            if (dateFrom) {
                url += `&date_from=${dateFrom}`;
            }
            if (dateTo) {
                url += `&date_to=${dateTo}`;
            }

            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Actualizar una cita (admin)
    updateDate: async (dateId, dateData) => {
        try {
            const response = await api.put(`/admin/dates/${dateId}`, dateData);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Marcar una cita como completada (admin)
    completeDate: async (dateId) => {
        try {
            const response = await api.put(`/admin/dates/${dateId}/complete`);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // Marcar una cita como cancelada (admin)
    CancelDate: async (dateId) => {
        try {
            const response = await api.put(`/admin/dates/${dateId}/cancel`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

};

export default api;