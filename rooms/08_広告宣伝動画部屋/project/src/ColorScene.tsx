import React from 'react';
import {AbsoluteFill,Img,interpolate,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {paper} from './FilmStyle';
export const ColorScene:React.FC<{portrait?:boolean,reveal?:boolean}>=({portrait=false,reveal=true})=>{
 const frame=useCurrentFrame();const {fps}=useVideoConfig();
 const amount=reveal?interpolate(frame,[1.25*fps,2.6*fps],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}):1;
 const imageStyle:React.CSSProperties={width:'100%',height:'100%',objectFit:'cover',objectPosition:'52% 50%',position:'absolute',scale:String(interpolate(frame,[0,8*fps],[1.015,1.055],{extrapolateRight:'clamp'}))};
 return <AbsoluteFill style={{overflow:'hidden',background:paper}}>
  <div style={{position:'absolute',inset:portrait?'0 0 470px 0':'0'}}>
   <Img src={staticFile('BG_bridge_spring__0.webp')} style={imageStyle}/>
   <Img src={staticFile('BG_bridge_spring__FULL.webp')} style={{...imageStyle,opacity:amount}}/>
  </div>
  <AbsoluteFill style={{background:portrait?'linear-gradient(180deg,rgba(244,240,231,.15) 35%,rgba(244,240,231,.3) 59%,#f4f0e7 76%)':'linear-gradient(180deg,transparent 20%,rgba(244,240,231,.78) 63%,rgba(244,240,231,.96) 100%)'}}/>
  {reveal?<>
   <div style={{position:'absolute',top:portrait?120:80,left:portrait?90:120,fontSize:portrait?34:30,letterSpacing:6}}>{amount<.5?'初周の風景':'色づく風景'}</div>
   <div data-safe-text style={{position:'absolute',left:portrait?90:140,right:portrait?90:140,bottom:portrait?230:120,fontSize:portrait?84:94,lineHeight:1.65,letterSpacing:portrait?1:5}}>{portrait?<>あの日、<br/>きみはどんな<br/>顔をしていた？</>:<>あの日、<br/>きみはどんな顔をしていた？</>}</div>
  </>:<div data-safe-text style={{position:'absolute',left:90,right:90,bottom:280,fontSize:58,lineHeight:1.8}}>きみの色が<br/>見えるまで。</div>}
 </AbsoluteFill>;
};
