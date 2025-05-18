
import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Outdent as Tooth, Home } from "lucide-react";
import { Button } from "@/components/ui/button";

const NotFoundPage = () => {
  return (
    <div className="container mx-auto py-20 px-4 text-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md mx-auto"
      >
        <div className="mb-8">
          <motion.div
            animate={{ 
              rotate: [0, 10, -10, 10, 0],
              scale: [1, 1.1, 1]
            }}
            transition={{ 
              duration: 2,
              repeat: Infinity,
              repeatType: "reverse"
            }}
            className="inline-block"
          >
            <Tooth className="h-24 w-24 text-primary mx-auto" />
          </motion.div>
        </div>
        
        <h1 className="text-4xl font-bold mb-4">Página no encontrada</h1>
        
        <p className="text-xl text-gray-600 mb-8">
          Lo sentimos, la página que estás buscando no existe o ha sido movida.
        </p>
        
        <Link to="/">
          <Button size="lg" className="gap-2">
            <Home className="h-5 w-5" />
            Volver al inicio
          </Button>
        </Link>
      </motion.div>
    </div>
  );
};

export default NotFoundPage;
