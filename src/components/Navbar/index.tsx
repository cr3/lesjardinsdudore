import React, { useState, useEffect } from 'react';
import { FaBars } from 'react-icons/fa';
import { useTranslation } from "react-i18next";
import { animateScroll as scroll } from 'react-scroll';
import logo from '../../images/logo.png';
import Lang from '../Lang';
import {
    MobileIcon,
    Nav,
    NavbarContainer,
    NavMenu,
    NavItem,
    NavLang,
    NavLink,
} from './NavbarElements';


const Navbar: React.FC<{toggle: () => void}> = ({toggle}) => {
  const { t } = useTranslation();
  const [scrollNav, setScrollNav] = useState(false);

  //when scroll past 80px, trigger header background
  const changeNav = () => {
    if (window.scrollY >= 80) {
      setScrollNav(true)
    } else {
      setScrollNav(false)
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', changeNav)
  }, []);

  const toggleHome = () => {
    scroll.scrollToTop();
  };

  return (
    <>
      <Nav scrollNav={scrollNav}>
        <NavbarContainer>
          <img src={logo} alt={t("title")} onClick={toggleHome} />
          <MobileIcon onClick={toggle}>
            <FaBars />
          </MobileIcon>
          <NavMenu>
            <NavItem>
              <NavLink
                to="about"
                smooth={true}
                duration={500}
                spy={true}
                offset={-80}>
                  {t("about")}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                to="team"
                smooth={true}
                duration={500}
                spy={true}
                offset={-80}>
                  {t("team")}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                to="donate"
                smooth={true}
                duration={500}
                spy={true}
                offset={-80}>
                  {t("donate")}
              </NavLink>
            </NavItem>
          </NavMenu>
          <NavLang>
            <Lang />
          </NavLang>
        </NavbarContainer>
      </Nav>
    </>
  );
};

export default Navbar;