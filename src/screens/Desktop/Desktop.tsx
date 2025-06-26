import React, { useState } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { DatePicker } from "../../components/ui/date-picker";

export const Desktop = (): JSX.Element => {
  const [birthday, setBirthday] = useState<Date | undefined>();

  // Form field data for mapping
  const formFields = [
    { id: "lastname", label: "Lastname", placeholder: "Enter lastname" },
    { id: "firstname", label: "Firstname", placeholder: "Enter firstname" },
    { id: "middlename", label: "Middlename", placeholder: "Enter middlename" },
    {
      id: "suffix",
      label: "Suffix (If Applicable)",
      placeholder: "Enter suffix (if applicable)",
    },
  ];

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
      
      {/* Logo images - positioned absolutely over the header */}
      <div className="flex absolute top-[14px] left-[26px] z-20">
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

      {/* Main content container */}
      <div className="flex flex-row justify-center w-full relative z-10">
        <div className="w-full max-w-[1400px] relative scale-75 origin-top">
          <div className="absolute w-full h-full top-0 left-0">
            {/* Main title - centered */}
            <h1 className="absolute w-full top-[40px] text-center font-sans font-black text-[#05196a] text-[44px] tracking-[0] leading-[normal] drop-shadow-lg">
              OSPITAL NG IMUS
            </h1>

            {/* Form section - centered */}
            <div className="absolute top-[120px] left-1/2 transform -translate-x-1/2">
              <form className="flex flex-col gap-5 items-center">
                {formFields.map((field) => (
                  <div key={field.id} className="relative">
                    <Input
                      id={field.id}
                      className="w-[450px] h-[58px] bg-white/95 backdrop-blur-sm rounded-[24px] shadow-[0px_4px_4px_#00000040] px-6 text-[26px] placeholder:text-[#838383]"
                      placeholder={field.placeholder}
                    />
                  </div>
                ))}

                {/* Birthday field with date picker */}
                <div className="relative">
                  <DatePicker
                    value={birthday}
                    onChange={setBirthday}
                    placeholder="Select birthday"
                    className="w-[450px] h-[58px]"
                  />
                </div>

                {/* Search button */}
                <Button className="w-[282px] h-[77px] mt-[42px] bg-[#05196a] rounded-[24px] shadow-[0px_4px_4px_#00000040] font-sans font-extrabold text-white text-[38px] hover:bg-[#041456] transition-colors">
                  SEARCH
                </Button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};