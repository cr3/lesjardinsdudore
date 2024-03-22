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
          title: "Les jardins du Doré",
          contribute: "Contribute!",
          intro: `
            TADAM ! En arrivant sur cette page, j'espère que vous vous
            sentirez privilégiés, parce qu'il n'y pas grand monde à
            qui nous avons parlé DU projet. On a décidé que ce serait...`,
          projectLabel: "Project",
          projectTitle: "Sur plusieurs années, en perpétuelle évolution",
          projectDescription: `
            Nous ne souhaitons pas rusher, la nature prend son temps. Et
            nous prenons le temps de prendre la température de notre
            nouvelle communauté lausoise, pour voir comment les jardins
            se développeront, ce que nous serons capables d’y produire
            et de transformer, ce que la communauté aurait besoin. En
            vrais mots, c’est une étude de marché, mais comme nous
            sommes un peu anarchistes, et que nous n’aimons pas faire
            les chose comme du monde, ben, on va suivre le flow.`,
          teamLabel: "Team",
          teamTitle: "Mary & Marc",
          teamDescription: `
            Maryannick après des années, et des années
            d’apprentissages, rencontres, stages, wwoofing, lectures,
            va enfin pouvoir passer des plans à la réalité (comme
            quoi tout arrive, même à 44 ans!!) Elle a fait le choix
            de lâcher le salariat temporairement pour s’investir
            à 200 % de son temps dans les jardins. Marc a lui aussi
            suivi une formation en permaculture, et garde son emploi,
            il occupera ses temps libres à s’investir aux côtés
            de Maryannick, et en continuant son support logistique,
            décisionnel, et la création du site.`,
        },
      },
      fr: {
        translation: {
          title: "Les jardins du Doré",
          contribute: "Contribuez!",
          intro: `
            TADAM ! En arrivant sur cette page, j'espère que vous vous
            sentirez privilégiés, parce qu'il n'y pas grand monde à
            qui nous avons parlé DU projet. On a décidé que ce serait...`,
          projectLabel: "Le projet",
          projectTitle: "Sur plusieurs années, en perpétuelle évolution",
          projectDescription: `
            Nous ne souhaitons pas rusher, la nature prend son temps. Et
            nous prenons le temps de prendre la température de notre
            nouvelle communauté lausoise, pour voir comment les jardins
            se développeront, ce que nous serons capables d’y produire
            et de transformer, ce que la communauté aurait besoin. En
            vrais mots, c’est une étude de marché, mais comme nous
            sommes un peu anarchistes, et que nous n’aimons pas faire
            les chose comme du monde, ben, on va suivre le flow.`,
          teamLabel: "L'équipe",
          teamTitle: "Mary & Marc",
          teamDescription: `
            Maryannick après des années, et des années
            d’apprentissages, rencontres, stages, wwoofing, lectures,
            va enfin pouvoir passer des plans à la réalité (comme
            quoi tout arrive, même à 44 ans!!) Elle a fait le choix
            de lâcher le salariat temporairement pour s’investir
            à 200 % de son temps dans les jardins. Marc a lui aussi
            suivi une formation en permaculture, et garde son emploi,
            il occupera ses temps libres à s’investir aux côtés
            de Maryannick, et en continuant son support logistique,
            décisionnel, et la création du site.`,
        },
      },
    },
  });

export default i18n;