import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';

// Brand Constants from the Guide
const COLORS = {
  ELECTRIC_INDIGO: '#4F46E5',
  CYBER_MINT: '#10B981',
  DEEP_SPACE: '#0F172A',
  NEON_PULSE: '#F472B6',
  TEXT: '#F8FAFC',
};

interface RemotionVisionPersonaProps {
  companyName: string;
  metricLabel: string;
  metricValue: string;
  headline: string;
}

export const RemotionVisionPersona: React.FC<RemotionVisionPersonaProps> = ({
  companyName = 'Remotion Vision',
  metricLabel = 'Performance Boost',
  metricValue = '+127%',
  headline = 'Programmatic Video Intelligence',
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Entrance animations
  const entrance = spring({
    frame,
    fps,
    config: { damping: 12 },
  });

  // Dynamic values entrance
  const valueEntrance = spring({
    frame: frame - 15,
    fps,
    config: { stiffness: 100 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });
  const scale = interpolate(entrance, [0, 1], [0.95, 1]);

  return (
    <AbsoluteFill style={{ 
      backgroundColor: COLORS.DEEP_SPACE, 
      color: COLORS.TEXT, 
      fontFamily: 'Inter, sans-serif',
      padding: 60,
      opacity,
      transform: `scale(${scale})`
    }}>
      {/* Background Glow Effect */}
      <div style={{
        position: 'absolute',
        top: -height * 0.2,
        right: -width * 0.2,
        width: width * 0.6,
        height: height * 0.6,
        background: `radial-gradient(circle, ${COLORS.ELECTRIC_INDIGO}33 0%, transparent 70%)`,
        filter: 'blur(100px)',
      }} />

      {/* Header / Brand */}
      <div style={{ fontSize: 24, fontWeight: 600, color: COLORS.ELECTRIC_INDIGO, marginBottom: 20 }}>
        {companyName.toUpperCase()}
      </div>

      {/* Main Headline */}
      <div style={{ 
        fontSize: 80, 
        fontWeight: 800, 
        lineHeight: 1.1, 
        width: '80%',
        marginBottom: 40,
        letterSpacing: '-0.02em'
      }}>
        {headline}
      </div>

      {/* Metric Card (Atomic Component) */}
      <div style={{
        background: 'rgba(30, 41, 59, 0.7)',
        backdropFilter: 'blur(12px)',
        border: `1px solid rgba(255,255,255,0.1)`,
        borderRadius: 24,
        padding: 40,
        display: 'inline-flex',
        flexDirection: 'column',
        gap: 10,
        transform: `translateY(${interpolate(valueEntrance, [0, 1], [20, 0])}px)`,
        opacity: valueEntrance,
      }}>
        <div style={{ color: COLORS.CYBER_MINT, fontWeight: 600, fontSize: 24 }}>
          {metricLabel}
        </div>
        <div style={{ fontSize: 72, fontWeight: 800 }}>
          {metricValue}
        </div>
      </div>

      {/* Dynamic Cursor / Brackets Motif */}
      <div style={{
        position: 'absolute',
        bottom: 60,
        left: 60,
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        color: COLORS.NEON_PULSE,
        fontFamily: 'JetBrains Mono, monospace',
        fontSize: 18,
      }}>
        <span style={{ opacity: Math.sin(frame / 5) * 0.5 + 0.5 }}>●</span>
        <span>programmatic_execution_active</span>
      </div>
    </AbsoluteFill>
  );
};
