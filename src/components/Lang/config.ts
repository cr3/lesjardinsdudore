import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";

interface Language {
  code: string,
  label: string,
};

export const LANGUAGES: Language[] = [
  { code: "en", label: "English" },
  { code: "fr", label: "Français"},
];

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "fr",
    supportedLngs: LANGUAGES.map(l => l.code),
    interpolation: {
      escapeValue: false,
    },
    resources: {
      en: {
        translation: {
          title: "Doré Gardens",
          label: "Select another language!",
          about: "About",
          donate: "Donate",
          team: "Team",
        },
      },
      fr: {
        translation: {
          title: "Les jardins du Doré",
          label: "Choisir une autre langue!",
          about: "À propos",
          donate: "Faire un don",
          team: "L'équipe",
        },
      },
    },
  });

export default i18n;