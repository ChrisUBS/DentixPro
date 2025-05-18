import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import { useAuth } from "@/contexts/AuthContext";
import { userService, dateService } from "@/services/api";
import AppointmentListItem from "@/components/user-dashboard/AppointmentListItem";
import EmptyStateAppointments from "@/components/user-dashboard/EmptyStateAppointments";
import CancelAppointmentDialog from "@/components/user-dashboard/CancelAppointmentDialog";

const UserDashboard = () => {
  const [appointments, setAppointments] = useState([]);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      loadAppointments();
    }
  }, [user]);

  const loadAppointments = async () => {
    try {
      setLoading(true);
      const data = await userService.getUserDates();

      setAppointments(data.data);
    } catch (error) {
      toast({
        title: "Error al cargar citas",
        description: "No se pudieron obtener tus citas. Intenta más tarde.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmCancel = async () => {
    if (selectedAppointment) {
      try {
        await dateService.cancelDate(selectedAppointment._id);
        toast({
          title: "Cita cancelada",
          description: "Tu cita ha sido cancelada correctamente",
        });
        setIsDialogOpen(false);
        setSelectedAppointment(null);
        await loadAppointments();
      } catch (error) {
        toast({
          title: "Error al cancelar cita",
          description: "No se pudo cancelar la cita. Intenta más tarde.",
          variant: "destructive",
        });
      }
    }
  };

  const openCancelDialog = (appointment) => {
    setSelectedAppointment(appointment);
    setIsDialogOpen(true);
  };

  // Obtener fecha de hoy sin hora
  const today = new Date().toISOString().split("T")[0];

  const upcomingAppointments = appointments.filter((appointment) => {
    const appointmentDate = appointment.date;
    return (
      appointment.status === "pending" &&
      appointmentDate >= today
    );
  });

  const pastAppointments = appointments.filter((appointment) => {
    const appointmentDate = appointment.date;
    return (
      appointment.status === "completed" ||
      appointment.status === "cancelled" ||
      (appointment.status === "pending" && appointmentDate < today)
    );
  });

  return (
    <div className="container mx-auto py-10 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-4xl mx-auto"
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Mis Citas</h1>
            <p className="text-gray-600">Gestiona tus citas dentales desde aquí</p>
          </div>
          <Link to="/agendar-cita">
            <Button className="mt-4 md:mt-0">
              <Calendar className="mr-2 h-4 w-4" />
              Nueva Cita
            </Button>
          </Link>
        </div>

        <Tabs defaultValue="upcoming" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="upcoming" className="text-center">
              Próximas Citas
              {upcomingAppointments.length > 0 && (
                <span className="ml-2 bg-primary text-white text-xs rounded-full px-2 py-1">
                  {upcomingAppointments.length}
                </span>
              )}
            </TabsTrigger>
            <TabsTrigger value="past" className="text-center">
              Historial de Citas
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upcoming" className="space-y-4">
            {loading ? (
              <p>Cargando citas...</p>
            ) : upcomingAppointments.length > 0 ? (
              upcomingAppointments.map((appointment) => (
                <AppointmentListItem
                  key={appointment.id}
                  appointment={appointment}
                  onCancel={openCancelDialog}
                  type="upcoming"
                />
              ))
            ) : (
              <EmptyStateAppointments type="upcoming" />
            )}
          </TabsContent>

          <TabsContent value="past" className="space-y-4">
            {loading ? (
              <p>Cargando citas...</p>
            ) : pastAppointments.length > 0 ? (
              pastAppointments.map((appointment) => (
                <AppointmentListItem
                  key={appointment.id}
                  appointment={appointment}
                  type="past"
                />
              ))
            ) : (
              <EmptyStateAppointments type="past" />
            )}
          </TabsContent>
        </Tabs>
      </motion.div>

      <CancelAppointmentDialog
        isOpen={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        onConfirm={handleConfirmCancel}
      />
    </div>
  );
};

export default UserDashboard;
