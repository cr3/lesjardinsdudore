import React from 'react';
import Home from './pages';
import Plantes from './pages/Plantes';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "@fontsource/roboto";
import './components/Lang/config';
import './App.css';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/plantes" element={<Plantes />} />
      </Routes>
    </BrowserRouter>
  );

};

export default App;