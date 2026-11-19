import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,useVideoConfig,interpolate} from 'remotion';
import {paper} from './FilmStyle';
export const EncounterScene:React.FC=()=>{
 const f=useCurrentFrame();const {fps}=useVideoConfig();
 return <AbsoluteFill style={{background:paper}}>
 <div style={{position:'absolute',left:0,right:0,top:220,height:1120,overflow:'hidden'}}>
 <Img src={staticFile('CG_bridge_hello__0.webp')} style={{height:'100%',width:'100%',objectFit:'cover',objectPosition:'70% center',scale:String(interpolate(f,[0,5*fps],[1,1.025],{extrapolateRight:'clamp'}))}}/>
 </div>
 <div style={{position:'absolute',inset:0,background:'linear-gradient(180deg,#f4f0e7 3%,transparent 20%,transparent 56%,#f4f0e7 75%)'}}/>
 <div data-safe-text style={{position:'absolute',top:125,left:90,fontSize:34,letterSpacing:6}}>声から、始まる物語。</div>
 <div data-safe-text style={{position:'absolute',bottom:250,left:90,right:90,fontSize:61,lineHeight:1.9}}>わたしは、まだ、<br/>あなたの顔を知らない。</div>
 </AbsoluteFill>;
};
