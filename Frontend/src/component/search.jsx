import React, { useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar/Navbar';
import './Cssfiles/search.css';
import img from '../Asserts/LG.png'
import { IoSearch } from "react-icons/io5";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons'

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:5000/search?query=${query}`);
      setResults(response.data.results);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setLoading(false);
    }
  };

  return (
    <>
    <Navbar />
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
            <a href="#logout">
              <FontAwesomeIcon icon={faSignOutAlt} className="icon" />
              Logout
            </a>
          </li>
        </ul>
      </aside>
    <div className='form-container'>
    <div className='form-form'>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%', height: '150px' }}>
          <img src={img} alt="Description de l'image" style={{ width: '210px', height: 'auto' }} />
        </div>
            <h1 >Discover your internship on our platform !</h1>
            <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center' }}>
              <input type="text" value={query} onChange={handleChange}
                placeholder="Enter your search query..."
              />
              <button type="submit" style={{marginLeft: '20px',marginBottom:'16px', fontSize:"15px"}}>Search <IoSearch  className='icon'/></button>
              </div>
      </form>
      {loading && <p style={{ textAlign: 'center', fontStyle: 'italic' }}>Loading...</p>}
      {results.length > 0 ? (
        <div>
          <h2 style={{ marginBottom: '10px' ,color : 'hsl(240,4%,36%)' , fontSize:'18px'}}>Show results:</h2>
          <ul style={{ listStyleType: 'none', padding: '0' }}>
            {results.map((result, index) => (
              <li key={index} style={{ marginBottom: '20px' }}>
                <div style={{ border: '1px solid #ccc', borderRadius: '5px', padding: '10px' }}>
                  <a href={result.lien} target="_blank" rel="noopener noreferrer" style={{fontSize: '17px'}} >
                    {result.titre}
                  </a>
                  <p style={{ fontSize: '14px', color: '#666', marginTop: '5px' }}>{result.description} + Clic on the title for looking more</p>
                </div>
              </li>
            ))}
          </ul>

        </div>
      ) : (
        !loading && <p style={{ textAlign: 'center' }}></p>
      )}
    </div>
    </div>
    </>
  );
}

export default App;