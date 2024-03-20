import i18n from "i18next";
import { initReactI18next } from "react-i18next";

export const LANGUAGES = [
  { label: "Français", code: "fr" },
  { label: "English", code: "en" },
];

i18n
  .use(initReactI18next)
  .init({
    fallbackLng: "fr",
    lng: "fr",
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