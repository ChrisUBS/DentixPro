import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import { motion } from "framer-motion";
import { Toaster } from "@/components/ui/toaster";

// Páginas
import HomePage from "@/pages/HomePage";
import LoginPage from "@/pages/LoginPage";
import RegisterPage from "@/pages/RegisterPage";
import UserDashboard from "@/pages/UserDashboard";
import AdminDashboard from "@/pages/AdminDashboard";
import AppointmentForm from "@/pages/AppointmentForm";
import NotFoundPage from "@/pages/NotFoundPage";

// Componentes
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

// Rutas protegidas
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) return <div className="text-center py-10">Cargando...</div>;

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.rol)) {
    return <Navigate to="/" replace />;
  }

  return children;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="flex flex-col min-h-screen">
          <Navbar />

          <motion.main
            className="flex-grow"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Rutas protegidas para usuarios */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute allowedRoles={["user", "admin"]}>
                    <UserDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/agendar-cita"
                element={
                  <ProtectedRoute allowedRoles={["user"]}>
                    <AppointmentForm />
                  </ProtectedRoute>
                }
              />

              {/* Rutas protegidas para administradores */}
              <Route
                path="/admin"
                element={
                  <ProtectedRoute allowedRoles={["admin"]}>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />

              {/* Página 404 */}
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </motion.main>

          <Footer />
          <Toaster />
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
