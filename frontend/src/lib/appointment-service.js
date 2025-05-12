
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

// Servicios dentales disponibles
export const dentalServices = [
  { id: 1, name: "Limpieza dental", duration: 30 },
  { id: 2, name: "Revisión general", duration: 20 },
  { id: 3, name: "Extracción dental", duration: 45 },
  { id: 4, name: "Tratamiento de caries", duration: 40 },
  { id: 5, name: "Blanqueamiento dental", duration: 60 },
  { id: 6, name: "Ortodoncia", duration: 30 },
  { id: 7, name: "Radiografía dental", duration: 15 },
  { id: 8, name: "Endodoncia", duration: 90 }
];

// Horarios disponibles
export const availableTimeSlots = [
  "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
  "12:00", "12:30", "13:00", "15:00", "15:30", 
  "16:00", "16:30", "17:00", "17:30", "18:00"
];

// Guardar una cita en localStorage
export const saveAppointment = (appointment) => {
  const appointments = getAppointments();
  
  // Generar un ID único para la cita
  const newAppointment = {
    ...appointment,
    id: Date.now().toString(),
    status: 'pendiente',
    createdAt: new Date().toISOString()
  };
  
  appointments.push(newAppointment);
  localStorage.setItem('dentalAppointments', JSON.stringify(appointments));
  
  return newAppointment;
};

// Obtener todas las citas
export const getAppointments = () => {
  const appointments = localStorage.getItem('dentalAppointments');
  return appointments ? JSON.parse(appointments) : [];
};

// Obtener citas de un usuario específico
export const getUserAppointments = (userId) => {
  const appointments = getAppointments();
  return appointments.filter(appointment => appointment.userId === userId);
};

// Actualizar el estado de una cita
export const updateAppointmentStatus = (appointmentId, newStatus) => {
  const appointments = getAppointments();
  const updatedAppointments = appointments.map(appointment => {
    if (appointment.id === appointmentId) {
      return { ...appointment, status: newStatus };
    }
    return appointment;
  });
  
  localStorage.setItem('dentalAppointments', JSON.stringify(updatedAppointments));
  return updatedAppointments.find(a => a.id === appointmentId);
};

// Cancelar una cita
export const cancelAppointment = (appointmentId) => {
  return updateAppointmentStatus(appointmentId, 'cancelada');
};

// Completar una cita
export const completeAppointment = (appointmentId) => {
  return updateAppointmentStatus(appointmentId, 'completada');
};

// Verificar si un horario está disponible
export const isTimeSlotAvailable = (date, timeSlot) => {
  const appointments = getAppointments();
  const formattedDate = format(new Date(date), 'yyyy-MM-dd');
  
  return !appointments.some(appointment => 
    format(new Date(appointment.date), 'yyyy-MM-dd') === formattedDate && 
    appointment.time === timeSlot &&
    appointment.status !== 'cancelada'
  );
};

// Formatear fecha para mostrar
export const formatAppointmentDate = (dateString) => {
  return format(new Date(dateString), "EEEE d 'de' MMMM 'de' yyyy", { locale: es });
};

// Obtener el servicio por ID
export const getServiceById = (serviceId) => {
  return dentalServices.find(service => service.id === parseInt(serviceId));
};
