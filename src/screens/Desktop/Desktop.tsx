import React, { useState, useRef } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { DatePicker } from "../../components/ui/date-picker";
import { AppointmentDashboard } from "../AppointmentDashboard";
import { AdminLogin } from "../AdminLogin";
import { AdminDashboard } from "../AdminDashboard";

export const Desktop = (): JSX.Element => {
  const [birthday, setBirthday] = useState<Date | undefined>();
  const [formData, setFormData] = useState({
    lastname: "",
    firstname: "",
    middlename: "",
    suffix: "",
  });
  const [showNotFound, setShowNotFound] = useState(false);
  const [showFound, setShowFound] = useState(false);
  const [foundPatient, setFoundPatient] = useState<any>(null);
  const [matchingBirthdays, setMatchingBirthdays] = useState<string[]>([]);
  const [selectBirthdayMode, setSelectBirthdayMode] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const [uploadedIdImage, setUploadedIdImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const idCardRef = useRef<HTMLDivElement>(null);
  const [birthdayDay, setBirthdayDay] = useState<string>("");
  const [birthdayMonth, setBirthdayMonth] = useState<string>("");
  const [birthdayYear, setBirthdayYear] = useState<string>("");
  const [showAddPatient, setShowAddPatient] = useState(false);
  const [activeTab, setActiveTab] = useState<'search' | 'add'>('search');
  const [addForm, setAddForm] = useState({
    lastname: '',
    firstname: '',
    middlename: '',
    suffix: '',
    birthdayDay: '',
    birthdayMonth: '',
    birthdayYear: '',
    address: '',
    phone: '',
    email: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    medical_history: '',
    allergies: '',
    blood_type: '',
  });
  const [addSuccess, setAddSuccess] = useState<string | null>(null);
  const [addError, setAddError] = useState<string | null>(null);
  const [showAppointmentDashboard, setShowAppointmentDashboard] = useState(false);
  const [selectedPatientForAppointment, setSelectedPatientForAppointment] = useState<any>(null);
  const [isSubmittingPatient, setIsSubmittingPatient] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [showAdminDashboard, setShowAdminDashboard] = useState(false);

  const days = Array.from({ length: 31 }, (_, i) => String(i + 1).padStart(2, '0'));
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const years = Array.from({ length: 2025 - 1900 + 1 }, (_, i) => String(1900 + i));
  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];

  // Form field data for mapping
  const formFields = [
    { id: "lastname", label: "Lastname", placeholder: "Enter lastname" },
    { id: "firstname", label: "Firstname", placeholder: "Enter firstname" },
    { id: "middlename", label: "Middlename", placeholder: "Enter middlename" },
    { id: "suffix", label: "Suffix (Optional)", placeholder: "Enter suffix (optional)" },
  ];

  const knownPatients = [
    { id: 1, lastname: "Santos", firstname: "Maria", middlename: "Cruz", suffix: null, birthday: "1985-03-15", address: "123 Rizal St., Imus, Cavite" },
    { id: 2, lastname: "Santos", firstname: "Shayne", middlename: "Cruz", suffix: null, birthday: "1985-05-15", address: "456 Mabini St., Imus, Cavite" },
    { id: 3, lastname: "Garcia", firstname: "Juan", middlename: "Dela Cruz", suffix: "Jr.", birthday: "1990-07-22", address: "789 Bonifacio Ave., Bacoor, Cavite" },
    { id: 4, lastname: "Reyes", firstname: "Ana", middlename: "Bautista", suffix: null, birthday: "1978-11-08", address: "321 Aguinaldo Hwy., Dasmariñas, Cavite" },
    { id: 5, lastname: "Gonzales", firstname: "Pedro", middlename: "Martinez", suffix: "Sr.", birthday: "1965-01-30", address: "654 P. Burgos St., Imus, Cavite" },
    { id: 6, lastname: "Lopez", firstname: "Carmen", middlename: "Villanueva", suffix: null, birthday: "1992-09-12", address: "987 Gen. Trias Dr., Gen. Trias, Cavite" },
    { id: 7, lastname: "Mendoza", firstname: "Roberto", middlename: "Fernandez", suffix: "III", birthday: "1988-05-18", address: "159 Molino Blvd., Bacoor, Cavite" },
    { id: 8, lastname: "Torres", firstname: "Luz", middlename: "Aquino", suffix: null, birthday: "1975-12-03", address: "753 Salitran Rd., Dasmariñas, Cavite" },
    { id: 9, lastname: "Flores", firstname: "Miguel", middlename: "Ramos", suffix: "Jr.", birthday: "1983-08-25", address: "852 Palico Rd., Imus, Cavite" },
    { id: 10, lastname: "Morales", firstname: "Rosa", middlename: "Castillo", suffix: null, birthday: "1995-04-07", address: "951 Anabu Rd., Imus, Cavite" },
    { id: 11, lastname: "Rivera", firstname: "Carlos", middlename: "Jimenez", suffix: null, birthday: "1970-10-14", address: "357 Tanzang Luma, Imus, Cavite" },
  ];

  // Helper to convert month name to number
  const monthNameToNumber = (month: string) => {
    const months = [
      "january", "february", "march", "april", "may", "june",
      "july", "august", "september", "october", "november", "december"
    ];
    const idx = months.indexOf(month.trim().toLowerCase());
    return idx === -1 ? null : String(idx + 1).padStart(2, '0');
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    // Require all birthday fields before proceeding
    if (!birthdayDay || !birthdayMonth || !birthdayYear) {
      alert("Please enter the complete birthday (day, month, year) before searching for patient records.");
      return;
    }
    // Convert to YYYY-MM-DD
    const monthNum = monthNameToNumber(birthdayMonth);
    if (!monthNum) {
      alert("Please enter a valid month name (e.g., March).");
      return;
    }
    const formattedBirthday = `${birthdayYear}-${monthNum}-${birthdayDay.padStart(2, '0')}`;
    
    try {
      // First try to search in the database
      const response = await fetch('/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          lastname: formData.lastname.trim(),
          firstname: formData.firstname.trim(),
          middlename: formData.middlename.trim(),
          suffix: formData.suffix.trim(),
          birthday: formattedBirthday
        })
      });

      const data = await response.json();
      
      if (data.success && data.data.patients.length > 0) {
        // Found patient in database
        const patient = data.data.patients[0];
        setFoundPatient(patient);
        setShowFound(true);
        setShowNotFound(false);
        setMatchingBirthdays([]);
        setSelectBirthdayMode(false);
        return;
      }
    } catch (error) {
      console.error('Database search error:', error);
    }

    // Fallback to local search if database search fails or no results
    const match = knownPatients.find(
      p =>
        p.lastname.toLowerCase() === formData.lastname.trim().toLowerCase() &&
        p.firstname.toLowerCase() === formData.firstname.trim().toLowerCase() &&
        p.middlename?.toLowerCase() === formData.middlename.trim().toLowerCase() &&
        p.birthday === formattedBirthday
    );

    if (match) {
      setFoundPatient(match);
      setShowFound(true);
      setShowNotFound(false);
      setMatchingBirthdays([]);
      setSelectBirthdayMode(false);
      return;
    } else {
      setShowNotFound(true);
      setShowFound(false);
      setFoundPatient(null);
      setMatchingBirthdays([]);
      setSelectBirthdayMode(false);
      return;
    }
  };

  const handleBirthdaySelect = (bday: string) => {
    const match = knownPatients.find(
      p =>
        p.lastname.toLowerCase() === formData.lastname.trim().toLowerCase() &&
        (!formData.firstname || p.firstname.toLowerCase() === formData.firstname.trim().toLowerCase()) &&
        (!formData.middlename || p.middlename?.toLowerCase() === formData.middlename.trim().toLowerCase()) &&
        (!formData.suffix || (p.suffix || "").toLowerCase() === formData.suffix.trim().toLowerCase()) &&
        p.birthday === bday
    );
    if (match) {
      setFoundPatient(match);
      setShowFound(true);
      setShowNotFound(false);
      setSelectBirthdayMode(false);
      setBirthday(new Date(match.birthday));
    } else {
      setShowNotFound(true);
      setShowFound(false);
      setSelectBirthdayMode(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleTryAgain = () => {
    setShowNotFound(false);
    // Optionally reset form
    if (formRef.current) formRef.current.reset();
    setFormData({ lastname: "", firstname: "", middlename: "", suffix: "" });
    setBirthday(undefined);
  };

  const handleBack = () => {
    // Replace with your navigation logic
    window.location.href = "/";
  };

  const handleCloseFound = () => {
    setShowFound(false);
    setFoundPatient(null);
    if (formRef.current) formRef.current.reset();
    setFormData({ lastname: "", firstname: "", middlename: "", suffix: "" });
    setBirthday(undefined);
  };

  const handleIdImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setUploadedIdImage(event.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUploadButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handlePrintIdCard = () => {
    if (!idCardRef.current) return;
    // Add a print class to the card, print, then remove the class
    idCardRef.current.classList.add('print-id-card');
    window.print();
    setTimeout(() => {
      idCardRef.current?.classList.remove('print-id-card');
    }, 1000);
  };

  // Add a helper function to format birthday
  const formatBirthday = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  const handleAddPatient = () => {
    setShowAddPatient(true);
  };

  const handleCloseAddPatient = () => {
    setShowAddPatient(false);
    // Reset form and messages
    setAddForm({ 
      lastname: '', 
      firstname: '', 
      middlename: '', 
      suffix: '', 
      birthdayDay: '', 
      birthdayMonth: '', 
      birthdayYear: '', 
      address: '',
      phone: '',
      email: '',
      emergency_contact_name: '',
      emergency_contact_phone: '',
      medical_history: '',
      allergies: '',
      blood_type: '',
    });
    setAddSuccess(null);
    setAddError(null);
  };

  const handleAddFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setAddForm({ ...addForm, [e.target.name]: e.target.value });
  };

  const handleAddPatientSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddSuccess(null);
    setAddError(null);
    setIsSubmittingPatient(true);

    // Validate required fields
    if (!addForm.lastname || !addForm.firstname || !addForm.middlename || 
        !addForm.birthdayDay || !addForm.birthdayMonth || !addForm.birthdayYear || !addForm.address) {
      setAddError('Please fill in all required fields (lastname, firstname, middlename, birthday, address).');
      setIsSubmittingPatient(false);
      return;
    }

    // Prepare birthday in YYYY-MM-DD format
    const monthNum = monthNameToNumber(addForm.birthdayMonth);
    if (!monthNum) {
      setAddError('Please enter a valid month name (e.g., March).');
      setIsSubmittingPatient(false);
      return;
    }
    const birthday = `${addForm.birthdayYear}-${monthNum}-${addForm.birthdayDay.padStart(2, '0')}`;

    // Validate date
    const dateObj = new Date(birthday);
    if (isNaN(dateObj.getTime())) {
      setAddError('Please enter a valid date.');
      setIsSubmittingPatient(false);
      return;
    }

    try {
      const response = await fetch('/add_patient', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
          lastname: addForm.lastname.trim(),
          firstname: addForm.firstname.trim(),
          middlename: addForm.middlename.trim(),
          suffix: addForm.suffix.trim() || null,
          birthday,
          address: addForm.address.trim(),
          phone: addForm.phone.trim() || null,
          email: addForm.email.trim() || null,
          emergency_contact_name: addForm.emergency_contact_name.trim() || null,
          emergency_contact_phone: addForm.emergency_contact_phone.trim() || null,
          medical_history: addForm.medical_history.trim() || null,
          allergies: addForm.allergies.trim() || null,
          blood_type: addForm.blood_type || null,
        })
      });

      const data = await response.json();
      
      if (response.ok && data.success) {
        setAddSuccess(`Patient "${addForm.firstname} ${addForm.lastname}" has been successfully added to the database!`);
        // Reset form after successful submission
        setAddForm({ 
          lastname: '', 
          firstname: '', 
          middlename: '', 
          suffix: '', 
          birthdayDay: '', 
          birthdayMonth: '', 
          birthdayYear: '', 
          address: '',
          phone: '',
          email: '',
          emergency_contact_name: '',
          emergency_contact_phone: '',
          medical_history: '',
          allergies: '',
          blood_type: '',
        });
        
        // Auto-close the modal after 3 seconds
        setTimeout(() => {
          handleCloseAddPatient();
        }, 3000);
      } else {
        setAddError(data.message || 'Failed to add patient. Please try again.');
      }
    } catch (error) {
      console.error('Error adding patient:', error);
      setAddError('Network error. Please check your connection and try again.');
    } finally {
      setIsSubmittingPatient(false);
    }
  };

  const handleAppointmentClick = () => {
    if (foundPatient) {
      setSelectedPatientForAppointment(foundPatient);
      setShowAppointmentDashboard(true);
      setShowFound(false); // Hide the patient ID modal
    }
  };

  const handleBackFromAppointment = () => {
    setShowAppointmentDashboard(false);
    setSelectedPatientForAppointment(null);
    setShowFound(true); // Show the patient ID modal again
  };

  const handleAdminLogin = () => {
    setShowAdminLogin(true);
  };

  const handleAdminLoginSuccess = () => {
    setShowAdminLogin(false);
    setShowAdminDashboard(true);
  };

  const handleAdminLogout = () => {
    localStorage.removeItem('adminLoggedIn');
    setShowAdminDashboard(false);
  };

  const handleBackFromAdminLogin = () => {
    setShowAdminLogin(false);
  };

  // Check if admin is already logged in on component mount
  React.useEffect(() => {
    const isAdminLoggedIn = localStorage.getItem('adminLoggedIn') === 'true';
    if (isAdminLoggedIn) {
      setShowAdminDashboard(true);
    }
  }, []);

  // If showing admin login, render it instead of the main interface
  if (showAdminLogin) {
    return <AdminLogin onLogin={handleAdminLoginSuccess} onBack={handleBackFromAdminLogin} />;
  }

  // If showing admin dashboard, render it instead of the main interface
  if (showAdminDashboard) {
    return <AdminDashboard onLogout={handleAdminLogout} />;
  }

  // If showing appointment dashboard, render it instead of the main interface
  if (showAppointmentDashboard && selectedPatientForAppointment) {
    return (
      <AppointmentDashboard 
        patient={selectedPatientForAppointment}
        onBack={handleBackFromAppointment}
      />
    );
  }

  return (
    <div className="bg-white w-full min-h-screen relative">
      {/* Full-width background image with blur */}
      <div className="fixed inset-0 w-full h-full z-0">
        <img
          className="w-full h-full object-cover opacity-80 blur-sm"
          alt="Hospital background"
          src="/Screenshot (1).png"
        />
      </div>

      {/* Header section - Full width across entire viewport */}
      <header className="w-full h-[140px] bg-white/90 backdrop-blur-sm border-0 border-none shadow-[0px_4px_4px_#00000040] relative z-10" />
      <div className="w-full h-[24px] bg-[#05196a] border-0 border-none shadow-[0px_4px_4px_#00000040] relative z-10" />
      
      {/* Header row: logos left, title centered, admin button right */}
      <div className="flex items-center absolute top-[14px] left-0 w-full z-20 px-6">
        {/* Logos group on the left */}
        <div className="flex items-center">
          <img
            className="w-[89px] h-[89px] mt-[6px] object-cover"
            alt="Ph seal imus"
            src="/Ph_seal_Imus.png"
          />
          <img
            className="w-[110px] h-[110px] ml-[9px] object-cover"
            alt="Imus logo"
            src="/20250625_092038.jpg"
          />
          <img
            className="w-[89px] h-[89px] ml-[9px] mt-[10px] object-cover"
            alt="Hospital logo"
            src="/20250625_092019.jpg"
          />
        </div>
        {/* Centered title */}
        <div className="flex-1 flex justify-center">
          <div className="flex flex-col items-center">
            <h1 className="text-center font-sans font-black text-[#05196a] text-[44px] tracking-[0] leading-[normal] drop-shadow-lg whitespace-nowrap">
              OSPITAL NG IMUS
            </h1>
            <span style={{ fontFamily: 'Times New Roman, Times, serif', fontStyle: 'italic', fontWeight: 'bold', fontSize: '16px', color: '#05196a' }}>
              We serve, We care
            </span>
          </div>
        </div>
        {/* Admin button on the right */}
        <div className="w-[300px] flex justify-end">
          <button
            onClick={handleAdminLogin}
            className="bg-white hover:bg-gray-50 text-[#05196a] px-6 py-2 rounded-lg text-lg font-semibold shadow-lg border border-gray-200 transition-colors"
          >
            Admin Login
          </button>
        </div>
      </div>

      {/* Main content container */}
      <div className="flex flex-row justify-center w-full relative z-10">
        <div className="w-full max-w-[1400px] relative origin-top">
          <div className="absolute w-full h-full top-0 left-0">
            {/* Tab system */}
            {/* Remove the tab system (the div with the two buttons for 'Search Patient' and 'Add Patient') */}
          </div>
        </div>
      </div>

      {activeTab === 'search' ? (
        <div className="absolute top-[200px] left-1/2 transform -translate-x-1/2">
          <form ref={formRef} className="flex flex-col gap-3 items-center" onSubmit={handleSearch}>
            {formFields.map((field) => (
              <div key={field.id} className="relative w-full flex justify-start mb-1">
                <Input
                  id={field.id}
                  value={formData[field.id as keyof typeof formData]}
                  onChange={handleInputChange}
                  className="w-[350px] h-[40px] text-[18px] bg-white/95 backdrop-blur-sm rounded-[16px] shadow-[0px_2px_2px_#00000040] px-4 placeholder:text-[#838383] placeholder:text-[18px]"
                  placeholder={field.placeholder}
                />
              </div>
            ))}
            <div className="flex gap-2 w-[350px] mb-2">
              <select
                value={birthdayDay}
                onChange={e => setBirthdayDay(e.target.value)}
                className="w-1/3 text-[18px] text-white bg-[#05196a] rounded px-2 py-2"
              >
                <option value="">Day</option>
                {days.map(day => (
                  <option key={day} value={day}>{day}</option>
                ))}
              </select>
              <select
                value={birthdayMonth}
                onChange={e => setBirthdayMonth(e.target.value)}
                className="w-1/3 text-[18px] text-white bg-[#05196a] rounded px-2 py-2"
              >
                <option value="">Month</option>
                {months.map(month => (
                  <option key={month} value={month}>{month}</option>
                ))}
              </select>
              <select
                value={birthdayYear}
                onChange={e => setBirthdayYear(e.target.value)}
                className="w-1/3 text-[18px] text-white bg-[#05196a] rounded px-2 py-2"
              >
                <option value="">Year</option>
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
            <div className="flex flex-row gap-4 w-[350px] mt-[16px]">
              <Button type="submit" className="flex-1 h-[50px] bg-[#05196a] rounded-[16px] shadow font-sans font-extrabold text-white text-[22px] hover:bg-[#041456] transition-colors">
                SEARCH
              </Button>
              <Button type="button" onClick={handleAddPatient} className="flex-1 h-[50px] bg-green-600 rounded-[16px] shadow font-sans font-extrabold text-white text-[22px] hover:bg-green-800 transition-colors">
                Add Patient
              </Button>
            </div>
          </form>
        </div>
      ) : (
        <div className="flex flex-col items-center w-full">
          <form onSubmit={handleAddPatientSubmit} className="flex flex-col gap-3 items-center w-full max-w-md bg-white/95 p-8 rounded-xl shadow-lg">
            <h2 className="text-2xl font-bold mb-2 text-[#05196a]">Add Patient</h2>
            <Input name="lastname" value={addForm.lastname} onChange={handleAddFormChange} placeholder="Lastname" className="w-full text-[18px]" />
            <Input name="firstname" value={addForm.firstname} onChange={handleAddFormChange} placeholder="Firstname" className="w-full text-[18px]" />
            <Input name="middlename" value={addForm.middlename} onChange={handleAddFormChange} placeholder="Middlename" className="w-full text-[18px]" />
            <Input name="suffix" value={addForm.suffix} onChange={handleAddFormChange} placeholder="Suffix (Optional)" className="w-full text-[18px]" />
            <div className="flex gap-2 w-full">
              <select name="birthdayDay" value={addForm.birthdayDay} onChange={handleAddFormChange} className="w-1/3 text-[18px] text-white bg-[#05196a] rounded px-2 py-2">
                <option value="">Day</option>
                {days.map(day => <option key={day} value={day}>{day}</option>)}
              </select>
              <select name="birthdayMonth" value={addForm.birthdayMonth} onChange={handleAddFormChange} className="w-1/3 text-[18px] text-white bg-[#05196a] rounded px-2 py-2">
                <option value="">Month</option>
                {months.map(month => <option key={month} value={month}>{month}</option>)}
              </select>
              <select name="birthdayYear" value={addForm.birthdayYear} onChange={handleAddFormChange} className="w-1/3 text-[18px] text-white bg-[#05196a] rounded px-2 py-2">
                <option value="">Year</option>
                {years.map(year => <option key={year} value={year}>{year}</option>)}
              </select>
            </div>
            <Input name="address" value={addForm.address} onChange={handleAddFormChange} placeholder="Address" className="w-full text-[18px]" />
            {addError && <div className="text-red-600 font-semibold mt-2 text-center">{addError}</div>}
            {addSuccess && <div className="text-green-600 font-semibold mt-2 text-center">{addSuccess}</div>}
            <Button 
              type="submit" 
              disabled={isSubmittingPatient}
              className="w-full h-[50px] mt-[16px] bg-[#05196a] rounded-[16px] shadow font-sans font-extrabold text-white text-[22px] hover:bg-[#041456] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmittingPatient ? 'Adding Patient...' : 'Add Patient'}
            </Button>
          </form>
        </div>
      )}

      {showNotFound && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-40">
          <div className="bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center">
            <h2 className="text-3xl font-bold mb-4 text-red-600">Record not found</h2>
            <p className="mb-6 text-lg">Try again.</p>
            <div className="flex gap-4">
              <Button onClick={handleBack} className="bg-gray-400 text-white px-6 py-2 rounded-lg text-lg">Back</Button>
            </div>
          </div>
        </div>
      )}

      {showFound && foundPatient && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-40">
          {/* Print Button - outside the card, upper right of modal */}
          <button
            onClick={handlePrintIdCard}
            className="absolute top-8 right-16 bg-blue-600 hover:bg-blue-800 text-white px-4 py-2 rounded shadow text-sm font-bold z-20 print:hidden"
            title="Print ID Card"
            type="button"
          >
            Print
          </button>
          <div className="rounded-2xl shadow-lg p-0 flex flex-col items-center min-w-[600px] relative">
            {/* ID Card Design */}
            <div
              ref={idCardRef}
              className="w-[520px] h-[320px] bg-gradient-to-r from-green-400 via-blue-500 to-blue-800 rounded-xl flex flex-col items-center justify-between p-8 relative shadow-2xl border-4 border-white print-id-card-container"
              style={{ boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)' }}
            >
              {/* Hospital logo and title */}
              <div className="flex flex-row items-center w-full mb-2 justify-between">
                <img
                  src="/Ph_seal_Imus.png"
                  alt="Ph seal imus"
                  className="w-12 h-12 object-cover rounded-full border-2 border-white bg-white"
                />
                <div className="flex-1 text-center">
                  <span className="text-white font-bold text-lg tracking-wide drop-shadow">PATIENT ID</span>
                </div>
                <img
                  src="/20250625_092019.jpg"
                  alt="Hospital logo"
                  className="w-12 h-12 object-cover rounded-full border-2 border-white bg-white"
                />
              </div>
              {/* Patient photo and info - centered info */}
              <div className="flex flex-row items-center w-full gap-8 justify-center flex-1">
                <div className="flex flex-col items-center gap-2">
                  <img
                    src={uploadedIdImage || "/Patient ID sample.png"}
                    alt="Patient ID"
                    className="w-24 h-24 object-cover rounded-lg border-2 border-white bg-white"
                  />
                  <input
                    type="file"
                    accept="image/*"
                    ref={fileInputRef}
                    className="hidden"
                    onChange={handleIdImageUpload}
                  />
                  <button
                    type="button"
                    onClick={handleUploadButtonClick}
                    className="mt-1 px-3 py-1 bg-white bg-opacity-80 text-blue-800 text-xs font-semibold rounded shadow hover:bg-opacity-100 transition print:hidden"
                  >
                    Upload Photo
                  </button>
                </div>
                <div className="flex flex-col items-center justify-center text-white text-base font-medium gap-2 text-center self-center my-auto">
                  <div className="flex flex-col items-center w-full">
                    <div><span className="font-bold">Lastname:</span> {foundPatient.lastname}</div>
                    <div><span className="font-bold">Firstname:</span> {foundPatient.firstname}</div>
                    <div><span className="font-bold">Middlename:</span> {foundPatient.middlename || '-'}</div>
                    <div><span className="font-bold">Suffix:</span> {foundPatient.suffix || '-'}</div>
                    <div><span className="font-bold">Birthday:</span> {formatBirthday(foundPatient.birthday)}</div>
                    <div><span className="font-bold">Address:</span> {foundPatient.address}</div>
                  </div>
                </div>
              </div>
              {/* ID Footer */}
              <div className="w-full flex flex-row items-center justify-between mt-2">
                <span className="text-xs text-white/80 font-semibold">Patient ID Card</span>
                <span className="text-xs text-white/80 font-semibold">Valid at ONI</span>
              </div>
            </div>
            <div className="flex flex-row gap-4 mt-6 print:hidden">
              <Button onClick={handleCloseFound} className="bg-gray-400 text-white px-6 py-2 rounded-lg text-lg">Back</Button>
              <Button onClick={handleAppointmentClick} className="bg-green-700 text-white px-6 py-2 rounded-lg text-lg">Appointment</Button>
            </div>
          </div>
        </div>
      )}

      {selectBirthdayMode && matchingBirthdays.length > 1 && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-40">
          <div className="bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center">
            <h2 className="text-2xl font-bold mb-4 text-blue-700">Select Birthday</h2>
            <p className="mb-6 text-lg">Multiple records found for this name. Please select the correct birthday:</p>
            <div className="flex flex-col gap-4">
              {matchingBirthdays.map(bday => (
                <button
                  key={bday}
                  onClick={() => handleBirthdaySelect(bday)}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg text-lg hover:bg-blue-800 transition-colors"
                >
                  {formatBirthday(bday)}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {showAddPatient && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-40">
          <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col items-center max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4 text-green-700">Add New Patient</h2>
            <form onSubmit={handleAddPatientSubmit} className="flex flex-col gap-3 items-center w-full">
              {/* Basic Information */}
              <div className="w-full border-b pb-4 mb-4">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Basic Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <Input 
                    name="lastname" 
                    value={addForm.lastname} 
                    onChange={handleAddFormChange} 
                    placeholder="Lastname *" 
                    className="w-full text-[16px]" 
                    required
                  />
                  <Input 
                    name="firstname" 
                    value={addForm.firstname} 
                    onChange={handleAddFormChange} 
                    placeholder="Firstname *" 
                    className="w-full text-[16px]" 
                    required
                  />
                  <Input 
                    name="middlename" 
                    value={addForm.middlename} 
                    onChange={handleAddFormChange} 
                    placeholder="Middlename *" 
                    className="w-full text-[16px]" 
                    required
                  />
                  <Input 
                    name="suffix" 
                    value={addForm.suffix} 
                    onChange={handleAddFormChange} 
                    placeholder="Suffix (Optional)" 
                    className="w-full text-[16px]" 
                  />
                </div>
                
                <div className="flex gap-2 w-full mt-3">
                  <select 
                    name="birthdayDay" 
                    value={addForm.birthdayDay} 
                    onChange={handleAddFormChange} 
                    className="w-1/3 text-[16px] text-white bg-[#05196a] rounded px-2 py-2"
                    required
                  >
                    <option value="">Day *</option>
                    {days.map(day => <option key={day} value={day}>{day}</option>)}
                  </select>
                  <select 
                    name="birthdayMonth" 
                    value={addForm.birthdayMonth} 
                    onChange={handleAddFormChange} 
                    className="w-1/3 text-[16px] text-white bg-[#05196a] rounded px-2 py-2"
                    required
                  >
                    <option value="">Month *</option>
                    {months.map(month => <option key={month} value={month}>{month}</option>)}
                  </select>
                  <select 
                    name="birthdayYear" 
                    value={addForm.birthdayYear} 
                    onChange={handleAddFormChange} 
                    className="w-1/3 text-[16px] text-white bg-[#05196a] rounded px-2 py-2"
                    required
                  >
                    <option value="">Year *</option>
                    {years.map(year => <option key={year} value={year}>{year}</option>)}
                  </select>
                </div>
              </div>

              {/* Contact Information */}
              <div className="w-full border-b pb-4 mb-4">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Contact Information</h3>
                <div className="grid grid-cols-1 gap-3">
                  <Input 
                    name="address" 
                    value={addForm.address} 
                    onChange={handleAddFormChange} 
                    placeholder="Address *" 
                    className="w-full text-[16px]" 
                    required
                  />
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <Input 
                      name="phone" 
                      value={addForm.phone} 
                      onChange={handleAddFormChange} 
                      placeholder="Phone Number" 
                      className="w-full text-[16px]" 
                    />
                    <Input 
                      name="email" 
                      value={addForm.email} 
                      onChange={handleAddFormChange} 
                      placeholder="Email Address" 
                      type="email"
                      className="w-full text-[16px]" 
                    />
                  </div>
                </div>
              </div>

              {/* Emergency Contact */}
              <div className="w-full border-b pb-4 mb-4">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Emergency Contact</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <Input 
                    name="emergency_contact_name" 
                    value={addForm.emergency_contact_name} 
                    onChange={handleAddFormChange} 
                    placeholder="Emergency Contact Name" 
                    className="w-full text-[16px]" 
                  />
                  <Input 
                    name="emergency_contact_phone" 
                    value={addForm.emergency_contact_phone} 
                    onChange={handleAddFormChange} 
                    placeholder="Emergency Contact Phone" 
                    className="w-full text-[16px]" 
                  />
                </div>
              </div>

              {/* Medical Information */}
              <div className="w-full pb-4 mb-4">
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Medical Information</h3>
                <div className="grid grid-cols-1 gap-3">
                  <select 
                    name="blood_type" 
                    value={addForm.blood_type} 
                    onChange={handleAddFormChange} 
                    className="w-full text-[16px] border border-gray-300 rounded px-3 py-2"
                  >
                    <option value="">Select Blood Type (Optional)</option>
                    {bloodTypes.map(type => <option key={type} value={type}>{type}</option>)}
                  </select>
                  <Input 
                    name="allergies" 
                    value={addForm.allergies} 
                    onChange={handleAddFormChange} 
                    placeholder="Known Allergies (Optional)" 
                    className="w-full text-[16px]" 
                  />
                  <textarea 
                    name="medical_history" 
                    value={addForm.medical_history} 
                    onChange={handleAddFormChange} 
                    placeholder="Medical History (Optional)" 
                    className="w-full text-[16px] border border-gray-300 rounded px-3 py-2 min-h-[80px]"
                    rows={3}
                  />
                </div>
              </div>
              
              {addError && (
                <div className="w-full p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-center text-sm">
                  {addError}
                </div>
              )}
              
              {addSuccess && (
                <div className="w-full p-3 bg-green-100 border border-green-400 text-green-700 rounded-lg text-center text-sm">
                  {addSuccess}
                </div>
              )}
              
              <div className="flex gap-3 w-full mt-4">
                <Button 
                  type="button" 
                  onClick={handleCloseAddPatient} 
                  className="flex-1 bg-gray-400 text-white px-6 py-2 rounded-lg text-lg hover:bg-gray-500 transition-colors"
                >
                  Cancel
                </Button>
                <Button 
                  type="submit" 
                  disabled={isSubmittingPatient}
                  className="flex-1 bg-green-600 rounded-[16px] shadow font-sans font-extrabold text-white text-lg hover:bg-green-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmittingPatient ? 'Adding...' : 'Add Patient'}
                </Button>
              </div>
            </form>
            
            <p className="text-xs text-gray-500 mt-3 text-center">
              * Required fields
            </p>
          </div>
        </div>
      )}
    </div>
  );
};