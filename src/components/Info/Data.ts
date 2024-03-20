import Dirt from '../../images/dirt.png'
import Mnm from '../../images/mnm.png'
import Rene from '../../images/rene.png'

type T = (x: string) => void

export function about(t: T) {
  return {
    id: 'about',
    lightBg: true,
    lightText: false,
    lightTextDesc: false,
    topLine: t("about"),
    headline: t("title"),
    description: 'TODO',
    imgStart: true,
    img: Dirt,
    alt: '...',
    darkText: true,
  };
}

export function team(t: T) {
  return {
    id: 'team',
    lightBg: false,
    lightText: true,
    lightTextDesc: true,
    topLine: t("team"),
    headline: "Mary & Marc",
    description: 'TODO',
    imgStart: false,
    img: Mnm,
    alt: 'M&M',
    darkText: false,
  };
}

export function donate(t: T) {
  return {
    id: 'donate',
    lightBg: true,
    lightText: false,
    lightTextDesc: false,
    topLine: t("donate"),
    headline: "TODO",
    description: 'TODO',
    imgStart: true,
    img: Rene,
    alt: 'René',
    darkText: true,
  };
}
