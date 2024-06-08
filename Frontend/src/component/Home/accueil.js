import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './accueil.css';  // Assurez-vous de créer un fichier CSS pour les styles
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons'
import Navbar from '../Navbar/Navbar';

function Accueil() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:5000/offers');
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  return (
    <>
    <Navbar/>
    <div className="home-containe">
      <aside className="sidebar">
        <ul>
          <li>
            <a href="/search">
              <FontAwesomeIcon icon={faUser} className="icon" />
              Search page
            </a>
          </li>
          <li>
            <a href="#settings">
              <FontAwesomeIcon icon={faCog} className="icon" />
              Settings
            </a>
          </li>
          <li>
            <a href="Login">
              <FontAwesomeIcon icon={faSignOutAlt} className="icon" />
              Logout
            </a>
          </li>
        </ul>
      </aside>
      <div className='hh'>
      <div className="home">
        <main>
          {categories.map((category, index) => (
            <section key={index} className="category">
              <h2>{category.name}</h2>
              <div className="offers">
                {category.offers.map((offer, index) => (
                  <div key={index} className="offer">
                    <h3>{offer.titre}</h3>
                    <p>{offer.description}</p>
                    <a href={offer.lien} target="_blank" rel="noopener noreferrer">En savoir plus</a>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </main>
      </div>
    </div>
    </div>
    </>
  );
}

export default Accueil;
