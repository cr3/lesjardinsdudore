import React from 'react';
import { InfoContainer, 
    InfoWrapper, 
    InfoRow, 
    Column1, 
    Column2, 
    TextWrapper, 
    TopLine, 
    Heading, 
    Subtitle, 
    ImgWrap,
    Img,
    } from './style';

const Info: React.FC<{
  lightBg: boolean,
  imgStart: boolean,
  id: string,
  topLine: any, 
  lightText: boolean, 
  headline: any, 
  darkText: boolean, 
  description: any,
  img: any,
  alt: string,
}> = ({
  lightBg, 
  imgStart, 
  id, 
  topLine, 
  lightText, 
  headline, 
  darkText, 
  description, 
  img, 
  alt,
}) => {
  return (
    <>
      <InfoContainer lightBg={lightBg} id={id}>
        <InfoWrapper>
          <InfoRow imgStart={imgStart}>
            <Column1>
            <TextWrapper>
              <TopLine>{topLine}</TopLine>
              <Heading lightText={lightText}>{headline}</Heading>
              <Subtitle darkText={darkText}>{description}</Subtitle>
            </TextWrapper>
            </Column1>
            <Column2>
            <ImgWrap>
              <Img src={img} alt={alt} />
            </ImgWrap>
            </Column2>
          </InfoRow>
        </InfoWrapper>
      </InfoContainer>
    </>
  )
}

export default Info
