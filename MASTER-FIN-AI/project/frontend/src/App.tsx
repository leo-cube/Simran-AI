import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import DashboardLayout from './components/Dashboard/DashboardLayout';
import DashboardHome from './pages/Dashboard/Home';
import PricingPage from './pages/Dashboard/PricingPage';
import PrivateRoute from './utils/PrivateRoute';
import CustomModel from './pages/Dashboard/Custom_model';
import HelpPage from './pages/Dashboard/Help';

function App() {
  const token = localStorage.getItem('token');

  return (
    <Router>
      <Routes>
        <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Login onToggle={() => {}} />} />
        <Route path="/signup" element={token ? <Navigate to="/dashboard" /> : <Signup onToggle={() => {}} />} />
        
        <Route path="/dashboard" element={
          <PrivateRoute>
            <DashboardLayout />
          </PrivateRoute>
        }>
          <Route index element={<DashboardHome />} />
          <Route path="pricing" element={<PricingPage />} />
          <Route path="chat" element={<CustomModel />} />
          <Route path="help" element={<HelpPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;