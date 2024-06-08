import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Cssfiles/Login.css';
import Navbar from './Navbar/Navbar';
import img from '../Asserts/LOG.jpg';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const response = await axios.post('http://localhost:5005/api/login', {
        email: email,
        password: password,
      });
  
      if (response.data && response.data.message === 'Connexion réussie') {
        const user_id=response.data.user_id;
        console.log(user_id);
        sessionStorage.setItem('user_id', user_id);
        // Rediriger l'utilisateur vers la page d'accueil après la connexion réussie
        navigate('/Accueil');
      } else {
        setErrorMessage('Adresse email ou mot de passe incorrect');
      }
    } catch (error) {
      console.error('Error during login:', error);
      setErrorMessage('Une erreur est survenue lors de la connexion');
    }
  };
  
  return (
    <>
      <Navbar />
      <div className="login-container">
        <div className="login-image"> 
            <img src={img} alt="Description de l'image" />
         </div>
        <div className="login-form">
          <h2>Connexion</h2>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={handleEmailChange}
                required
              />
              <label htmlFor="password">Mot de passe </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={handlePasswordChange}
                required
              />
            </div>
            <button type="submit">Se connecter</button>
            <div className="signup-link">
              <p>Vous avez oubliez votre password? <Link to="/SignupForm">Contactez l'administration</Link></p>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Login;


