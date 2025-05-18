import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Outdent as Tooth } from 'lucide-react';


const servicesData = [
  {
    icon: <Tooth className="h-10 w-10 text-indigo-500" />,
    title: "Limpieza Dental",
    description: "Eliminamos la placa y el sarro para mantener tus dientes sanos y brillantes."
  },
  {
    icon: <Tooth className="h-10 w-10 text-indigo-500" />,
    title: "Tratamiento de Caries",
    description: "Restauramos tus dientes dañados con los mejores materiales."
  },
  {
    icon: <Tooth className="h-10 w-10 text-indigo-500" />,
    title: "Blanqueamiento",
    description: "Devuelve el brillo a tu sonrisa con nuestros tratamientos de blanqueamiento."
  },
  {
    icon: <Tooth className="h-10 w-10 text-indigo-500" />,
    title: "Ortodoncia",
    description: "Alineamos tus dientes para una sonrisa perfecta y una mordida saludable."
  }
];

const ServicesSection = () => {
  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Nuestros Servicios</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Ofrecemos una amplia gama de servicios dentales para mantener tu sonrisa saludable y radiante.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {servicesData.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <Card className="h-full hover:shadow-lg transition-shadow">
                <CardContent className="p-6 text-center">
                  <div className="mb-4 flex justify-center">
                    {service.icon}
                  </div>
                  <h3 className="text-xl font-bold mb-2">{service.title}</h3>
                  <p className="text-gray-600">{service.description}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;
