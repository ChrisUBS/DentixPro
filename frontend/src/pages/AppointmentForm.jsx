import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import AppointmentFormFields from "@/components/appointment-form/AppointmentFormFields";
import AppointmentSuccessMessage from "@/components/appointment-form/AppointmentSuccessMessage";
import { useAuth } from "@/contexts/AuthContext";
import { dateService } from "@/services/api";

const dentalServices = [
  { id: 1, name: "Limpieza dental", duration: 30 },
  { id: 2, name: "Revisión general", duration: 20 },
  { id: 3, name: "Extracción dental", duration: 45 },
  { id: 4, name: "Tratamiento de caries", duration: 40 },
  { id: 5, name: "Blanqueamiento dental", duration: 60 },
  { id: 6, name: "Ortodoncia", duration: 30 },
  { id: 7, name: "Radiografía dental", duration: 15 },
  { id: 8, name: "Endodoncia", duration: 90 },
];

const availableTimeSlots = [
  "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
  "12:00", "12:30", "13:00", "15:00", "15:30",
  "16:00", "16:30", "17:00", "17:30", "18:00"
];

const AppointmentForm = () => {
  const initialFormData = {
    serviceId: "",
    date: "",
    time: "",
    description: "",
  };

  const [formData, setFormData] = useState(initialFormData);
  const [availableTimes, setAvailableTimes] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const { toast } = useToast();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    if (formData.date) {
      setAvailableTimes(availableTimeSlots);
    } else {
      setAvailableTimes([]);
    }
  }, [formData.date]);

  const handleFieldChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    if (!formData.serviceId || !formData.date || !formData.time) {
      toast({
        title: "Error",
        description: "Por favor, completa todos los campos requeridos",
        variant: "destructive",
      });
      setIsSubmitting(false);
      return;
    }

    const appointment = {
      title: dentalServices.find(s => s.id.toString() === formData.serviceId)?.name || "Sin título",
      date: formData.date,
      time: formData.time,
      description: formData.description,
    };


    try {
      await dateService.createDate(appointment);

      toast({
        title: "Cita agendada",
        description: "Tu cita ha sido agendada correctamente",
      });

      setIsSuccess(true);
      setFormData(initialFormData);
    } catch (error) {
      toast({
        title: "Error",
        description:
          error.response?.data?.msg || "Error al agendar la cita. Inténtalo más tarde.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBookAnother = () => {
    setIsSuccess(false);
    setFormData(initialFormData);
  };

  if (isSuccess) {
    return <AppointmentSuccessMessage onBookAnother={handleBookAnother} />;
  }

  return (
    <div className="container max-w-2xl mx-auto py-10 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Agendar Cita</h1>
          <p className="text-gray-600">
            Completa el formulario para agendar tu cita dental
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Información de la Cita</CardTitle>
            <CardDescription>
              Selecciona el servicio, fecha y hora para tu cita
            </CardDescription>
          </CardHeader>
          <CardContent>
            <AppointmentFormFields
              formData={formData}
              onFieldChange={handleFieldChange}
              availableTimes={availableTimes}
              isSubmitting={isSubmitting}
              onSubmit={handleSubmit}
              services={dentalServices}
            />
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default AppointmentForm;
