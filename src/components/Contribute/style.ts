import styled from 'styled-components';

export const ContributeContainer = styled.div`
    height: 1100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: #f9f9f9;

		@media screen and (max-width: 985px) {
        height: 1300px;
    }

    @media screen and (max-width: 885px) {
        height: 2300px;
    }

    @media screen and (max-width : 480px) {
        height: 2300px;
    }
`;

export const ContributeWrapper = styled.div`
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    grid-gap: 16px;
    padding: 0 50px;

    @media screen and (max-width: 1000px) {
        grid-template-columns: 1fr 1fr;
    }

    @media screen and (max-width: 768px) {
        grid-template-columns: 1fr;
        padding: 0 20px;
    }
`;

export const ContributeCard = styled.div`
    background: #010606;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    border-radius: 10px;
    max-height: 340px;
    padding: 30px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    transition: all 0.2s ease-in-out;
`;

export const ContributeLink = styled.a`
    color: #fff;
    font-size: 24px;
`;

export const ContributeIcon = styled.img`
    height: 160px;
    width: 160px;
    margin-bottom: 10px;
`;

export const ContributeH1 = styled.h1`
    font-size: 2.5rem;
    color: #010606;
    margin-bottom: 64px;

    @media screen and (max-width: 480px) {
        font-size: 2rem;
    }
`;

export const ContributeH2 = styled.h2`
    color: #fff;
    font-size: 1rem;
    margin-bottom: 10px;
`;

export const ContributeP = styled.p`
    color: #fff;
    font-size: 1rem;
    text-align: center;
`;