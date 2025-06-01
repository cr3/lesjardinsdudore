import React, { useState } from 'react';
import i18n from "i18next";
import { LangButton } from './style';
import { LANGUAGES } from './config';

const nextLanguage = () => {
  const code = i18n.resolvedLanguage
  const currentIndex = LANGUAGES.findIndex(l => l.code === code)
  const nextIndex = (currentIndex + 1) % LANGUAGES.length
  return LANGUAGES[nextIndex];
}

const Lang: React.FC = () => {
  const [lang, setLang] = useState(nextLanguage())

  const toggleLang = () => {
    i18n.changeLanguage(lang.code)
    setLang(nextLanguage())
  };

  return (
    <LangButton
      onClick={toggleLang}
    >
      {lang.label}
    </LangButton>
  );
};

export default Lang;