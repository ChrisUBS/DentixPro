
import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const AppointmentSuccessMessage = ({ onBookAnother }) => {
  const navigate = useNavigate();

  return (
    <div className="container max-w-md mx-auto py-16 px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="border-2 border-green-200">
          <CardHeader className="text-center pb-2">
            <div className="mx-auto bg-green-100 p-3 rounded-full w-16 h-16 flex items-center justify-center mb-4">
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
            <CardTitle className="text-2xl font-bold text-green-700">¡Cita Agendada!</CardTitle>
            <CardDescription className="text-green-600">
              Tu cita ha sido agendada correctamente
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center pt-4">
            <p className="mb-6 text-gray-600">
              Puedes ver los detalles de tu cita en tu panel de usuario.
            </p>
            <div className="space-y-4">
              <Button
                onClick={() => navigate("/dashboard")}
                className="w-full"
              >
                Ver Mis Citas
              </Button>
              <Button
                variant="outline"
                onClick={onBookAnother}
                className="w-full"
              >
                Agendar Otra Cita
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default AppointmentSuccessMessage;
