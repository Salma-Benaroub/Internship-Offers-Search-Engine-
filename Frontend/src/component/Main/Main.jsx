import React from 'react'
import './main.css'
import img3 from '../../Asserts/2.jpg'
import img4 from '../../Asserts/1.jpg'
import img5 from '../../Asserts/3.jpg'
import img6 from '../../Asserts/ensa.png'
//import icons


function Main() {
  return (
    <>
    <section className="about container section" id="about">
    <div className="secTitle2" >
        <h3 className='title2'>The purpose of this platform</h3>
    </div>
    <div className="about-container">
      <div className="about-img">
        <img src={img6} style={{width:"350px", marginLeft:"50px"}} alt="Internship" />
      </div>
      <div className="about-text">
        <span>About us</span>
         <p>At <b>ENSAInternGuide</b>, we are dedicated to empowering ENSA students in their journey to secure valuable internship opportunities.Our platform serves as a centralized hub where students can easily access a wide range of internship listings, tailored to their academic and professional interests. We understand the challenges and complexities of finding the right internship, which is why we provide intuitive search tools, up-to-date information, and personalized support.</p>
          <p>Our mission is to bridge the gap between students and industry professionals, facilitating meaningful connections that pave the way for future careers. With ENSAInternGuide, students can confidently navigate their internship search and unlock their full potential.</p>
        <a href="/login" className="btn">Go start !</a>
      </div>
    </div>
  </section>
  
  <section className="reviews container section" id="reviews">
     <div className="secTitle3" >
        <h3 className="title3">Experiences of our users</h3>
      </div>
      <div className="reviews-container">
        <div className="box">
          <div className="rev-img">
            <img src={img3} alt="client" />
          </div>
          <h2>Salim Barkaoui</h2>
          <div className="stars">
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star-half'></i>
          </div>
          <p>Thanks to ENSAInternGuide, I found my dream internship in record time. The platform is incredibly user-friendly, and the listings are always up-to-date. It made the entire process seamless and stress-free. I highly recommend it to all my peers!</p>
        </div>

        <div className="box">
          <div className="rev-img">
            <img src={img5} alt="client" />
          </div>
          <h2>Manal Hilali</h2>
          <div className="stars">
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
          </div>
          <p>ENSAInternGuide made my internship search so much easier. The advanced search filters are highly effective, and I quickly found several opportunities that were a perfect fit for my skills and interests. Plus, the responses from companies were prompt and professional.</p>
        </div>

        <div className="box">
          <div className="rev-img">
            <img src={img4} alt="client" />
          </div>
          <h2>Saad Miftah</h2>
          <div className="stars">
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star'></i>
            <i className='bx bxs-star-half'></i>
          </div>
          <p>I'm incredibly grateful for ENSAInternGuide. What used to be a stressful and overwhelming task of finding an internship turned into a smooth and efficient process. With the resources and tips provided on the site, I landed an internship at a prestigious company.</p>
        </div>
      </div>
    </section>

    <section id="contact" className="section-contact container section">

    <div className="secTitle4" >
        <h3 className="title4">If you have any questions</h3>
      </div>
      <form >
        <div className="form-nom-email">
          <div className="form-column">
            <label htmlFor="nom"><b>Nom</b></label>
            <input
              type="text"
              name="nom"
              id="nom"
            />
          </div>
          <div className="form-column">
            <label htmlFor="nom"><b>Email</b></label>
            <input
              type="text"
              name="nom"
              id="nom"
            />
          </div>
        </div>
        <label htmlFor="message"><b>Message</b></label>
        <textarea
          name="message"
          id="message"
          rows="10"
        />
        <a href="#contact" className="btn1">Send</a>
      </form>
    
    </section>
    </>
  )
}

export default Main