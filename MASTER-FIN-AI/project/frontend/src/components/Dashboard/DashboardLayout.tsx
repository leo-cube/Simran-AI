import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

const DashboardLayout = () => {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1">
        <Navbar />
        <main className="p-4 md:p-6 pt-20 md:ml-64">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;