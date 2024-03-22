import React from 'react';
import { useTranslation } from "react-i18next";
import Lang from '../Lang';
import {
  Icon, 
  CloseIcon, 
  SidebarContainer, 
  SidebarLang, 
  SidebarLink, 
  SidebarMenu, 
  SidebarWrapper, 
} from './style';

const Sidebar: React.FC<{isOpen: boolean, toggle: () => void}> = ({isOpen, toggle}) => {
  const { t } = useTranslation();

  return (
    <SidebarContainer isOpen={isOpen} onClick={toggle}>
      <Icon onClick={toggle}>
        <CloseIcon />
      </Icon>
      <SidebarWrapper>
        <SidebarMenu>
          <SidebarLink to='team' onClick={toggle}>
            {t("teamLabel")}
          </SidebarLink>
          <SidebarLink to='project' onClick={toggle}>
            {t("projectLabel")}
          </SidebarLink>
          <SidebarLink to='contribute' onClick={toggle}>
            {t("contribute")}
          </SidebarLink>
        </SidebarMenu>
        <SidebarLang>
          <Lang />
        </SidebarLang>
      </SidebarWrapper>
    </SidebarContainer>
  )
}

export default Sidebar
