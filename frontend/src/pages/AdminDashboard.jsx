import React, { useState, useEffect, useMemo } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Calendar, Clock, CheckCircle, XCircle } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useToast } from "@/components/ui/use-toast";
import { dateService, userService } from "@/services/api";
import { useAuth } from "@/contexts/AuthContext";
import { formatAppointmentDate } from "@/lib/appointment-service";

import SummaryCard from "@/components/admin-dashboard/SummaryCard";
import AdminFilters from "@/components/admin-dashboard/AdminFilters";
import AdminAppointmentItem from "@/components/admin-dashboard/AdminAppointmentItem";
import EmptyStateAdminAppointments from "@/components/admin-dashboard/EmptyStateAdminAppointments";
import UpdateStatusDialog from "@/components/admin-dashboard/UpdateStatusDialog";

const AdminDashboard = () => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const [allAppointments, setAllAppointments] = useState([]);
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogAction, setDialogAction] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [activeTab, setActiveTab] = useState("all");

  // Redirige si no es administrador
  useEffect(() => {
    if (!loading && (!isAuthenticated || !isAdmin())) {
      toast({
        title: "Acceso denegado",
        description: "Necesitas ser administrador para acceder al panel.",
        variant: "destructive",
      });
      navigate("/login");
    }
  }, [loading, isAuthenticated, isAdmin, navigate]);

  // Carga las citas al iniciar
  useEffect(() => {
    if (!loading && isAuthenticated && isAdmin()) {
      loadData();
    }
  }, [loading, isAuthenticated, isAdmin]);

  const translateStatus = (status) => {
    switch (status) {
      case "pending":
        return "pendiente";
      case "completed":
        return "completada";
      case "cancelled":
        return "cancelada";
      default:
        return status;
    }
  };

  const loadData = async () => {
    try {
      // Obtener citas y usuarios
      const appointmentsData = await dateService.getAllDates(1, 1000);
      const usersData = await userService.getAllUsers(1, 1000);
      
      // Crear mapa de usuarios por ID
      const userMap = {};
      for (const user of usersData.data || []) {
        userMap[user.userId] = user;
      }

      // Normalizar citas con info de usuario
      const normalized = (appointmentsData.data || []).map((app) => {
        const user = userMap[app.userId];

        return {
          ...app,
          id: app.userId,
          status: translateStatus(app.status),
          userName: user?.name || "Usuario desconocido",
          userEmail: user?.email || "Email no disponible",
        };
      });

      setAllAppointments(normalized);
    } catch (error) {
      console.error("Error al cargar citas o usuarios:", error);
      toast({
        title: "Error al cargar datos",
        description: "No se pudieron cargar las citas o los usuarios.",
        variant: "destructive",
      });
    }
  };

  // Filtrar citas
  useEffect(() => {
    let filtered = [...allAppointments];

    if (activeTab === "today") {
      const today = new Date().toISOString().split("T")[0];
      filtered = filtered.filter((app) => app.date === today);
    } else if (activeTab === "upcoming") {
      const today = new Date();
      filtered = filtered.filter(
        (app) => new Date(app.date) > today && app.status === "pendiente"
      );
    } else if (activeTab === "completed") {
      filtered = filtered.filter((app) => app.status === "completada");
    } else if (activeTab === "cancelled") {
      filtered = filtered.filter((app) => app.status === "cancelada");
    }

    if (statusFilter !== "all") {
      filtered = filtered.filter((app) => app.status === statusFilter);
    }

    console.log(filtered)

    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(
        (app) =>
          app.title.toLowerCase().includes(term) ||
          app.userName.toLowerCase().includes(term) ||
          app.userEmail.toLowerCase().includes(term) ||
          formatAppointmentDate(app.date).toLowerCase().includes(term)
      );
    }

    filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
    setFilteredAppointments(filtered);
  }, [allAppointments, searchTerm, statusFilter, activeTab]);

  const handleConfirmStatusChange = async () => {
    console.log(selectedAppointment);
    if (selectedAppointment && dialogAction) {
      try {
        if (dialogAction === "complete") {
          await dateService.completeDate(selectedAppointment._id);
        } else if (dialogAction === "cancel") {
          await dateService.CancelDate(selectedAppointment._id);
        }

        await loadData();

        toast({
          title: "Estado actualizado",
          description: `La cita ha sido marcada como ${dialogAction === "complete" ? "completada" : "cancelada"}.`,
        });
      } catch (error) {
        toast({
          title: "Error",
          description: "No se pudo actualizar el estado de la cita.",
          variant: "destructive",
        });
      } finally {
        setIsDialogOpen(false);
        setSelectedAppointment(null);  
      }
    }
  };

  const openDialog = (appointment, action) => {
    setSelectedAppointment(appointment);
    setDialogAction(action);
    setIsDialogOpen(true);
  };

  const summaryStats = useMemo(() => {
    const today = new Date().toISOString().split("T")[0];
    return {
      total: allAppointments.length,
      today: allAppointments.filter((app) => app.date === today).length,
      upcoming: allAppointments.filter(
        (app) => new Date(app.date) > new Date() && app.status === "pendiente"
      ).length,
      completed: allAppointments.filter((app) => app.status === "completada").length,
      cancelled: allAppointments.filter((app) => app.status === "cancelada").length,
    };
  }, [allAppointments]);

  const renderAppointmentsList = (appointmentsToRender) => {
    if (appointmentsToRender.length === 0) {
      return <EmptyStateAdminAppointments />;
    }

    return appointmentsToRender.map((appointment) => (
      <AdminAppointmentItem
        key={appointment.id}
        appointment={appointment}
        onOpenDialog={openDialog}
      />
    ));
  };

  if (loading) return <p className="p-4 text-gray-600">Cargando...</p>;

  return (
    <div className="container mx-auto py-10 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Panel de Administración</h1>
          <p className="text-gray-600">Gestiona todas las citas del consultorio dental</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <SummaryCard title="Total de Citas" value={summaryStats.total} icon={<Calendar />} gradientFrom="from-blue-50" gradientTo="to-blue-100" borderColor="border-blue-200" textColor="text-blue-700" iconBgColor="bg-blue-200" iconColor="text-blue-700" />
          <SummaryCard title="Citas Próximas" value={summaryStats.upcoming} icon={<Clock />} gradientFrom="from-yellow-50" gradientTo="to-yellow-100" borderColor="border-yellow-200" textColor="text-yellow-700" iconBgColor="bg-yellow-200" iconColor="text-yellow-700" />
          <SummaryCard title="Citas Completadas" value={summaryStats.completed} icon={<CheckCircle />} gradientFrom="from-green-50" gradientTo="to-green-100" borderColor="border-green-200" textColor="text-green-700" iconBgColor="bg-green-200" iconColor="text-green-700" />
          <SummaryCard title="Citas Canceladas" value={summaryStats.cancelled} icon={<XCircle />} gradientFrom="from-red-50" gradientTo="to-red-100" borderColor="border-red-200" textColor="text-red-700" iconBgColor="bg-red-200" iconColor="text-red-700" />
        </div>

        <AdminFilters
          searchTerm={searchTerm}
          onSearchTermChange={setSearchTerm}
          statusFilter={statusFilter}
          onStatusFilterChange={setStatusFilter}
        />

        <Tabs defaultValue="all" onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 sm:grid-cols-3 md:grid-cols-5 mb-8">
            <TabsTrigger value="all">Todas ({summaryStats.total})</TabsTrigger>
            <TabsTrigger value="today">Hoy ({summaryStats.today})</TabsTrigger>
            <TabsTrigger value="upcoming">Próximas ({summaryStats.upcoming})</TabsTrigger>
            <TabsTrigger value="completed">Completadas ({summaryStats.completed})</TabsTrigger>
            <TabsTrigger value="cancelled">Canceladas ({summaryStats.cancelled})</TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="space-y-4">{renderAppointmentsList(filteredAppointments)}</TabsContent>
          <TabsContent value="today" className="space-y-4">{renderAppointmentsList(filteredAppointments)}</TabsContent>
          <TabsContent value="upcoming" className="space-y-4">{renderAppointmentsList(filteredAppointments)}</TabsContent>
          <TabsContent value="completed" className="space-y-4">{renderAppointmentsList(filteredAppointments)}</TabsContent>
          <TabsContent value="cancelled" className="space-y-4">{renderAppointmentsList(filteredAppointments)}</TabsContent>
        </Tabs>
      </motion.div>

      <UpdateStatusDialog
        isOpen={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        appointment={selectedAppointment}
        action={dialogAction}
        onConfirm={handleConfirmStatusChange}
      />
    </div>
  );
};

export default AdminDashboard;
