import React, { useState, useRef, useEffect } from 'react';
import { UserCircleIcon, ArrowLeftStartOnRectangleIcon } from '@heroicons/react/24/outline';

export function ProfileDropdown({ onLogout }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button 
        type="button" 
        onClick={() => setIsOpen(!isOpen)} 
        className="cursor-pointer rounded-full p-1 hover:bg-solid transition-colors"
      >
        <UserCircleIcon className="h-7 w-7 text-black" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-20 ring-1 ring-black ring-opacity-5">
          <div className="py-1">
            <button
              onClick={onLogout}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              <ArrowLeftStartOnRectangleIcon className="h-5 w-5 mr-3" />
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}