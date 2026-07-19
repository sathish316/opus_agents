import { useMemo, useState } from 'react'
import { ScaleSelector } from './components/ScaleSelector'
import { Metronome } from './components/Metronome'
import { InteractiveTabs } from './components/InteractiveTabs'
import { ScaleLesson } from './components/ScaleLesson'
import { MAJOR_SCALES, buildTab, getScaleById } from './data/majorScales'
import { useMetronome } from './hooks/useMetronome'
import './App.css'

function App() {
  const [scaleId, setScaleId] = useState(MAJOR_SCALES[0]!.id)
  const [bpm, setBpm] = useState(72)
  const scale = useMemo(() => getScaleById(scaleId), [scaleId])
  const tabNotes = useMemo(() => buildTab(scale), [scale])

  const { isPlaying, beatIndex, toggle, stop } = useMetronome({
    bpm,
    beatCount: tabNotes.length,
  })

  const handleScaleChange = (id: string) => {
    stop()
    setScaleId(id)
  }

  return (
    <div className="app">
      <div className="app__atmosphere" aria-hidden="true" />

      <header className="hero">
        <p className="hero__eyebrow">Guitar practice · AgentApp</p>
        <h1 className="hero__brand">Scales</h1>
        <p className="hero__lede">
          Major-scale routines with fingerings, synced tabs, and a practice metronome.
        </p>
        <ScaleSelector scales={MAJOR_SCALES} value={scaleId} onChange={handleScaleChange} />
      </header>

      <main className="practice">
        <div className="practice__stage">
          <div className="practice__scale-name">
            <span>Now practicing</span>
            <strong>{scale.name}</strong>
          </div>
          <InteractiveTabs notes={tabNotes} activeIndex={beatIndex} />
          <Metronome
            bpm={bpm}
            onBpmChange={setBpm}
            isPlaying={isPlaying}
            onToggle={toggle}
            beatIndex={beatIndex}
          />
        </div>

        <ScaleLesson scale={scale} />
      </main>

      <footer className="footer">
        <p>Scales · AgentApps practice suite · One octave E-shape pattern for every major key</p>
      </footer>
    </div>
  )
}

export default App
