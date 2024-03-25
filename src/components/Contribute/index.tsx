import React from 'react';
import { useTranslation } from "react-i18next";
import Euro from '../../images/euro.png';
import Interac from '../../images/interac.png';
import Paypal from '../../images/paypal.png';
import Wise from '../../images/wise.png';
import Time from '../../images/time.png';
import Ideas from '../../images/ideas.png';
import {
  ContributeContainer,
  ContributeH1,
  ContributeLink,
  ContributeWrapper,
  ContributeCard,
  ContributeIcon,
  ContributeH2,
  ContributeP 
} from './style';

const Contribute: React.FC = () => {
const { t } = useTranslation();

  return (
    <ContributeContainer id="contribute">
      <ContributeH1>{t("contribute")}</ContributeH1>
      <ContributeWrapper>
        <ContributeCard>
          <ContributeIcon src={Euro} />
          <ContributeH2>En espèces</ContributeH2>
          <ContributeP>Lors de l'événement!</ContributeP>
        </ContributeCard>
        <ContributeCard>
          <ContributeIcon src={Time} />
          <ContributeH2>En temps</ContributeH2>
          <ContributeP>Pour les voyageurs et ceux qui habitent le continent.</ContributeP>
        </ContributeCard>
        <ContributeCard>
          <ContributeIcon src={Ideas} />
          <ContributeH2>En compétences</ContributeH2>
          <ContributeP>Votre expérience est précieuse à nos yeux.</ContributeP>
        </ContributeCard>
        <ContributeCard>
          <ContributeIcon src={Wise} />
          <ContributeH2>Virement à l'international</ContributeH2>
          <ContributeP>
            <ContributeLink href="https://wise.com/pay/r/jylnNv6nbKwbo5I">20</ContributeLink>,&nbsp;
            <ContributeLink href="https://wise.com/pay/r/20RMMxDXBVohZtk">50</ContributeLink>,&nbsp;
            <ContributeLink href="https://wise.com/pay/r/yrLtj8-vm2Y_S4I">100</ContributeLink> EUR
          </ContributeP>
        </ContributeCard>
        <ContributeCard>
          <ContributeIcon src={Interac} />
          <ContributeH2>Virement au Canada</ContributeH2>
          <ContributeP>marc@lesjardinsdudore.ca</ContributeP>
        </ContributeCard>
        <ContributeCard>
          <ContributeIcon src={Paypal} />
          <ContributeH2>Virement en CAD</ContributeH2>
          <ContributeP>
            <ContributeLink href='https://www.paypal.com/pools/c/92Y6lpgyrc'>Paypal</ContributeLink>
          </ContributeP>
        </ContributeCard>
      </ContributeWrapper>
    </ContributeContainer>
  )
}

export default Contribute
