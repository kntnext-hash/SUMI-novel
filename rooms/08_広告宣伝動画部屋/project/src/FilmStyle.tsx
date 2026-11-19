import React from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';
export const paper='#f4f0e7';
export const ink='#242a2b';
export const Font:React.FC=()=>{
 const [handle]=React.useState(()=>delayRender('Japanese film font'));
 React.useEffect(()=>{const font=new FontFace('Spring',`url(${staticFile('NotoSerifJP-Regular.otf')})`);font.load().then(f=>{document.fonts.add(f);continueRender(handle);});},[handle]);
 return null;
};
export const base:React.CSSProperties={background:paper,color:ink,fontFamily:'Spring, serif'};
