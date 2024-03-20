import React from 'react';
import { useTranslation } from "react-i18next";
import {animateScroll as scroll } from 'react-scroll';
import {
  FooterAddress, 
  FooterContainer, 
  FooterWrap, 
  SocialMedia,
  SocialMediaWrap,
  SocialLogo,
} from './FooterElements';

const Footer: React.FC = () => {
  const { t } = useTranslation();

  const toggleHome = () => {
    scroll.scrollToTop();
  };

  return (
    <FooterContainer id='footer'>
      <FooterWrap>
        <SocialMedia>
          <SocialMediaWrap>
            <SocialLogo to="/" onClick={toggleHome}>
              {t("title")}
            </SocialLogo>
            <FooterAddress>
              58 chemin du Doré, Notre-Dame-du-Laus (Québec) J0M2M0
            </FooterAddress>
          </SocialMediaWrap>
        </SocialMedia>
      </FooterWrap>
    </FooterContainer>
  )
};

export default Footer;