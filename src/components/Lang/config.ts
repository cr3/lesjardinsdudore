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
            TADAM ! By arriving on this page, I hope that you will feel
            privileged because few people know about THE project. We
            decided it would be...`,
          projectLabel: "Project",
          projectTitle: "Over many years, in perpetual evolution",
          projectDescription: `
            We don't wish to rush - nature takes its time. And we are
            taking our time to take the temperature of our new community
            in Notre-Dame-du-Laus, see how the gardens develop, what
            will grow, what we can transform, and what the community
            needs. In real words, it's market research, but as we are
            anarchists and that we don't do things like everyone else,
            we'll just go with the flow.`,
          teamLabel: "Team",
          teamTitle: "Mary & Marc",
          teamDescription: `
            Maryannick, after years and years of learning, meeting
            peoples, internships, wwoofing, and readings, will finally go
            from plants to reality (anything can happen, even at 44 years of
            age!!) She decided to leave her salary temporarily to invest
            herself at 200% in the gardens. Marc too has learned about
            permaculture will spend his spare time at the side of Maryannick
            by offering support for logistics, decisions and this website.`,
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
