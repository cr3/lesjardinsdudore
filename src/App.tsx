import React from 'react';
import Home from './pages';
import { BrowserRouter } from 'react-router-dom';
import "@fontsource/roboto";
import './i18n';
import './App.css';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Home />
    </BrowserRouter>
  );

};

export default App;