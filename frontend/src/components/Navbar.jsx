
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Outdent as Tooth, Menu, X, User, LogOut, Calendar, Home } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { logoutUser } from "@/lib/auth-service";
import { useToast } from "@/components/ui/use-toast";

const Navbar = ({ session, setSession }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    setSession(null);
    toast({
      title: "Sesión cerrada",
      description: "Has cerrado sesión correctamente",
    });
    navigate("/");
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <motion.div
            whileHover={{ rotate: 20 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <Tooth className="h-6 w-6 text-primary" />
          </motion.div>
          <span className="hidden font-bold sm:inline-block text-xl">
            DentixPro
          </span>
        </Link>

        {/* Menú de navegación para pantallas grandes */}
        <nav className="hidden md:flex items-center space-x-6">
          <Link
            to="/"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            Inicio
          </Link>
          
          {session ? (
            <>
              {session.role === "admin" ? (
                <Link
                  to="/admin"
                  className="text-sm font-medium transition-colors hover:text-primary"
                >
                  Panel de Administración
                </Link>
              ) : (
                <>
                  <Link
                    to="/dashboard"
                    className="text-sm font-medium transition-colors hover:text-primary"
                  >
                    Mis Citas
                  </Link>
                  <Link
                    to="/agendar-cita"
                    className="text-sm font-medium transition-colors hover:text-primary"
                  >
                    Agendar Cita
                  </Link>
                </>
              )}
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium">
                  Hola, {session.name}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-1"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="sr-only md:not-sr-only">Cerrar sesión</span>
                </Button>
              </div>
            </>
          ) : (
            <div className="flex items-center space-x-2">
              <Link to="/login">
                <Button variant="ghost" size="sm">
                  Iniciar sesión
                </Button>
              </Link>
              <Link to="/register">
                <Button>Registrarse</Button>
              </Link>
            </div>
          )}
        </nav>

        {/* Botón de menú para móviles */}
        <button
          className="md:hidden"
          onClick={toggleMenu}
          aria-label="Toggle menu"
        >
          {isMenuOpen ? (
            <X className="h-6 w-6" />
          ) : (
            <Menu className="h-6 w-6" />
          )}
        </button>
      </div>

      {/* Menú móvil */}
      {isMenuOpen && (
        <motion.div
          className="md:hidden"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className="container py-4 space-y-4">
            <Link
              to="/"
              className="flex items-center space-x-2 p-2 rounded-md hover:bg-accent"
              onClick={() => setIsMenuOpen(false)}
            >
              <Home className="h-5 w-5" />
              <span>Inicio</span>
            </Link>
            
            {session ? (
              <>
                {session.role === "admin" ? (
                  <Link
                    to="/admin"
                    className="flex items-center space-x-2 p-2 rounded-md hover:bg-accent"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <User className="h-5 w-5" />
                    <span>Panel de Administración</span>
                  </Link>
                ) : (
                  <>
                    <Link
                      to="/dashboard"
                      className="flex items-center space-x-2 p-2 rounded-md hover:bg-accent"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <Calendar className="h-5 w-5" />
                      <span>Mis Citas</span>
                    </Link>
                    <Link
                      to="/agendar-cita"
                      className="flex items-center space-x-2 p-2 rounded-md hover:bg-accent"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <Calendar className="h-5 w-5" />
                      <span>Agendar Cita</span>
                    </Link>
                  </>
                )}
                <div className="border-t pt-4">
                  <div className="px-2 mb-2 text-sm font-medium">
                    Hola, {session.name}
                  </div>
                  <Button
                    variant="ghost"
                    className="w-full justify-start"
                    onClick={() => {
                      handleLogout();
                      setIsMenuOpen(false);
                    }}
                  >
                    <LogOut className="h-5 w-5 mr-2" />
                    Cerrar sesión
                  </Button>
                </div>
              </>
            ) : (
              <div className="space-y-2">
                <Link
                  to="/login"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <Button variant="ghost" className="w-full justify-start">
                    <User className="h-5 w-5 mr-2" />
                    Iniciar sesión
                  </Button>
                </Link>
                <Link
                  to="/register"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <Button className="w-full">Registrarse</Button>
                </Link>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </header>
  );
};

export default Navbar;
