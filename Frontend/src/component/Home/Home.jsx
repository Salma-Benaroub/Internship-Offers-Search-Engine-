import React from 'react';
import './home.css';
import video from '../../Asserts/video.mp4';
import { FiFacebook } from 'react-icons/fi';
import { AiOutlineInstagram } from 'react-icons/ai';
import { BsListTask } from 'react-icons/bs';
import { TbApps } from 'react-icons/tb';

function Home() {
  return (
    <section className='homee'>
      <div className="overlay"></div>
      <video src={video} muted autoPlay loop type="video/mp4" />
      
      <div className="homeContent">
        <div className="textDiv">
          <h1 className='homeTitle'>Exploring internship opportunities: Navigating your path to professional growth</h1><br></br>
      
            <p className='description'> 
              Discover a dynamic online platform designed to assist students in finding internships tailored to their academic interests and career goals. InternHub provides a centralized hub for accessing a diverse range of internship listings from leading companies and organizations. Our intuitive interface enables students to effortlessly browse, filter, and apply for internships that match their skill sets and aspirations.
            </p>
         
        </div>

        <div className="cardDiv grid">
          {/* Contenu des cartes ici */}
        </div>

        <div className="homeFooterIcon flex">
          <div className="rightIcons">
            <FiFacebook className='icon' />
            <AiOutlineInstagram className='icon' />
          </div>
          <div className="leftIcons">
            <BsListTask className='icon'/>
            <TbApps className='icon'/>
          </div> 
        </div>
      </div>
    </section>
  );
}

export default Home;