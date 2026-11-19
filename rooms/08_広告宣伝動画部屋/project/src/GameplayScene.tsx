import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';
export const GameplayScene:React.FC<{shot:string}>=({shot})=><AbsoluteFill>
 <Img src={staticFile(shot)} style={{width:'100%',height:'100%',objectFit:'contain'}}/>
 <div style={{position:'absolute',top:38,right:60,padding:'10px 20px',background:'rgba(244,240,231,.86)',fontSize:24,letterSpacing:3}}>ゲーム本編の画面</div>
</AbsoluteFill>;
