import React, { useState } from 'react';
import { useTranslation } from "react-i18next";
import Footer from '../components/Footer';
import Hero from '../components/Hero';
import Info from '../components/Info';
import { about, team, donate } from '../components/Info/Data';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

const Home: React.FC = () => {
  const { t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)

  const toggle = () => {
    setIsOpen(!isOpen)
  };

  return (
    <>
      <Sidebar isOpen={isOpen} toggle={toggle} />
      <Navbar toggle={toggle} />
      <Hero />
      <Info {...about(t)} />
      <Info {...team(t)} />
      <Info {...donate(t)} />
      <Footer />
    </>
  );
};

export default Home;