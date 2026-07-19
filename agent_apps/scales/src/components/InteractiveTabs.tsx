import type { GuitarNote } from '../data/majorScales'
import { stringName } from '../data/majorScales'

type Props = {
  notes: GuitarNote[]
  activeIndex: number
}

const STRING_ORDER: GuitarNote['string'][] = [1, 2, 3, 4, 5, 6]

export function InteractiveTabs({ notes, activeIndex }: Props) {
  const maxFret = Math.max(5, ...notes.map((n) => n.fret))

  return (
    <div className="tabs">
      <div className="tabs__header">
        <h2>Interactive tabs</h2>
        <p>One note per beat. The lit fret follows the metronome.</p>
      </div>

      <div className="tabs__board" role="img" aria-label="Guitar tablature fretboard">
        {STRING_ORDER.map((stringNumber) => (
          <div className="tabs__string-row" key={stringNumber}>
            <span className="tabs__string-name">{stringName(stringNumber)}</span>
            <div className="tabs__frets">
              {Array.from({ length: maxFret + 1 }, (_, fret) => {
                const noteIndex = notes.findIndex((n) => n.string === stringNumber && n.fret === fret)
                const note = noteIndex >= 0 ? notes[noteIndex] : null
                const isActive = noteIndex === activeIndex
                return (
                  <div
                    key={fret}
                    className={`tabs__fret ${note ? 'has-note' : ''} ${isActive ? 'is-active' : ''}`}
                    data-fret={fret}
                  >
                    {note ? (
                      <span className="tabs__note" title={`${note.label} · finger ${note.finger}`}>
                        <strong>{note.fret}</strong>
                        <em>{note.label}</em>
                      </span>
                    ) : (
                      <span className="tabs__empty" />
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      <ol className="tabs__sequence">
        {notes.map((note, index) => (
          <li key={`${note.string}-${note.fret}-${index}`} className={index === activeIndex ? 'is-active' : ''}>
            <span className="tabs__seq-fret">{note.fret}</span>
            <span className="tabs__seq-meta">
              {stringName(note.string)} · {note.label} · finger {note.finger === 0 ? 'open' : note.finger}
            </span>
          </li>
        ))}
      </ol>
    </div>
  )
}
