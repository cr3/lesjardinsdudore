import React from 'react';
import { useTranslation } from "react-i18next";
import i18n from "i18next";
import { LANGUAGES } from '../../i18n';
import {
  Icon, 
  CloseIcon, 
  SidebarContainer, 
  SidebarLang, 
  SidebarLangSelect, 
  SidebarLink, 
  SidebarMenu, 
  SidebarWrapper, 
} from './SidebarElements';

const Sidebar: React.FC<{isOpen: boolean, toggle: () => void}> = ({isOpen, toggle}) => {
  const { t } = useTranslation();

  const onChangeLang = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const lang_code = e.target.value;
    i18n.changeLanguage(lang_code);
  };

  return (
    <SidebarContainer isOpen={isOpen} onClick={toggle}>
      <Icon onClick={toggle}>
        <CloseIcon />
      </Icon>
      <SidebarWrapper>
        <SidebarMenu>
          <SidebarLink to='about' onClick={toggle}>
            {t("about")}
          </SidebarLink>
          <SidebarLink to='team' onClick={toggle}>
            {t("team")}
          </SidebarLink>
          <SidebarLink to='donate' onClick={toggle}>
            {t("donate")}
          </SidebarLink>
        </SidebarMenu>
        <SidebarLang>
          <SidebarLangSelect defaultValue={i18n.language} onChange={onChangeLang}>
            {LANGUAGES.map(({ code, label }) => (
              <option key={code} value={code}>
                {label}
              </option>
            ))}
          </SidebarLangSelect>
        </SidebarLang>
      </SidebarWrapper>
    </SidebarContainer>
  )
}

export default Sidebar
