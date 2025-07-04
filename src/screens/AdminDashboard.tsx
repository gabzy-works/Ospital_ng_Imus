import React, { useEffect, useState } from 'react';

interface Patient {
  id: number;
  lastname: string;
  firstname: string;
  middlename: string;
  suffix?: string;
  birthday: string;
  address: string;
  created_at: string;
  is_new: number;
}

interface Appointment {
  id: number;
  patient_id: number;
  appointment_date: string;
  type: string;
  reason: string;
  created_at: string;
  patient_name?: string;
}

interface AdminDashboardProps {
  onLogout: () => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ onLogout }) => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'patients' | 'appointments'>('patients');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Load patients
      const patientsResponse = await fetch('/patients');
      const patientsData = await patientsResponse.json();
      
      if (patientsData.success) {
        setPatients(patientsData.data);
      } else {
        throw new Error('Failed to load patients');
      }

      // Load all appointments
      const appointmentsResponse = await fetch('/admin/appointments');
      const appointmentsData = await appointmentsResponse.json();
      
      if (appointmentsData.success) {
        setAppointments(appointmentsData.appointments);
      } else {
        console.warn('Failed to load appointments:', appointmentsData.message);
        setAppointments([]);
      }
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredPatients = patients.filter(patient =>
    patient.lastname.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.firstname.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.middlename?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.address.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredAppointments = appointments.filter(appointment =>
    appointment.patient_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    appointment.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    appointment.reason?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getPatientAppointments = (patientId: number) => {
    return appointments.filter(apt => apt.patient_id === patientId);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="flex items-center space-x-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#05196a]"></div>
          <span className="text-lg text-gray-600">Loading admin dashboard...</span>
        </div>
      </div>
    );
  }

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
                <h1 className="text-2xl font-bold text-[#05196a]">Admin Dashboard</h1>
                <p className="text-gray-600">Ospital ng Imus - Patient Management System</p>
              </div>
            </div>
            <button 
              onClick={onLogout} 
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg text-lg font-semibold transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
            <button 
              onClick={loadData}
              className="ml-4 text-red-800 underline hover:no-underline"
            >
              Retry
            </button>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Patients</p>
                <p className="text-2xl font-bold text-gray-800">{patients.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600 mr-4">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Appointments</p>
                <p className="text-2xl font-bold text-gray-800">{appointments.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-yellow-100 text-yellow-600 mr-4">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-600">Upcoming Appointments</p>
                <p className="text-2xl font-bold text-gray-800">
                  {appointments.filter(apt => new Date(apt.appointment_date) > new Date()).length}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-xl shadow-lg mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab('patients')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'patients'
                    ? 'border-[#05196a] text-[#05196a]'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Patients ({patients.length})
              </button>
              <button
                onClick={() => setActiveTab('appointments')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'appointments'
                    ? 'border-[#05196a] text-[#05196a]'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Appointments ({appointments.length})
              </button>
            </nav>
          </div>

          {/* Search Bar */}
          <div className="p-6 border-b border-gray-200">
            <div className="relative">
              <input
                type="text"
                placeholder={`Search ${activeTab}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#05196a] focus:border-transparent"
              />
              <svg className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {activeTab === 'patients' ? (
              <div className="space-y-4">
                {filteredPatients.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <p className="text-lg">No patients found.</p>
                    {searchTerm && <p className="text-sm">Try adjusting your search terms.</p>}
                  </div>
                ) : (
                  filteredPatients.map(patient => (
                    <div key={patient.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            <h3 className="text-lg font-semibold text-gray-800 mr-3">
                              {patient.firstname} {patient.middlename} {patient.lastname} {patient.suffix || ''}
                            </h3>
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              ID: {patient.id}
                            </span>
                            {patient.is_new === 1 && (
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 ml-2">
                                New Patient
                              </span>
                            )}
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                            <div>
                              <p><span className="font-medium">Birthday:</span> {formatDate(patient.birthday)}</p>
                              <p><span className="font-medium">Address:</span> {patient.address}</p>
                            </div>
                            <div>
                              <p><span className="font-medium">Registered:</span> {formatDateTime(patient.created_at)}</p>
                              <p><span className="font-medium">Appointments:</span> {getPatientAppointments(patient.id).length}</p>
                            </div>
                          </div>
                        </div>
                        
                        <button
                          onClick={() => setSelectedPatient(selectedPatient?.id === patient.id ? null : patient)}
                          className="ml-4 text-[#05196a] hover:text-blue-800 font-medium text-sm"
                        >
                          {selectedPatient?.id === patient.id ? 'Hide Details' : 'View Details'}
                        </button>
                      </div>
                      
                      {selectedPatient?.id === patient.id && (
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <h4 className="font-medium text-gray-800 mb-3">Patient Appointments</h4>
                          {getPatientAppointments(patient.id).length === 0 ? (
                            <p className="text-gray-500 text-sm">No appointments scheduled.</p>
                          ) : (
                            <div className="space-y-2">
                              {getPatientAppointments(patient.id).map(appointment => (
                                <div key={appointment.id} className="bg-gray-50 rounded p-3 text-sm">
                                  <div className="flex justify-between items-start">
                                    <div>
                                      <p className="font-medium">{appointment.type}</p>
                                      <p className="text-gray-600">{formatDate(appointment.appointment_date)}</p>
                                      {appointment.reason && (
                                        <p className="text-gray-600 mt-1">{appointment.reason}</p>
                                      )}
                                    </div>
                                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                      new Date(appointment.appointment_date) > new Date() 
                                        ? 'bg-green-100 text-green-800' 
                                        : 'bg-gray-100 text-gray-800'
                                    }`}>
                                      {new Date(appointment.appointment_date) > new Date() ? 'Upcoming' : 'Past'}
                                    </span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            ) : (
              <div className="space-y-4">
                {filteredAppointments.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <p className="text-lg">No appointments found.</p>
                    {searchTerm && <p className="text-sm">Try adjusting your search terms.</p>}
                  </div>
                ) : (
                  filteredAppointments.map(appointment => (
                    <div key={appointment.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            <h3 className="text-lg font-semibold text-gray-800 mr-3">
                              {appointment.patient_name || `Patient ID: ${appointment.patient_id}`}
                            </h3>
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                              {appointment.type}
                            </span>
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                            <div>
                              <p><span className="font-medium">Date:</span> {formatDate(appointment.appointment_date)}</p>
                              <p><span className="font-medium">Patient ID:</span> {appointment.patient_id}</p>
                            </div>
                            <div>
                              <p><span className="font-medium">Scheduled:</span> {formatDateTime(appointment.created_at)}</p>
                              {appointment.reason && (
                                <p><span className="font-medium">Reason:</span> {appointment.reason}</p>
                              )}
                            </div>
                          </div>
                        </div>
                        
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                          new Date(appointment.appointment_date) > new Date() 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {new Date(appointment.appointment_date) > new Date() ? 'Upcoming' : 'Past'}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};