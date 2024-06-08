// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './component/Login';
import Search from './component/search'
import Accueil from './component/Home/accueil';
import Page1 from './component/Page1';




function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Page1/>} />   
        <Route path="Login" element={<Login/>}  />
        <Route path="Accueil" element={<Accueil/>}  />
        <Route path="/search" element={<Search/>}  />
      </Routes>
    </Router>
  )
}
export default App;
