import React from 'react';
import {AbsoluteFill,Sequence,staticFile,useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {Font,base} from './FilmStyle';
import {ColorScene} from './ColorScene';
import {EncounterScene} from './EncounterScene';
import {GameplayScene} from './GameplayScene';
import {TitleScene} from './TitleScene';
export const PortraitFilm:React.FC=()=>{
 const {fps}=useVideoConfig();
 return <AbsoluteFill style={base}><Font/>
 <Audio src={staticFile('mix15.wav')}/>
 <Sequence name="同構図が色づくフック・広告コピー" from={0} durationInFrames={5*fps} premountFor={fps}><ColorScene portrait/></Sequence>
 <Sequence name="初周白筆・顔を知らない出会い" from={5*fps} durationInFrames={5*fps} premountFor={fps}><EncounterScene/></Sequence>
 <Sequence name="色彩の風景" from={10*fps} durationInFrames={2*fps} premountFor={fps}><ColorScene portrait reveal={false}/></Sequence>
 <Sequence name="作品名" from={12*fps} durationInFrames={3*fps} premountFor={fps}><TitleScene portrait/></Sequence>
 </AbsoluteFill>;
};
export const LandscapeFilm:React.FC=()=>{
 const {fps}=useVideoConfig();
 return <AbsoluteFill style={base}><Font/>
 <Audio src={staticFile('mix30.wav')}/>
 <Sequence name="序盤・通学路の本文" from={0} durationInFrames={5*fps} premountFor={fps}><GameplayScene shot="adv_bridge.png"/></Sequence>
 <Sequence name="序盤・おはよう" from={5*fps} durationInFrames={5*fps} premountFor={fps}><GameplayScene shot="adv_hello.png"/></Sequence>
 <Sequence name="序盤・鞄にしまうイヤホン" from={10*fps} durationInFrames={6*fps} premountFor={fps}><GameplayScene shot="adv_bag.png"/></Sequence>
 <Sequence name="同構図の無彩と色彩・広告コピー" from={16*fps} durationInFrames={10*fps} premountFor={fps}><ColorScene/></Sequence>
 <Sequence name="作品名" from={26*fps} durationInFrames={4*fps} premountFor={fps}><TitleScene/></Sequence>
 </AbsoluteFill>;
};
