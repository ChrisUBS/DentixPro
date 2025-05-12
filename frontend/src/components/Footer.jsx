
import React from "react";
import { Outdent as Tooth, Phone, Mail, MapPin, Clock } from 'lucide-react';
import { motion } from "framer-motion";

const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-indigo-600 to-cyan-600 text-white">
      <div className="container mx-auto py-12 px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Información de contacto */}
          <div>
            <div className="flex items-center mb-4">
              <motion.div
                whileHover={{ rotate: 20 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Tooth className="h-6 w-6 mr-2" />
              </motion.div>
              <h3 className="text-xl font-bold">DentixPro</h3>
            </div>
            <p className="mb-4">
              Cuidamos de tu sonrisa con los mejores profesionales y la tecnología más avanzada.
            </p>
            <ul className="space-y-2">
              <li className="flex items-center">
                <Phone className="h-5 w-5 mr-2" />
                <span>(123) 456-7890</span>
              </li>
              <li className="flex items-center">
                <Mail className="h-5 w-5 mr-2" />
                <span>contacto@dentixpro.com</span>
              </li>
              <li className="flex items-center">
                <MapPin className="h-5 w-5 mr-2" />
                <span>Av. Principal #123, Ciudad</span>
              </li>
            </ul>
          </div>

          {/* Horario */}
          <div>
            <h3 className="text-xl font-bold mb-4">Horario de Atención</h3>
            <ul className="space-y-2">
              <li className="flex items-center">
                <Clock className="h-5 w-5 mr-2" />
                <div>
                  <span className="font-medium">Lunes a Viernes:</span>
                  <p>9:00 AM - 7:00 PM</p>
                </div>
              </li>
              <li className="flex items-center">
                <Clock className="h-5 w-5 mr-2" />
                <div>
                  <span className="font-medium">Sábados:</span>
                  <p>9:00 AM - 2:00 PM</p>
                </div>
              </li>
              <li className="flex items-center">
                <Clock className="h-5 w-5 mr-2" />
                <div>
                  <span className="font-medium">Domingos:</span>
                  <p>Cerrado</p>
                </div>
              </li>
            </ul>
          </div>

          {/* Enlaces rápidos */}
          <div>
            <h3 className="text-xl font-bold mb-4">Enlaces Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="hover:underline">Inicio</a>
              </li>
              <li>
                <a href="/login" className="hover:underline">Iniciar Sesión</a>
              </li>
              <li>
                <a href="/register" className="hover:underline">Registrarse</a>
              </li>
              <li>
                <a href="/agendar-cita" className="hover:underline">Agendar Cita</a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white/20 mt-8 pt-8 text-center">
          <p>&copy; {new Date().getFullYear()} DentixPro. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
