import React, { useEffect, useState } from 'react';

interface Appointment {
  id: number;
  patient_id: number;
  appointment_date: string;
  type: string;
  reason: string;
  created_at: string;
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

export const AppointmentDashboard = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newDate, setNewDate] = useState('');
  const [newType, setNewType] = useState('Consultation');
  const [newReason, setNewReason] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Get patient_id from URL
  const urlParams = new URLSearchParams(window.location.search);
  const patient_id = urlParams.get('patient_id');

  useEffect(() => {
    if (!patient_id) return;
    setLoading(true);
    fetch(`/appointments/${patient_id}`)
      .then(res => res.json())
      .then(data => {
        if (data.success) setAppointments(data.appointments.map((appt: any) => ({ ...appt, type: appt.type || appt.reason?.split(':')[0] || 'Consultation' })));
        else setError('Failed to load appointments');
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load appointments');
        setLoading(false);
      });
  }, [patient_id]);

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
      body: JSON.stringify({ patient_id, appointment_date: newDate, reason: reasonField })
    });
    const data = await res.json();
    if (data.success) {
      setNewDate('');
      setNewReason('');
      setNewType('Consultation');
      // Reload appointments
      fetch(`/appointments/${patient_id}`)
        .then(res => res.json())
        .then(data => setAppointments(data.appointments.map((appt: any) => ({ ...appt, type: appt.type || appt.reason?.split(':')[0] || 'Consultation' }))));
    } else {
      setError(data.message || 'Failed to add appointment');
    }
    setSubmitting(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-xl">
        <div className="flex flex-row justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-[#05196a]">Appointments</h2>
          <button onClick={() => window.history.back()} className="bg-gray-400 text-white px-4 py-2 rounded-lg text-lg">Back</button>
        </div>
        {loading ? (
          <div>Loading...</div>
        ) : error ? (
          <div className="text-red-600 mb-4">{error}</div>
        ) : (
          <ul className="mb-6">
            {appointments.length === 0 && <li className="text-gray-500">No appointments found.</li>}
            {appointments.map(appt => (
              <li key={appt.id} className="mb-2 p-2 border-b">
                <span className="font-bold">{appt.appointment_date}</span> - <span className="text-blue-700 font-semibold">{appt.type}</span> {appt.reason && appt.reason.includes(':') ? <span className="text-gray-600">({appt.reason.split(':').slice(1).join(':').trim()})</span> : null}
              </li>
            ))}
          </ul>
        )}
        <form onSubmit={handleAddAppointment} className="flex flex-col gap-3">
          <label className="font-semibold">Appointment Type:</label>
          <select value={newType} onChange={e => setNewType(e.target.value)} className="border rounded px-2 py-1">
            {APPOINTMENT_TYPES.map(type => <option key={type} value={type}>{type}</option>)}
          </select>
          <label className="font-semibold">Appointment Date:</label>
          <input type="date" value={newDate} onChange={e => setNewDate(e.target.value)} className="border rounded px-2 py-1" required />
          <label className="font-semibold">Reason (optional):</label>
          <input type="text" value={newReason} onChange={e => setNewReason(e.target.value)} className="border rounded px-2 py-1" placeholder="Reason" />
          <button type="submit" className="bg-green-700 text-white px-4 py-2 rounded-lg mt-2" disabled={submitting}>{submitting ? 'Saving...' : 'Add Appointment'}</button>
        </form>
      </div>
    </div>
  );
}; 