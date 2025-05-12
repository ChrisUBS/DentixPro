
import React from "react";
import { Calendar } from "lucide-react";

const EmptyStateAdminAppointments = () => {
  return (
    <div className="text-center py-12 bg-gray-50 rounded-lg">
      <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <h3 className="text-xl font-medium mb-2">No hay citas para mostrar</h3>
      <p className="text-gray-600">
        No se encontraron citas que coincidan con los criterios de búsqueda o filtro.
      </p>
    </div>
  );
};

export default EmptyStateAdminAppointments;
