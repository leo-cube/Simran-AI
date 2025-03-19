import React from 'react';
import { Bell, Search, Settings, User } from 'lucide-react';

const Navbar = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  return (
    <nav className="bg-white border-b border-gray-200 fixed z-30 w-full">
      <div className="px-3 py-3 lg:px-5 lg:pl-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center justify-start">
            <button id="toggleSidebarMobile" aria-expanded="true" aria-controls="sidebar" className="lg:hidden mr-2 text-gray-600 hover:text-gray-900 cursor-pointer p-2 hover:bg-gray-100 focus:bg-gray-100 focus:ring-2 focus:ring-gray-100 rounded">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd"></path>
              </svg>
            </button>
            <div className="text-xl font-bold flex items-center lg:ml-2.5">
              <span className="self-center whitespace-nowrap">Dashboard</span>
            </div>
          </div>
          <div className="flex items-center">
            <div className="hidden md:flex items-center mx-4">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
                <input
                  type="text"
                  className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                  placeholder="Search..."
                />
              </div>
            </div>
            <button className="p-2 text-gray-500 rounded-lg hover:text-gray-900 hover:bg-gray-100">
              <Bell className="w-6 h-6" />
            </button>
            <button className="p-2 text-gray-500 rounded-lg hover:text-gray-900 hover:bg-gray-100 ml-2">
              <Settings className="w-6 h-6" />
            </button>
            <div className="flex items-center ml-3">
              <div className="relative">
                <button className="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300">
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
                    <User className="w-5 h-5" />
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;