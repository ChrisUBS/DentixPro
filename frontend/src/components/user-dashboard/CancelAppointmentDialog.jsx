
import React from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { AlertCircle } from "lucide-react";

const CancelAppointmentDialog = ({ isOpen, onOpenChange, onConfirm }) => {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Cancelar Cita</DialogTitle>
          <DialogDescription>
            ¿Estás seguro de que deseas cancelar esta cita? Esta acción no se puede deshacer.
          </DialogDescription>
        </DialogHeader>
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 flex items-start">
          <AlertCircle className="h-5 w-5 text-yellow-600 mr-3 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-yellow-800">Importante</h4>
            <p className="text-sm text-yellow-700 mt-1">
              Te recomendamos cancelar con al menos 24 horas de anticipación para permitir que otros pacientes puedan agendar en ese horario.
            </p>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Volver
          </Button>
          <Button variant="destructive" onClick={onConfirm}>
            Sí, cancelar cita
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default CancelAppointmentDialog;
