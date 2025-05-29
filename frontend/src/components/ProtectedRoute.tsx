import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { authAPI } from '../services/api';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAdmin?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requireAdmin = false }) => {
  const location = useLocation();
  const [isVerifying, setIsVerifying] = useState(true);
  const [isValid, setIsValid] = useState(false);

  useEffect(() => {
    const verifyToken = async () => {
      try {
        const token = requireAdmin ? localStorage.getItem('adminToken') : localStorage.getItem('access_token');
        
        if (!token) {
          setIsValid(false);
          return;
        }

        // Verify the token
        await authAPI.verifyToken();
        setIsValid(true);
      } catch (error) {
        console.error('Token verification failed:', error);
        // Clear invalid tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('adminToken');
        setIsValid(false);
      } finally {
        setIsVerifying(false);
      }
    };

    verifyToken();
  }, [requireAdmin]);

  if (isVerifying) {
    return null; // or a loading spinner
  }

  if (requireAdmin && !isValid) {
    return <Navigate to="/admin/login" state={{ from: location }} replace />;
  }

  if (!requireAdmin && !isValid) {
    return <Navigate to="/auth" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute; 