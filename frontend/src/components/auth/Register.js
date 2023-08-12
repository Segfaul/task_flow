import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import client from '../config/client';
import { AuthContext } from '../context/AuthContext';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const { setIsAuthenticated, setUsername: setAuthUsername } = useContext(AuthContext);
  const history = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await client.post('/api/register/', {
        username,
        password,
      });

      setIsAuthenticated(true);
      setAuthUsername(response.data.username);

      toast.success("You're successfully registered");

      history('/');

    } catch (err) {
      if (err.response) {

        const responseData = JSON.parse(err.response.request.response);

        const response = Object.values(responseData)[0]

        toast.error(`${response}`);
      }
    }
  };

  return (
    <div className='authentication'>
      <h1>Register</h1>
      <form className='authentication-form' onSubmit={handleRegister}>
        <input
          className='authentication-form-field'
          type="text"
          placeholder="Login"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className='authentication-form-field'
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className='authentication-form-submit' type="submit">Register</button>
      </form>
      <div className='authentication-description'>
        Already have an account? <Link className='authentication-description-link' to="/login">Login</Link>
      </div>
    </div>
  );
};

export default Register;
