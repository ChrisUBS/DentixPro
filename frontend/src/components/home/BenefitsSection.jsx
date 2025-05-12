
import React from "react";
import { motion } from "framer-motion";
import { CheckCircle, Clock, Award, Users } from 'lucide-react';

const benefitsData = [
  {
    icon: <CheckCircle className="h-8 w-8 text-green-500" />,
    title: "Atención de Calidad",
    description: "Nuestros profesionales están altamente capacitados para brindarte el mejor servicio."
  },
  {
    icon: <Clock className="h-8 w-8 text-blue-500" />,
    title: "Horarios Flexibles",
    description: "Ofrecemos horarios que se adaptan a tus necesidades."
  },
  {
    icon: <Award className="h-8 w-8 text-yellow-500" />,
    title: "Tecnología Avanzada",
    description: "Contamos con equipos de última generación para diagnósticos precisos y tratamientos efectivos."
  },
  {
    icon: <Users className="h-8 w-8 text-purple-500" />,
    title: "Atención Personalizada",
    description: "Cada paciente es único, por eso ofrecemos tratamientos adaptados a tus necesidades específicas."
  }
];

const BenefitsSection = () => {
  return (
    <section className="py-16">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">¿Por qué elegirnos?</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Nos esforzamos por brindar la mejor atención dental con un enfoque centrado en el paciente.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {benefitsData.map((benefit, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              viewport={{ once: true }}
              className="flex items-start p-6 bg-white rounded-lg shadow-md"
            >
              <div className="mr-4 mt-1">{benefit.icon}</div>
              <div>
                <h3 className="text-xl font-bold mb-2">{benefit.title}</h3>
                <p className="text-gray-600">{benefit.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default BenefitsSection;
