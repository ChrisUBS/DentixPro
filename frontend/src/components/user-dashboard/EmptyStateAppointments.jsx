
import React from "react";
import { Link } from "react-router-dom";
import { Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";

const EmptyStateAppointments = ({ type }) => {
  const messages = {
    upcoming: {
      title: "No tienes citas próximas",
      description: "Agenda una nueva cita para comenzar a cuidar tu salud dental",
      buttonText: "Agendar Cita",
      linkTo: "/agendar-cita"
    },
    past: {
      title: "No tienes historial de citas",
      description: "Tu historial de citas aparecerá aquí una vez que hayas completado alguna cita",
      buttonText: null
    }
  };

  const message = messages[type] || messages.upcoming;

  return (
    <div className="text-center py-12">
      <div className="flex justify-center mb-4">
        <Calendar className="h-12 w-12 text-gray-400" />
      </div>
      <h3 className="text-xl font-medium mb-2">{message.title}</h3>
      <p className="text-gray-600 mb-6">{message.description}</p>
      {message.buttonText && (
        <Link to={message.linkTo}>
          <Button>
            <Calendar className="mr-2 h-4 w-4" />
            {message.buttonText}
          </Button>
        </Link>
      )}
    </div>
  );
};

export default EmptyStateAppointments;
