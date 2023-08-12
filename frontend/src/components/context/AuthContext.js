import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const storedAuth = JSON.parse(localStorage.getItem('auth'));
    if (storedAuth) {
      setIsAuthenticated(storedAuth.isAuthenticated);
      setUsername(storedAuth.username);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('auth', JSON.stringify({ isAuthenticated, username }));
  }, [isAuthenticated, username]);

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, username, setUsername }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
