import React, { useState } from 'react';
import { useTranslation } from "react-i18next";
import Footer from '../components/Footer';
import Contribute from '../components/Contribute';
import Hero from '../components/Hero';
import Info from '../components/Info';
import { project, team } from '../components/Info/Data';
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
      <Info {...team(t)} />
      <Info {...project(t)} />
      <Contribute />
      <Footer />
    </>
  );
};

export default Home;