import React, { useEffect, useState } from 'react';

interface Patient {
  id: number;
  lastname: string;
  firstname: string;
  middlename: string;
  suffix?: string;
  birthday: string;
  address: string;
  phone?: string;
  email?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  medical_history?: string;
  allergies?: string;
  blood_type?: string;
  created_at: string;
  is_new: number;
}

interface Appointment {
  id: number;
  patient_id: number;
  appointment_date: string;
  appointment_time?: string;
  type: string;
  reason: string;
  status: string;
  doctor_name?: string;
  created_at: string;
  patient_name?: string;
}

interface ImportRecord {
  id: number;
  filename: string;
  import_date: string;
  records_imported: number;
  import_type: string;
  status: string;
}

interface AdminDashboardProps {
  onLogout: () => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ onLogout }) => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [importHistory, setImportHistory] = useState<ImportRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'patients' | 'appointments' | 'import'>('patients');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [showImportModal, setShowImportModal] = useState(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importing, setImporting] = useState(false);
  const [importResult, setImportResult] = useState<any>(null);

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

      // Load import history
      const importResponse = await fetch('/import_history');
      const importData = await importResponse.json();
      
      if (importData.success) {
        setImportHistory(importData.imports);
      } else {
        console.warn('Failed to load import history:', importData.message);
        setImportHistory([]);
      }
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileImport = async () => {
    if (!importFile) {
      alert('Please select a file to import');
      return;
    }

    setImporting(true);
    setImportResult(null);

    try {
      const formData = new FormData();
      formData.append('file', importFile);

      const response = await fetch('/import_patients', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      setImportResult(result);

      if (result.success) {
        // Reload data to show new patients
        await loadData();
        setImportFile(null);
      }
    } catch (error) {
      console.error('Import error:', error);
      setImportResult({
        success: false,
        message: 'Network error during import'
      });
    } finally {
      setImporting(false);
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
    patient.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.phone?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredAppointments = appointments.filter(appointment =>
    appointment.patient_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    appointment.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    appointment.reason?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    appointment.doctor_name?.toLowerCase().includes(searchTerm.toLowerCase())
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
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
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

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                </svg>
              </div>
              <div>
                <p className="text-sm text-gray-600">Data Imports</p>
                <p className="text-2xl font-bold text-gray-800">{importHistory.length}</p>
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
              <button
                onClick={() => setActiveTab('import')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'import'
                    ? 'border-[#05196a] text-[#05196a]'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Data Import ({importHistory.length})
              </button>
            </nav>
          </div>

          {/* Search Bar and Import Button */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <div className="relative flex-1 mr-4">
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
              {activeTab === 'import' && (
                <button
                  onClick={() => setShowImportModal(true)}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
                >
                  Import Data
                </button>
              )}
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            {activeTab === 'patients' && (
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
                              <p><span className="font-medium">Phone:</span> {patient.phone || 'N/A'}</p>
                              <p><span className="font-medium">Email:</span> {patient.email || 'N/A'}</p>
                            </div>
                            <div>
                              <p><span className="font-medium">Blood Type:</span> {patient.blood_type || 'N/A'}</p>
                              <p><span className="font-medium">Allergies:</span> {patient.allergies || 'None'}</p>
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
                          <h4 className="font-medium text-gray-800 mb-3">Patient Details & Appointments</h4>
                          
                          {/* Extended patient information */}
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 text-sm">
                            <div className="bg-gray-50 rounded p-3">
                              <h5 className="font-medium text-gray-700 mb-2">Emergency Contact</h5>
                              <p><span className="font-medium">Name:</span> {patient.emergency_contact_name || 'N/A'}</p>
                              <p><span className="font-medium">Phone:</span> {patient.emergency_contact_phone || 'N/A'}</p>
                            </div>
                            <div className="bg-gray-50 rounded p-3">
                              <h5 className="font-medium text-gray-700 mb-2">Medical Information</h5>
                              <p><span className="font-medium">History:</span> {patient.medical_history || 'None'}</p>
                            </div>
                          </div>

                          {/* Patient appointments */}
                          <h5 className="font-medium text-gray-800 mb-3">Appointments</h5>
                          {getPatientAppointments(patient.id).length === 0 ? (
                            <p className="text-gray-500 text-sm">No appointments scheduled.</p>
                          ) : (
                            <div className="space-y-2">
                              {getPatientAppointments(patient.id).map(appointment => (
                                <div key={appointment.id} className="bg-gray-50 rounded p-3 text-sm">
                                  <div className="flex justify-between items-start">
                                    <div>
                                      <p className="font-medium">{appointment.type}</p>
                                      <p className="text-gray-600">{formatDate(appointment.appointment_date)} {appointment.appointment_time && `at ${appointment.appointment_time}`}</p>
                                      {appointment.doctor_name && (
                                        <p className="text-gray-600">Doctor: {appointment.doctor_name}</p>
                                      )}
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
            )}

            {activeTab === 'appointments' && (
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
                              <p><span className="font-medium">Time:</span> {appointment.appointment_time || 'Not specified'}</p>
                              <p><span className="font-medium">Patient ID:</span> {appointment.patient_id}</p>
                            </div>
                            <div>
                              <p><span className="font-medium">Doctor:</span> {appointment.doctor_name || 'Not assigned'}</p>
                              <p><span className="font-medium">Status:</span> {appointment.status}</p>
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

            {activeTab === 'import' && (
              <div className="space-y-6">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-blue-800 mb-2">Data Import Instructions</h3>
                  <div className="text-sm text-blue-700 space-y-2">
                    <p><strong>Supported formats:</strong> CSV and JSON files</p>
                    <p><strong>Required fields:</strong> lastname, firstname, middlename, birthday, address</p>
                    <p><strong>Optional fields:</strong> suffix, phone, email, emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type</p>
                    <p><strong>CSV headers:</strong> Use column names like "lastname", "firstname", "middlename", etc.</p>
                    <p><strong>Date format:</strong> Use YYYY-MM-DD format for birthday field</p>
                  </div>
                </div>

                {importHistory.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <p className="text-lg">No import history found.</p>
                    <p className="text-sm">Import your first data file to get started.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-gray-800">Import History</h3>
                    {importHistory.map(record => (
                      <div key={record.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h4 className="text-lg font-semibold text-gray-800">{record.filename}</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600 mt-2">
                              <div>
                                <p><span className="font-medium">Import Date:</span> {formatDateTime(record.import_date)}</p>
                                <p><span className="font-medium">Records Imported:</span> {record.records_imported}</p>
                              </div>
                              <div>
                                <p><span className="font-medium">File Type:</span> {record.import_type.toUpperCase()}</p>
                                <p><span className="font-medium">Status:</span> {record.status}</p>
                              </div>
                            </div>
                          </div>
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                            record.status === 'completed' 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {record.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-40">
          <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold mb-4 text-[#05196a]">Import Patient Data</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select File (CSV or JSON)
                </label>
                <input
                  type="file"
                  accept=".csv,.json"
                  onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#05196a] focus:border-transparent"
                />
              </div>

              {importResult && (
                <div className={`p-3 rounded-lg ${
                  importResult.success 
                    ? 'bg-green-100 border border-green-400 text-green-700' 
                    : 'bg-red-100 border border-red-400 text-red-700'
                }`}>
                  <p className="font-medium">{importResult.message}</p>
                  {importResult.imported_count > 0 && (
                    <p className="text-sm mt-1">Imported: {importResult.imported_count} patients</p>
                  )}
                  {importResult.total_errors > 0 && (
                    <p className="text-sm mt-1">Errors: {importResult.total_errors}</p>
                  )}
                </div>
              )}

              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => {
                    setShowImportModal(false);
                    setImportFile(null);
                    setImportResult(null);
                  }}
                  className="flex-1 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleFileImport}
                  disabled={!importFile || importing}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {importing ? 'Importing...' : 'Import'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};