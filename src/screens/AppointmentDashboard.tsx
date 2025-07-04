import React, { useEffect, useState } from 'react';

interface Appointment {
  id: number;
  patient_id: number;
  appointment_date: string;
  type: string;
  reason: string;
  created_at: string;
}

interface Patient {
  id: number;
  lastname: string;
  firstname: string;
  middlename: string;
  suffix?: string;
  birthday: string;
  address: string;
}

interface AppointmentDashboardProps {
  patient: Patient;
  onBack: () => void;
}

const APPOINTMENT_TYPES = [
  'Consultation',
  'Laboratory',
  'Follow-up',
  'Imaging',
  'Admission',
  'Vaccination',
  'Surgery',
  'Other',
];

export const AppointmentDashboard: React.FC<AppointmentDashboardProps> = ({ patient, onBack }) => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newDate, setNewDate] = useState('');
  const [newType, setNewType] = useState('Consultation');
  const [newReason, setNewReason] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!patient?.id) return;
    setLoading(true);
    fetch(`/appointments/${patient.id}`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setAppointments(data.appointments.map((appt: any) => ({ 
            ...appt, 
            type: appt.type || appt.reason?.split(':')[0] || 'Consultation' 
          })));
        } else {
          setError('Failed to load appointments');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load appointments');
        setLoading(false);
      });
  }, [patient?.id]);

  const handleAddAppointment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDate) return;
    setSubmitting(true);
    setError(null);
    
    // Save type and reason together in reason field for now
    const reasonField = `${newType}: ${newReason}`;
    
    const res = await fetch('/appointments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        patient_id: patient.id, 
        appointment_date: newDate, 
        reason: reasonField 
      })
    });
    
    const data = await res.json();
    if (data.success) {
      setNewDate('');
      setNewReason('');
      setNewType('Consultation');
      // Reload appointments
      fetch(`/appointments/${patient.id}`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            setAppointments(data.appointments.map((appt: any) => ({ 
              ...appt, 
              type: appt.type || appt.reason?.split(':')[0] || 'Consultation' 
            })));
          }
        });
    } else {
      setError(data.message || 'Failed to add appointment');
    }
    setSubmitting(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatBirthday = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <img
                className="w-12 h-12 object-cover rounded-full mr-4"
                alt="Hospital logo"
                src="/20250625_092019.jpg"
              />
              <div>
                <h1 className="text-2xl font-bold text-[#05196a]">Appointment Dashboard</h1>
                <p className="text-gray-600">Ospital ng Imus</p>
              </div>
            </div>
            <button 
              onClick={onBack} 
              className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-lg text-lg font-semibold transition-colors"
            >
              ← Back to Patient ID
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Patient Information Card */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center mb-4">
                <img
                  src="/Patient ID sample.png"
                  alt="Patient"
                  className="w-16 h-16 object-cover rounded-lg border-2 border-gray-200 mr-4"
                />
                <div>
                  <h2 className="text-xl font-bold text-[#05196a]">Patient Information</h2>
                  <p className="text-gray-600">ID: {patient.id}</p>
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="border-b pb-2">
                  <p className="text-sm text-gray-600">Full Name</p>
                  <p className="font-semibold text-gray-800">
                    {patient.firstname} {patient.middlename} {patient.lastname} {patient.suffix || ''}
                  </p>
                </div>
                <div className="border-b pb-2">
                  <p className="text-sm text-gray-600">Birthday</p>
                  <p className="font-semibold text-gray-800">{formatBirthday(patient.birthday)}</p>
                </div>
                <div className="border-b pb-2">
                  <p className="text-sm text-gray-600">Address</p>
                  <p className="font-semibold text-gray-800">{patient.address}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Appointments Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-[#05196a] mb-6">Appointments</h2>
              
              {/* Add New Appointment Form */}
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Schedule New Appointment</h3>
                <form onSubmit={handleAddAppointment} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Appointment Type
                    </label>
                    <select 
                      value={newType} 
                      onChange={e => setNewType(e.target.value)} 
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#05196a] focus:border-transparent"
                    >
                      {APPOINTMENT_TYPES.map(type => (
                        <option key={type} value={type}>{type}</option>
                      ))}
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Appointment Date
                    </label>
                    <input 
                      type="date" 
                      value={newDate} 
                      onChange={e => setNewDate(e.target.value)} 
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#05196a] focus:border-transparent" 
                      required 
                    />
                  </div>
                  
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Reason (Optional)
                    </label>
                    <input 
                      type="text" 
                      value={newReason} 
                      onChange={e => setNewReason(e.target.value)} 
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#05196a] focus:border-transparent" 
                      placeholder="Additional details about the appointment"
                    />
                  </div>
                  
                  <div className="md:col-span-2">
                    <button 
                      type="submit" 
                      className="w-full bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed" 
                      disabled={submitting}
                    >
                      {submitting ? 'Scheduling...' : 'Schedule Appointment'}
                    </button>
                  </div>
                </form>
                
                {error && (
                  <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                    {error}
                  </div>
                )}
              </div>

              {/* Appointments List */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Upcoming & Past Appointments</h3>
                
                {loading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#05196a]"></div>
                    <span className="ml-2 text-gray-600">Loading appointments...</span>
                  </div>
                ) : appointments.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <p className="text-lg">No appointments scheduled yet.</p>
                    <p className="text-sm">Use the form above to schedule your first appointment.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {appointments.map(appointment => (
                      <div key={appointment.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center mb-2">
                              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 mr-3">
                                {appointment.type}
                              </span>
                              <span className="text-lg font-semibold text-gray-800">
                                {formatDate(appointment.appointment_date)}
                              </span>
                            </div>
                            
                            {appointment.reason && appointment.reason.includes(':') && (
                              <p className="text-gray-600 mt-1">
                                <span className="font-medium">Details:</span> {appointment.reason.split(':').slice(1).join(':').trim()}
                              </p>
                            )}
                            
                            <p className="text-sm text-gray-500 mt-2">
                              Scheduled on: {formatDate(appointment.created_at)}
                            </p>
                          </div>
                          
                          <div className="ml-4">
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                              new Date(appointment.appointment_date) > new Date() 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-gray-100 text-gray-800'
                            }`}>
                              {new Date(appointment.appointment_date) > new Date() ? 'Upcoming' : 'Past'}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};