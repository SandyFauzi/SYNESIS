import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import type {Segment} from './types';

const LABELS: Record<string, string> = {
  graph: 'GRAF KOMPUTASI', finite: 'CEK TURUNAN', gpu: 'PYTORCH / GPU',
  training: 'PROSES BELAJAR', network: 'JARINGAN NEURON', dead: 'NEURON MATI',
  decision: 'BATAS KEPUTUSAN', relu: 'AKTIVASI RELU', softmax: 'PROBABILITAS',
  wall: 'TEMBOK REKURSI', stack: 'BACKWARD ITERATIF', matrix: 'OPERASI MATRIKS',
  mnist: 'PIXEL → ANGKA', optimizer: 'LANGKAH OPTIMIZER',
};

const MiniSignal: React.FC<{segment: Segment}> = ({segment}) => {
  const frame = useCurrentFrame();
  const local = frame - segment.start;
  const t = Math.max(0, Math.min(1, local / Math.max(1, segment.duration - 1)));
  const pulseX = interpolate(t, [0, 1], [28, 252]);
  const phase = (segment.line * 17) % 100;

  if (['training', 'optimizer', 'finite'].includes(segment.visual)) {
    const points = Array.from({length: 8}, (_, i) => {
      const x = 20 + i * 34;
      const progress = i / 7;
      const y = segment.visual === 'optimizer'
        ? 72 - 54 * (1 - Math.pow(progress - 1, 2))
        : 68 - progress * 47 + Math.sin(i + phase) * 4;
      return `${x},${y}`;
    }).join(' ');
    return <svg width="280" height="92" viewBox="0 0 280 92">
      <line x1="14" y1="76" x2="268" y2="76" stroke="#46505D" strokeWidth="1" />
      <polyline points={points} fill="none" stroke="#37E68A" strokeWidth="3" strokeLinejoin="round" />
      <circle cx={pulseX} cy={Math.max(18, 70 - t * 48)} r="5" fill="#69B7FF" />
    </svg>;
  }

  if (['network', 'relu', 'dead', 'decision'].includes(segment.visual)) {
    const xs = [30, 102, 178, 250];
    return <svg width="280" height="92" viewBox="0 0 280 92">
      {xs.slice(0, -1).flatMap((x, col) => [22, 46, 70].map((y, row) => (
        <line key={`${col}-${row}`} x1={x + 7} y1={y} x2={xs[col + 1] - 7} y2={46 + (row - 1) * 15} stroke="#34404C" strokeWidth="1" />
      )))}
      {xs.flatMap((x, col) => [22, 46, 70].map((y, row) => (
        <circle key={`${col}-${row}`} cx={x} cy={y} r="6" fill={segment.visual === 'dead' && row === 0 ? '#29303A' : col === 3 ? '#37E68A' : '#69B7FF'} opacity={0.55 + 0.4 * Math.sin((local + row * 6) / 8) ** 2} />
      )))}
    </svg>;
  }

  if (['matrix', 'mnist'].includes(segment.visual)) {
    return <svg width="280" height="92" viewBox="0 0 280 92">
      {Array.from({length: 32}, (_, i) => {
        const col = i % 8; const row = Math.floor(i / 8);
        const on = ((i * 11 + segment.line) % 9) < 4;
        return <rect key={i} x={16 + col * 22} y={7 + row * 20} width="16" height="14" rx="2" fill={on ? '#69B7FF' : '#27303A'} />;
      })}
      <text x="205" y="54" fill="#37E68A" fontFamily="Consolas" fontSize="25">{segment.visual === 'mnist' ? segment.line % 10 : '@'}</text>
      <path d="M184 43 L198 43" stroke="#7C8797" strokeWidth="2" />
      <circle cx="258" cy="46" r={8 + 3 * Math.sin(local / 5)} fill="#37E68A" opacity=".75" />
    </svg>;
  }

  if (['softmax', 'wall', 'stack'].includes(segment.visual)) {
    return <svg width="280" height="92" viewBox="0 0 280 92">
      {Array.from({length: 6}, (_, i) => {
        const width = 28 + ((i * 31 + segment.line * 7) % 135);
        return <rect key={i} x="18" y={8 + i * 13} width={width} height="8" rx="4" fill={i === segment.line % 6 ? '#37E68A' : '#637184'} opacity=".85" />;
      })}
      {segment.visual === 'wall' && <line x1="205" y1="5" x2="205" y2="86" stroke="#FF6259" strokeDasharray="5 4" strokeWidth="3" />}
      {segment.visual === 'stack' && Array.from({length: 4}, (_, i) => <rect key={i} x={214} y={64 - i * 17} width="44" height="13" rx="3" fill="#37E68A" opacity={0.25 + i * 0.18} />)}
    </svg>;
  }

  return <svg width="280" height="92" viewBox="0 0 280 92">
    <line x1="26" y1="46" x2="254" y2="46" stroke="#35404C" strokeWidth="3" />
    {[26, 82, 138, 194, 250].map((x, i) => <circle key={x} cx={x} cy={46 + (i % 2 ? -18 : 18)} r="8" fill={i <= Math.floor(t * 5) ? '#37E68A' : '#69B7FF'} />)}
    <circle cx={pulseX} cy="46" r="5" fill="#E7C36A" />
  </svg>;
};

export const VisualStage: React.FC<{segment: Segment}> = ({segment}) => (
  <div style={{position: 'absolute', inset: '0 0 auto 0', height: 674, pointerEvents: 'none'}}>
    <div style={{position: 'absolute', top: 83, right: 24, display: 'flex', alignItems: 'center', gap: 8, padding: '7px 10px', borderRadius: 7, background: 'rgba(7,10,14,.76)', border: '1px solid rgba(55,230,138,.35)'}}>
      <span style={{width: 7, height: 7, borderRadius: 7, background: '#37E68A', boxShadow: '0 0 10px #37E68A'}} />
      <span style={{fontFamily: 'Consolas, monospace', fontSize: 12, color: '#B9C3CF'}}>{LABELS[segment.visual] ?? 'ALIRAN PROGRAM'}</span>
    </div>
    <div style={{position: 'absolute', left: 24, bottom: 90, width: 306, height: 118, padding: '10px 12px', borderRadius: 13, background: 'rgba(9,12,17,.82)', border: '1px solid rgba(105,183,255,.25)', boxShadow: '0 10px 30px rgba(0,0,0,.35)'}}>
      <MiniSignal segment={segment} />
    </div>
    <div style={{position: 'absolute', left: 24, right: 24, bottom: 20, minHeight: 55, borderRadius: 12, background: 'rgba(9,12,17,.88)', border: '1px solid #27303A', padding: '11px 15px', display: 'flex', alignItems: 'center', gap: 12}}>
      <span style={{fontFamily: 'Consolas, monospace', fontSize: 13, color: '#37E68A', flex: '0 0 auto'}}>Baris {segment.line}</span>
      <span style={{width: 1, height: 28, background: '#34404C'}} />
      <span style={{fontFamily: 'Arial, sans-serif', fontSize: 17, lineHeight: 1.25, color: '#ECF1F6'}}>{segment.caption}</span>
    </div>
  </div>
);
