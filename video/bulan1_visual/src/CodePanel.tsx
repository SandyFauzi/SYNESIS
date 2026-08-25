import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import type {Segment} from './types';

const KEYWORDS = new Set([
  'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
  'else', 'except', 'False', 'finally', 'for', 'from', 'if', 'import', 'in',
  'is', 'lambda', 'None', 'not', 'or', 'pass', 'raise', 'return', 'True',
  'try', 'while', 'with', 'yield', 'self',
]);

const tokenColor = (token: string): string => {
  if (token.startsWith('#')) return '#7C8797';
  if (/^(['"]).*\1$/.test(token)) return '#E7C36A';
  if (/^\d/.test(token)) return '#A890FF';
  if (KEYWORDS.has(token)) return '#69B7FF';
  if (/^[A-Z][A-Za-z_]*$/.test(token)) return '#7BE0C3';
  return '#D9E0E8';
};

const HighlightedLine: React.FC<{text: string}> = ({text}) => {
  const commentAt = text.indexOf('#');
  const before = commentAt >= 0 ? text.slice(0, commentAt) : text;
  const comment = commentAt >= 0 ? text.slice(commentAt) : '';
  const tokens = before.split(/((?:"[^"\n]*"|'[^'\n]*')|\b\d+(?:\.\d+)?\b|\b[A-Za-z_]\w*\b)/g);
  return (
    <>
      {tokens.map((token, index) => (
        <span key={`${index}-${token}`} style={{color: tokenColor(token)}}>{token}</span>
      ))}
      {comment && <span style={{color: tokenColor(comment)}}>{comment}</span>}
    </>
  );
};

export const CodePanel: React.FC<{segment: Segment; chapterProgress: number}> = ({segment, chapterProgress}) => {
  const frame = useCurrentFrame();
  const fontSize = 13.2;
  const travel = (text: string): number => Math.max(0, text.length * fontSize * 0.61 - 560);
  const scroll = (text: string): number => {
    if (travel(text) === 0) return 0;
    const local = frame - segment.start;
    const amount = interpolate(local, [0, segment.duration * 0.2, segment.duration * 0.82, segment.duration], [0, 0, 1, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return -travel(text) * amount;
  };

  return (
    <div style={{
      position: 'absolute', left: 22, right: 22, top: 674, bottom: 30,
      background: '#0E1218', border: '1px solid #252D38', borderRadius: 17,
      boxShadow: '0 18px 48px rgba(0,0,0,.45)', overflow: 'hidden',
      fontFamily: 'Consolas, Menlo, monospace',
    }}>
      <div style={{height: 53, display: 'flex', alignItems: 'center', padding: '0 18px', borderBottom: '1px solid #232A34'}}>
        <div style={{display: 'flex', gap: 7, marginRight: 15}}>
          {['#FF6259', '#FFBD2E', '#28C840'].map((color) => (
            <span key={color} style={{width: 10, height: 10, borderRadius: 10, background: color}} />
          ))}
        </div>
        <div style={{fontSize: 14, color: '#AEB7C4', flex: 1}}>{segment.file}</div>
        <div style={{fontSize: 13, color: '#37E68A'}}>Ln {segment.line}/{segment.totalLines}</div>
      </div>

      <div style={{padding: '13px 0 10px'}}>
        {segment.window.map(({no, text}) => {
          const active = no === segment.line;
          return (
            <div key={no} style={{
              height: 43, display: 'flex', alignItems: 'center', position: 'relative',
              background: active ? 'linear-gradient(90deg, rgba(55,230,138,.20), rgba(55,230,138,.045))' : 'transparent',
              borderLeft: active ? '4px solid #37E68A' : '4px solid transparent',
            }}>
              <span style={{width: 48, paddingRight: 12, textAlign: 'right', color: active ? '#37E68A' : '#505966', fontSize: 12}}>{no}</span>
              <span style={{flex: 1, overflow: 'hidden', paddingRight: 28}}>
                <code style={{display: 'inline-block', fontSize, lineHeight: 1, whiteSpace: 'pre', letterSpacing: '-0.15px', transform: active ? `translateX(${scroll(text)}px)` : undefined}}>
                  <HighlightedLine text={text || ' '} />
                </code>
              </span>
              {active && <span style={{position: 'absolute', right: 12, width: 7, height: 7, borderRadius: 7, background: '#37E68A', boxShadow: '0 0 12px #37E68A'}} />}
            </div>
          );
        })}
      </div>

      <div style={{position: 'absolute', left: 18, right: 18, bottom: 17}}>
        <div style={{display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8}}>
          <span style={{fontSize: 11, color: '#37E68A', border: '1px solid rgba(55,230,138,.45)', borderRadius: 5, padding: '3px 6px'}}>PROSES</span>
          <span style={{fontFamily: 'Arial, sans-serif', fontSize: 15, color: '#CDD4DD', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{segment.caption}</span>
        </div>
        <div style={{height: 4, borderRadius: 4, background: '#232A34', overflow: 'hidden'}}>
          <div style={{height: '100%', width: `${chapterProgress * 100}%`, background: 'linear-gradient(90deg,#37E68A,#69B7FF)'}} />
        </div>
      </div>
    </div>
  );
};
