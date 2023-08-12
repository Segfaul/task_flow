import React, { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { toast } from 'react-toastify';
import client from '../config/client';

const Logout = () => {
    const { setIsAuthenticated, setUsername: setAuthUsername } = useContext(AuthContext);
    const history = useNavigate();

    const logout = async () => {
        try {
            await client.get('/api/logout/');
            setIsAuthenticated(false);
            setAuthUsername('');
      
            toast.success(`Logout Success`);

        } catch (err) {
            if (err.response) {

                const responseData = JSON.parse(err.response.request.response);
      
                const response = Object.values(responseData)[0]
      
                toast.error(`${response}`);
            }
        } finally{
            history('/');
        }
    };

    useEffect(() => {
        logout();
    });

    return <div>Выход...</div>;
};

export default Logout;