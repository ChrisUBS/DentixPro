
import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Toaster } from "@/components/ui/toaster";
import { initializeUsers, getCurrentSession } from "@/lib/auth-service";

// Páginas
import HomePage from "@/pages/HomePage";

// Componentes
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

// Rutas protegidas
const ProtectedRoute = ({ children, allowedRoles }) => {
  const session = getCurrentSession();
  
  if (!session) {
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles && !allowedRoles.includes(session.role)) {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

function App() {
  const [session, setSession] = useState(null);
  
  useEffect(() => {
    // Inicializar usuarios predefinidos
    initializeUsers();
    
    // Verificar si hay una sesión activa
    const currentSession = getCurrentSession();
    setSession(currentSession);
  }, []);
  
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar session={session} setSession={setSession} />
        
        <motion.main 
          className="flex-grow"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </motion.main>
        
        <Footer />
        <Toaster />
      </div>
    </Router>
  );
}

export default App;
