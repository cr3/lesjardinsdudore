import React, { useState, useEffect } from 'react';
import { FaBars } from 'react-icons/fa';
import { useTranslation } from "react-i18next";
import { animateScroll as scroll } from 'react-scroll';
import i18n from "i18next";
import {
    MobileIcon,
    Nav,
    NavbarContainer,
    NavMenu,
    NavItem,
    NavLang,
    NavLangSelect,
    NavLink,
} from './NavbarElements';
import { LANGUAGES } from '../../i18n';
import logo from '../../images/logo.png';


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

  const onChangeLang = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const lang_code = e.target.value;
    i18n.changeLanguage(lang_code);
  };

  return (
    <>
      <Nav scrollNav={scrollNav}>
        <NavbarContainer>
          <img src={logo} alt="Les jardins du Doré" onClick={toggleHome} />
          <MobileIcon onClick={toggle}>
            <FaBars />
          </MobileIcon>
          <NavMenu>
            <NavItem>
              <NavLink to="about"
                smooth={true}
                duration={500}
                spy={true}
                offset={-80}>
                  {t("about")}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="team"
                smooth={true}
                duration={500}
                spy={true}
                offset={-80}>
                  {t("team")}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="donate"
                smooth={true}
                duration={500}
                spy={true}
                offset={-80}>
                  {t("donate")}
              </NavLink>
            </NavItem>
          </NavMenu>
          <NavLang>
            <NavLangSelect defaultValue={i18n.language} onChange={onChangeLang}>
              {LANGUAGES.map(({ code, label }) => (
                <option key={code} value={code}>
                  {label}
                </option>
              ))}
            </NavLangSelect>
          </NavLang>
        </NavbarContainer>
      </Nav>
    </>
  );
};

export default Navbar;