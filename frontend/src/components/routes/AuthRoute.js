import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const AnonymousRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    isAuthenticated ? <Navigate to="/" /> : children
  );
};

const AuthRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    isAuthenticated ? children : <Navigate to="/" />
  );
};

export {
  AnonymousRoute,
  AuthRoute,
};
