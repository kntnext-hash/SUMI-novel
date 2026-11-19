import React from 'react';
import {AbsoluteFill,Img,staticFile,interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
import {paper} from './FilmStyle';
export const TitleScene:React.FC<{portrait?:boolean}>=({portrait=false})=>{
 const f=useCurrentFrame();const {fps}=useVideoConfig();
 return <AbsoluteFill style={{background:paper,alignItems:'center',justifyContent:'center'}}>
 <Img src={staticFile('BG_bridge_spring__FULL.webp')} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',opacity:.12}}/>
 <div style={{position:'absolute',inset:portrait?'110px 65px':'70px 100px',border:'1px solid rgba(40,45,45,.24)'}}/>
 <div style={{textAlign:'center',opacity:interpolate(f,[0,.45*fps],[0,1],{extrapolateRight:'clamp'})}}>
 <div data-safe-text style={{fontSize:portrait?32:34,letterSpacing:8,marginBottom:portrait?64:40}}>文学的幻想百合ビジュアルノベル</div>
 <div data-safe-text style={{fontSize:portrait?146:182,letterSpacing:portrait?8:22,lineHeight:1.6}}>顔のない春</div>
 <div data-safe-text style={{fontSize:portrait?40:46,letterSpacing:5,marginTop:portrait?42:28}}>きみの色が見えるまで。</div>
 </div>
 </AbsoluteFill>;
};
