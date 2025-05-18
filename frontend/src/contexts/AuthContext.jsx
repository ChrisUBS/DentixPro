// src/contexts/AuthContext.js
import React, { createContext, useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

// Crear el contexto
const AuthContext = createContext(null);

// Proveedor del contexto que envuelve a la aplicación
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Verificar autenticación al cargar la aplicación
    useEffect(() => {
        const checkUserAuth = async () => {
            try {
                // Intentar recuperar usuario del localStorage primero
                const storedUser = authService.getCurrentUser();

                if (storedUser) {
                    setUser(storedUser);
                }

                // Si hay un token, verificar con el servidor si es válido
                if (localStorage.getItem('authToken')) {
                    const userData = await authService.checkAuth();
                    setUser(userData);
                }
            } catch (err) {
                console.error('Error verificando autenticación:', err);
                // Si hay un error, limpiar el usuario y token
                authService.logout();
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkUserAuth();
    }, []);

    // Función para iniciar sesión
    const login = async (email, password) => {
        setLoading(true);
        setError(null);
        try {
            const data = await authService.login(email, password);
            setUser(data.user);
            return data;
        } catch (err) {
            setError(err.response?.data?.msg || 'Error al iniciar sesión');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Función para registrarse
    const signup = async (userData) => {
        setLoading(true);
        setError(null);
        try {
            const data = await authService.signup(userData);
            setUser(data.user);
            return data;
        } catch (err) {
            setError(err.response?.data?.msg || 'Error al registrarse');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // Función para cerrar sesión
    const logout = () => {
        authService.logout();
        setUser(null);
        navigate('/login');
    };

    // Verificar si un usuario es administrador
    const isAdmin = () => {
        return user && user.rol === 'admin';
    };

    // Valor del contexto que estará disponible para los componentes
    const value = {
        user,
        loading,
        error,
        login,
        signup,
        logout,
        isAdmin,
        isAuthenticated: !!user,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Hook personalizado para usar el contexto de autenticación
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth debe ser usado dentro de un AuthProvider');
    }
    return context;
};

export default AuthContext;