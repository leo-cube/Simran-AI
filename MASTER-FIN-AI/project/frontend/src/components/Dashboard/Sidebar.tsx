import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Home,
  Users,
  Calendar,
  Settings,
  HelpCircle,
  LogOut,
  CreditCard
} from 'lucide-react';

const Sidebar = () => {
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
  };

  return (
    <aside id="sidebar" className="fixed hidden z-20 h-full top-0 left-0 pt-16 lg:flex flex-shrink-0 flex-col w-64 transition-width duration-75">
      <div className="relative flex-1 flex flex-col min-h-0 border-r border-gray-200 bg-white pt-0">
        <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <div className="flex-1 px-3 space-y-1">
            <Link to="/dashboard" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <Home className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Dashboard</span>
            </Link>
            <Link to="/dashboard/chat" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <Users className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Chatbot</span>
            </Link>
            <Link to="/dashboard/pricing" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <CreditCard className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Pricing</span>
            </Link>
            <Link to="/dashboard/tetris" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <CreditCard className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Tetris</span>
            </Link>
            {/* <Link to="/dashboard/calendar" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <Calendar className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Calendar</span>
            </Link> */}
            {/* <Link to="/dashboard/settings" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <Settings className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Settings</span>
            </Link> */}
            <Link to="/dashboard/help" className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group">
              <HelpCircle className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Help</span>
            </Link>
            <button
              onClick={handleLogout}
              className="flex w-full items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
            >
              <LogOut className="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" />
              <span className="ml-3">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;