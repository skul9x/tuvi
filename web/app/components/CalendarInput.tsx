// web/app/components/CalendarInput.tsx
"use client";

import { useEffect, useState } from "react";

interface CalendarInputProps {
  day: number;
  month: number;
  year: number;
  onChange: (day: number, month: number, year: number) => void;
}

export default function CalendarInput({ day, month, year, onChange }: CalendarInputProps) {
  const [daysInMonth, setDaysInMonth] = useState(31);

  useEffect(() => {
    const getDaysInMonth = (y: number, m: number) => {
      return new Date(y, m, 0).getDate();
    };
    const totalDays = getDaysInMonth(year, month);
    setDaysInMonth(totalDays);
    if (day > totalDays) {
      onChange(totalDays, month, year);
    }
  }, [day, month, year, onChange]);

  const handleDayChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(parseInt(e.target.value), month, year);
  };

  const handleMonthChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(day, parseInt(e.target.value), year);
  };

  const handleYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(day, month, parseInt(e.target.value));
  };

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 120 }, (_, i) => currentYear - i);

  const inputClasses = "w-full bg-slate-900/50 border-b border-white/20 text-slate-50 px-4 py-3 outline-none transition-all duration-300 focus:border-amber-400 focus:bg-slate-900/80 rounded-lg appearance-none cursor-pointer text-sm sm:text-base";
  const labelClasses = "text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 block";

  return (
    <div className="grid grid-cols-3 gap-2 sm:gap-4">
      <div className="group">
        <label className={labelClasses}>Ngày</label>
        <div className="relative">
          <select value={day} onChange={handleDayChange} className={inputClasses}>
            {Array.from({ length: daysInMonth }, (_, i) => i + 1).map((d) => (
              <option key={d} value={d} className="bg-slate-900 text-slate-50">{d}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="group">
        <label className={labelClasses}>Tháng</label>
        <div className="relative">
          <select value={month} onChange={handleMonthChange} className={inputClasses}>
            {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
              <option key={m} value={m} className="bg-slate-900 text-slate-50">{m}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="group">
        <label className={labelClasses}>Năm</label>
        <div className="relative">
          <select value={year} onChange={handleYearChange} className={inputClasses}>
            {years.map((y) => (
              <option key={y} value={y} className="bg-slate-900 text-slate-50">{y}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
