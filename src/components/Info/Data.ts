import Mnm from '../../images/mnm.png'
import Plan from '../../images/plan.png'

type T = (x: string) => void

export function team(t: T) {
  return {
    id: 'team',
    lightBg: true,
    lightText: false,
    lightTextDesc: false,
    topLine: t("teamLabel"),
    headline: t("teamTitle"),
    description: t("teamDescription"),
    imgStart: true,
    img: Mnm,
    alt: 'M&M',
    darkText: true,
  };
}

export function project(t: T) {
  return {
    id: 'project',
    lightBg: false,
    lightText: true,
    lightTextDesc: true,
    topLine: t("projectLabel"),
    headline: t("projectTitle"),
    description: t("projectDescription"),
    imgStart: false,
    img: Plan,
    alt: 'Plan',
    darkText: false,
  };
}