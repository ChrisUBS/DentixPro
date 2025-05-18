import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Calendar } from 'lucide-react';

const CtaSection = ({ user }) => {
  return (
    <section className="py-16 bg-gradient-to-r from-indigo-600 to-cyan-600 text-white">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-3xl font-bold mb-6">¿Listo para una sonrisa más saludable?</h2>
        <p className="text-xl mb-8 max-w-2xl mx-auto">
          Agenda tu cita ahora y da el primer paso hacia una mejor salud dental.
        </p>
        
        {user ? (
          user.rol === "user" ? (
            <Link to="/agendar-cita">
              <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
                <Calendar className="mr-2 h-5 w-5" />
                Agendar Cita
              </Button>
            </Link>
          ) : (
            <Link to="/admin">
              <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
                Panel de Administración
              </Button>
            </Link>
          )
        ) : (
          <Link to="/login">
            <Button size="lg" className="bg-white text-indigo-600 hover:bg-gray-100">
              Iniciar Sesión
            </Button>
          </Link>
        )}
      </div>
    </section>
  );
};

export default CtaSection;
