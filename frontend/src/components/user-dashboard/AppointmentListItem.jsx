import React from "react";
import { motion } from "framer-motion";
import { Calendar, Clock, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { formatAppointmentDate } from "@/lib/appointment-service";

const AppointmentListItem = ({ appointment, onCancel, type }) => {
  const serviceName = appointment.title || "Servicio no disponible";
  const notes = appointment.description || "";

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case "pendiente":
        return "bg-yellow-100 text-yellow-800";
      case "completada":
        return "bg-green-100 text-green-800";
      case "cancelada":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case "pending":
        return "Pendiente";
      case "completed":
        return "Completada";
      case "cancelled":
        return "Cancelada";
      default:
        return status;
    }
  };

  const cardBorderClass =
    type === "upcoming"
      ? "border-l-primary"
      : appointment.status === "completed"
      ? "border-l-green-500"
      : appointment.status === "cancelled"
      ? "border-l-red-500"
      : "border-l-gray-500";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={`overflow-hidden border-l-4 ${cardBorderClass}`}>
        <CardContent className="p-0">
          <div className={`grid grid-cols-1 ${type === "upcoming" ? "md:grid-cols-4" : ""} gap-4`}>
            <div className={`p-6 ${type === "upcoming" ? "md:col-span-3" : ""}`}>
              <div className="flex items-center mb-2">
                <span
                  className={`text-xs font-medium px-2.5 py-0.5 rounded-full ${getStatusBadgeClass(
                    appointment.status
                  )}`}
                >
                  {getStatusText(appointment.status)}
                </span>
              </div>
              <h3 className="text-xl font-bold mb-2">
                {serviceName}
              </h3>
              <div className="flex items-center text-gray-600 mb-2">
                <Calendar className="h-4 w-4 mr-2" />
                <span>{formatAppointmentDate(appointment.date)}</span>
              </div>
              <div className="flex items-center text-gray-600">
                <Clock className="h-4 w-4 mr-2" />
                <span>{appointment.time} hrs</span>
              </div>
              {type === "upcoming" && notes && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md">
                  <p className="text-sm text-gray-600">{notes}</p>
                </div>
              )}
            </div>
            {type === "upcoming" && (
              <div className="bg-gray-50 p-6 flex flex-col justify-center items-center">
                <Button
                  variant="outline"
                  className="w-full text-red-600 border-red-200 hover:bg-red-50 hover:text-red-700"
                  onClick={() => onCancel(appointment)}
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Cancelar
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default AppointmentListItem;
