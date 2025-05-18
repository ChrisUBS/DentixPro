import React from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Separator } from "@/components/ui/separator";
import { formatAppointmentDate } from "@/lib/appointment-service"; // O tu nuevo formateador

const UpdateStatusDialog = ({ isOpen, onOpenChange, appointment, action, onConfirm }) => {
  if (!appointment) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {action === "complete" ? "Completar Cita" : "Cancelar Cita"}
          </DialogTitle>
          <DialogDescription>
            {action === "complete"
              ? "¿Estás seguro de que deseas marcar esta cita como completada?"
              : "¿Estás seguro de que deseas cancelar esta cita?"}
          </DialogDescription>
        </DialogHeader>

        <div className="bg-gray-50 p-4 rounded-md">
          <p className="font-medium">{appointment.userName}</p>
          <p className="text-sm text-gray-600">{appointment.userEmail}</p>
          <Separator className="my-2" />
          <p className="text-sm">
            <span className="font-medium">Fecha:</span>{" "}
            {formatAppointmentDate(appointment.date)}
          </p>
          <p className="text-sm">
            <span className="font-medium">Hora:</span> {appointment.time} hrs
          </p>
          <p className="text-sm">
            <span className="font-medium">Servicio:</span>{" "}
            {appointment.title || "No disponible"}
          </p>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Volver
          </Button>
          <Button
            variant={action === "complete" ? "default" : "destructive"}
            onClick={onConfirm}
          >
            {action === "complete" ? "Sí, completar" : "Sí, cancelar"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default UpdateStatusDialog;
