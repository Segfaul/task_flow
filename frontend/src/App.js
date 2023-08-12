import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Logout from './components/auth/Logout';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthRoute, AnonymousRoute } from './components/routes/AuthRoute'

const App = () => {
  return (
    <Router>
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path='/logout' element={
              <AuthRoute>
                <Logout />
              </AuthRoute>
              }>
            </Route>
            <Route path="/login" element={
              <AnonymousRoute>
                <Login />
              </AnonymousRoute>
              } 
            />
            <Route path="/register" element={
              <AnonymousRoute>
                <Register />
              </AnonymousRoute>
              }
            />
          </Routes>
        </main>
        <Footer />
        <ToastContainer className="toast-position" position="top-right" autoClose={1500} />
    </Router>
  );
};

export default App;
