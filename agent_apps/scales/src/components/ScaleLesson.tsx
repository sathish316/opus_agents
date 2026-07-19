import type { MajorScale } from '../data/majorScales'

type Props = {
  scale: MajorScale
}

export function ScaleLesson({ scale }: Props) {
  return (
    <div className="lesson">
      <section className="lesson__explain">
        <h2>How it works</h2>
        <p>{scale.explanation}</p>
        <ul className="lesson__facts">
          <li>
            <span>Notes</span>
            <strong>{scale.notes.join(' · ')}</strong>
          </li>
          <li>
            <span>Relative minor</span>
            <strong>{scale.relativeMinor}</strong>
          </li>
          <li>
            <span>Root fret (low E)</span>
            <strong>{scale.rootFret === 0 ? 'Open' : `Fret ${scale.rootFret}`}</strong>
          </li>
        </ul>
      </section>

      <section className="lesson__fingers">
        <h2>Finger order</h2>
        <p>{scale.fingerOrder}</p>
        <div className="lesson__finger-map" aria-hidden="true">
          {[1, 3, 4, 1, 3, 4, 2, 3].map((finger, index) => (
            <span key={`${finger}-${index}`} className="lesson__finger">
              {finger}
            </span>
          ))}
        </div>
        <p className="lesson__tip">{scale.tip}</p>
      </section>

      <section className="lesson__video">
        <h2>Watch</h2>
        <p>{scale.youtubeTitle}</p>
        <div className="lesson__embed">
          <iframe
            title={scale.youtubeTitle}
            src={`https://www.youtube-nocookie.com/embed/${scale.youtubeId}`}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            loading="lazy"
          />
        </div>
      </section>
    </div>
  )
}
