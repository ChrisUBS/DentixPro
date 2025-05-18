import React from "react";
import { motion } from "framer-motion";
import { Calendar, Clock, CheckCircle, XCircle, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { formatAppointmentDate } from "@/lib/appointment-service";

const AdminAppointmentItem = ({ appointment, onOpenDialog }) => {
  const isPast = new Date(appointment.date) < new Date() && appointment.status === "pendiente";

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case "pendiente": return "bg-yellow-100 text-yellow-800";
      case "completada": return "bg-green-100 text-green-800";
      case "cancelada": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case "pendiente": return "Pendiente";
      case "completada": return "Completada";
      case "cancelada": return "Cancelada";
      default: return status;
    }
  };

  const cardBorderClass =
    appointment.status === "completada"
      ? "border-l-green-500"
      : appointment.status === "cancelada"
        ? "border-l-red-500"
        : "border-l-primary";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={`overflow-hidden border-l-4 ${cardBorderClass}`}>
        <CardContent className="p-0">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-6 md:col-span-3">
              <div className="flex flex-wrap items-center gap-2 mb-3">
                <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full ${getStatusBadgeClass(appointment.status)}`}>
                  {getStatusText(appointment.status)}
                </span>
                {isPast && (
                  <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-red-100 text-red-800">
                    Vencida
                  </span>
                )}
              </div>

              <div className="flex items-start gap-3 mb-4">
                <div className="bg-gray-100 p-2 rounded-full">
                  <User className="h-5 w-5 text-gray-600" />
                </div>
                <div>
                  <h3 className="font-bold">
                    {appointment.userName || "Usuario desconocido"}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {appointment.userEmail || "Email no disponible"}
                  </p>
                </div>
              </div>

              <h4 className="text-lg font-semibold mb-2">
                {appointment.title || "Servicio no disponible"}
              </h4>

              <div className="flex items-center text-gray-600 mb-2">
                <Calendar className="h-4 w-4 mr-2" />
                <span>{formatAppointmentDate(appointment.date)}</span>
              </div>

              <div className="flex items-center text-gray-600">
                <Clock className="h-4 w-4 mr-2" />
                <span>{appointment.time} hrs</span>
              </div>

              {appointment.notes && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md">
                  <p className="text-sm text-gray-600">{appointment.notes}</p>
                </div>
              )}
            </div>

            <div className="bg-gray-50 p-6 flex flex-col justify-center items-center gap-3">
              {appointment.status === "pendiente" && (
                <>
                  <Button
                    className="w-full"
                    onClick={() => onOpenDialog(appointment, "complete")}
                  >
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Completar
                  </Button>
                  <Button
                    variant="outline"
                    className="w-full text-red-600 border-red-200 hover:bg-red-50 hover:text-red-700"
                    onClick={() => onOpenDialog(appointment, "cancel")}
                  >
                    <XCircle className="h-4 w-4 mr-2" />
                    Cancelar
                  </Button>
                </>
              )}

              {appointment.status === "completada" && (
                <div className="text-center">
                  <CheckCircle className="h-6 w-6 text-green-500 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Cita completada</p>
                </div>
              )}

              {appointment.status === "cancelada" && (
                <div className="text-center">
                  <XCircle className="h-6 w-6 text-red-500 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Cita cancelada</p>
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default AdminAppointmentItem;
