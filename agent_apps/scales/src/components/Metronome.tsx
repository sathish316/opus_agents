type Props = {
  bpm: number
  onBpmChange: (bpm: number) => void
  isPlaying: boolean
  onToggle: () => void
  beatIndex: number
}

export function Metronome({ bpm, onBpmChange, isPlaying, onToggle, beatIndex }: Props) {
  return (
    <div className="metronome">
      <div className="metronome__header">
        <h2>Metronome</h2>
        <p>BPM drives the click and the tab highlight together.</p>
      </div>

      <div className="metronome__controls">
        <button
          type="button"
          className={`metronome__play ${isPlaying ? 'is-playing' : ''}`}
          onClick={onToggle}
          aria-pressed={isPlaying}
        >
          {isPlaying ? 'Stop' : 'Start'}
        </button>

        <label className="metronome__bpm">
          <span>BPM</span>
          <input
            type="range"
            min={40}
            max={200}
            step={1}
            value={bpm}
            onChange={(event) => onBpmChange(Number(event.target.value))}
          />
          <input
            type="number"
            min={40}
            max={200}
            value={bpm}
            onChange={(event) => {
              const next = Number(event.target.value)
              if (!Number.isNaN(next)) onBpmChange(Math.min(200, Math.max(40, next)))
            }}
            aria-label="Beats per minute"
          />
        </label>
      </div>

      <div className="metronome__pulse" aria-hidden="true">
        {[0, 1, 2, 3].map((i) => (
          <span
            key={i}
            className={`metronome__dot ${beatIndex % 4 === i && beatIndex >= 0 ? 'is-active' : ''}`}
          />
        ))}
      </div>
    </div>
  )
}
