import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import client from '../config/client';
import { AuthContext } from '../context/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const { setIsAuthenticated, setUsername: setAuthUsername } = useContext(AuthContext);
  const history = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await client.post('/api/login/', {
        username,
        password,
      });

      setIsAuthenticated(true);
      setAuthUsername(response.data.username);

      console.log(response);

      toast.success(`Welcome back, ${response.data.username}`);

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
      <h1>Login</h1>
      <form className='authentication-form' onSubmit={handleLogin}>
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
        <button className='authentication-form-submit' type="submit">Login</button>
      </form>
      <div className='authentication-description'>
        Don't have an account? <Link className='authentication-description-link' to="/register">Register</Link>
      </div>
    </div>
  );
};

export default Login;
