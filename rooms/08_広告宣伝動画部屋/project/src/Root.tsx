import { Composition } from 'remotion';
import { PortraitFilm,LandscapeFilm } from './Films';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Portrait15" component={PortraitFilm} width={1080} height={1920} fps={30} durationInFrames={450}/>
      <Composition id="Landscape30" component={LandscapeFilm} width={1920} height={1080} fps={30} durationInFrames={900}/>
    </>
  );
};
