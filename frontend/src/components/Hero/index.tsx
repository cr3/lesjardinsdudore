import React, { useState, useEffect } from 'react';
import { useTranslation } from "react-i18next";
import Photo1 from '../../photos/photo1.png';
import Photo2 from '../../photos/photo2.png';
import Photo3 from '../../photos/photo3.png';
import {
  HeroContainer,
  HeroBg,
  HeroContent,
  HeroH1,
  HeroP,
  HeroBtnWrapper,
  PhotoBg,
} from './style';
import { Button } from '../Button/style';

const Hero: React.FC = () => {
  const { t } = useTranslation();
  const [photoSrc, setPhotoSrc] = useState(Photo1);

  useEffect(() => {
    const photos = [Photo1, Photo2, Photo3];

    const intervalId = setInterval(() => {
      const currentIndex = photos.indexOf(photoSrc);
      const newIndex = (currentIndex + 1) % photos.length;
      setPhotoSrc(photos[newIndex]);
    }, 5000)
    
    return () => clearInterval(intervalId);
  }, [photoSrc]);

  return (
    <HeroContainer id="home">
      <HeroBg>
        <PhotoBg
          id="heroPhoto"
          src={photoSrc}
        />
      </HeroBg>
      <HeroContent>
        <HeroP>{t("intro")}</HeroP>
        <HeroH1>{t("title")}</HeroH1>
        <HeroBtnWrapper>
          <Button
            to="contribute"
            smooth={true}
            duration={500}
            spy={true}
            offset={-80}
          >
            {t("contribute")}
          </Button>
        </HeroBtnWrapper>
      </HeroContent>
    </HeroContainer>
  );
};

export default Hero;
