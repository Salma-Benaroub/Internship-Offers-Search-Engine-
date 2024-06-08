import React, { useState } from 'react';
import './navbar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGraduationCap } from '@fortawesome/free-solid-svg-icons'; 

import { AiFillCloseCircle } from "react-icons/ai";
import { TbGridDots } from "react-icons/tb";

function Navbar() {
    const [active, setActive] = useState('navBar');

    const showNav = () => {
      setActive('navBar activeNavbar');
    };

    const removeNavbar = () => {
      setActive('navBar');
    };

    return (
      <section className='navBarSection'>
        <header className='header flex'>

          <div className='logoDiv'>
            <a href='' className='logo flex'>
              <h1><FontAwesomeIcon icon={faGraduationCap} style={{ color: "hsl(199,100%,33%) "}} /> ENSAInternGuide</h1>
            </a>
          </div>

          <div className={active}>
            <ul className='navLists flex'>

              <li className='navItem'>
                <a href= "/" className='navLink'>Home</a>
              </li>

              <li className='navItem'>
                <a href= "#about" className='navLink'>About</a>
              </li>

              <li className='navItem'>
                <a href= "#reviews" className='navLink'>Reviews</a>
              </li>
            
              <li className='navItem'>
                <a href= "#contact" className='navLink'>Contact</a>
              </li>

              <button className='btn'>
                <a href='/Login'> Espace Etudiant</a>
              </button>

            </ul>

          <div onClick={removeNavbar} className="closeNavbar"> 
            <AiFillCloseCircle className='icon'/>
          </div>

          </div>

          <div onClick={showNav} className="toggleNavbar">
            <TbGridDots className='icon'/>
          </div>
        </header>
      </section>
    );
}

export default Navbar;
