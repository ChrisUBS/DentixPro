import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Calendar } from 'lucide-react';
import { Button } from "@/components/ui/button";

const HeroSection = ({ user }) => {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 dental-gradient opacity-90 z-0"></div>
      <div className="absolute inset-0 tooth-pattern z-0"></div>
      
      <div className="container relative z-10 px-4 py-20 md:py-32 mx-auto text-center text-white">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto"
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Tu Sonrisa, Nuestra Prioridad
          </h1>
          <p className="text-xl md:text-2xl mb-8 opacity-90">
            Sistema de gestión de citas para nuestro consultorio dental. Agenda tu cita de manera fácil y rápida.
          </p>
          
          {user ? (
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {user.rol === "admin" ? (
                <Link to="/admin">
                  <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
                    Panel de Administración
                  </Button>
                </Link>
              ) : (
                <>
                  <Link to="/agendar-cita">
                    <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
                      <Calendar className="mr-2 h-5 w-5" />
                      Agendar Cita
                    </Button>
                  </Link>
                  <Link to="/dashboard">
                    <Button size="lg" variant="outline" className="bg-white text-indigo-600 hover:bg-gray-100">
                      Ver Mis Citas
                    </Button>
                  </Link>
                </>
              )}
            </div>
          ) : (
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/login">
                <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
                  Iniciar Sesión
                </Button>
              </Link>
              <Link to="/register">
                <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
                  Registrarse
                </Button>
              </Link>
            </div>
          )}
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;
