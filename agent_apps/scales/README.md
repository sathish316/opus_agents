# Scales

Guitar major-scale practice app (AgentApp). Pick any major key, study the fingering, watch a lesson video, and play along with interactive tabs synced to a metronome.

## Features

- Dropdown selector for all 12 major scales
- Short explanation, note list, and relative minor for each key
- Finger-order guidance for the movable E-shape pattern
- Embedded YouTube lesson per scale
- Interactive fretboard tabs
- Metronome with adjustable BPM (40–200)
- Tab highlight locked to the metronome beat (one note per click)

## Run

```bash
cd agent_apps/scales
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

## Build

```bash
npm run build
npm run preview
```

## Practice pattern

Every key uses the same one-octave **E-shape** major pattern with the root on the low E string. Change the root fret and the shape moves—ideal for building transferable muscle memory across the circle of fifths.
