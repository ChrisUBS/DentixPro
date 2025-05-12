
import React from "react";
import { motion } from "framer-motion";

const testimonialsData = [
  {
    name: "María Pérez",
    role: "Paciente desde 2020",
    initials: "MP",
    quote: "Excelente atención y profesionalismo. El sistema de citas online es muy conveniente y me ha facilitado mucho la gestión de mis visitas al dentista."
  },
  {
    name: "Juan Rodríguez",
    role: "Paciente desde 2019",
    initials: "JR",
    quote: "Los doctores son muy amables y explican todo el procedimiento detalladamente. Me encanta poder ver mis citas programadas en línea."
  },
  {
    name: "Ana López",
    role: "Paciente desde 2021",
    initials: "AL",
    quote: "Muy satisfecha con el tratamiento recibido. El sistema de citas es muy intuitivo y me permite gestionar mis visitas de manera eficiente."
  }
];

const TestimonialsSection = () => {
  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Lo que dicen nuestros pacientes</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            La satisfacción de nuestros pacientes es nuestro mayor orgullo.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonialsData.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="bg-white p-6 rounded-lg shadow-md"
            >
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4">
                  <span className="text-indigo-600 font-bold">{testimonial.initials}</span>
                </div>
                <div>
                  <h4 className="font-bold">{testimonial.name}</h4>
                  <p className="text-gray-600 text-sm">{testimonial.role}</p>
                </div>
              </div>
              <p className="text-gray-600">{testimonial.quote}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
