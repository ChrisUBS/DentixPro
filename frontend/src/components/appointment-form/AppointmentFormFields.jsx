import React from "react";
import { Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { format } from "date-fns";
import { es } from "date-fns/locale";

// Textarea personalizado
const Textarea = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <textarea
      className={`flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
      ref={ref}
      {...props}
    />
  );
});
Textarea.displayName = "Textarea";

// Utilidad local para formatear la fecha
const formatAppointmentDate = (dateString) =>
  format(new Date(dateString), "EEEE d 'de' MMMM 'de' yyyy", { locale: es });

const AppointmentFormFields = ({
  formData,
  onFieldChange,
  availableTimes,
  isSubmitting,
  onSubmit,
  services, // ✅ nueva prop
}) => {
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="service">Servicio Dental</Label>
        <Select
          value={formData.serviceId}
          onValueChange={(value) => onFieldChange("serviceId", value)}
        >
          <SelectTrigger>
            <SelectValue placeholder="Selecciona un servicio" />
          </SelectTrigger>
          <SelectContent>
            {services.map((service) => (
              <SelectItem key={service.id} value={service.id.toString()}>
                {service.name} ({service.duration} min)
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="date">Fecha</Label>
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="date"
            type="date"
            className="pl-10"
            min={new Date().toISOString().split("T")[0]}
            value={formData.date}
            onChange={(e) => onFieldChange("date", e.target.value)}
            required
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="time">Hora</Label>
        <Select
          value={formData.time}
          onValueChange={(value) => onFieldChange("time", value)}
          disabled={!formData.date}
        >
          <SelectTrigger>
            <SelectValue
              placeholder={
                formData.date
                  ? "Selecciona una hora"
                  : "Primero selecciona una fecha"
              }
            />
          </SelectTrigger>
          <SelectContent>
            {availableTimes.length > 0 ? (
              availableTimes.map((time) => (
                <SelectItem key={time} value={time}>
                  {time} hrs
                </SelectItem>
              ))
            ) : (
              <SelectItem value="" disabled>
                No hay horarios disponibles
              </SelectItem>
            )}
          </SelectContent>
        </Select>
        {formData.date &&
          availableTimes.length === 0 &&
          !formData.time && (
            <p className="text-sm text-red-500 mt-1">
              No hay horarios disponibles para esta fecha. Por favor, selecciona otra fecha.
            </p>
          )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="notes">Notas Adicionales (Opcional)</Label>
        <Textarea
          id="notes"
          placeholder="Describe brevemente tu motivo de consulta o cualquier información relevante..."
          value={formData.description}
          onChange={(e) => onFieldChange("description", e.target.value)}
        />
      </div>

      {formData.serviceId && formData.date && formData.time && (
        <div className="bg-blue-50 p-4 rounded-md border border-blue-100">
          <h3 className="font-medium text-blue-800 mb-2">Resumen de la Cita</h3>
          <div className="space-y-1 text-sm text-blue-700">
            <p>
              <span className="font-medium">Servicio:</span>{" "}
              {services.find((s) => s.id.toString() === formData.serviceId)?.name}
            </p>
            <p>
              <span className="font-medium">Fecha:</span>{" "}
              {formData.date && formatAppointmentDate(formData.date)}
            </p>
            <p>
              <span className="font-medium">Hora:</span> {formData.time} hrs
            </p>
          </div>
        </div>
      )}

      <Button
        type="submit"
        className="w-full"
        disabled={
          isSubmitting ||
          !formData.serviceId ||
          !formData.date ||
          !formData.time
        }
      >
        {isSubmitting ? (
          <div className="flex items-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Agendando cita...
          </div>
        ) : (
          <div className="flex items-center">
            <Calendar className="mr-2 h-4 w-4" />
            Agendar Cita
          </div>
        )}
      </Button>
    </form>
  );
};

export default AppointmentFormFields;
