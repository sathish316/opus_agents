import type { MajorScale } from '../data/majorScales'

type Props = {
  scales: MajorScale[]
  value: string
  onChange: (id: string) => void
}

export function ScaleSelector({ scales, value, onChange }: Props) {
  return (
    <label className="scale-selector">
      <span className="scale-selector__label">Major scale</span>
      <select
        className="scale-selector__select"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        aria-label="Select major scale"
      >
        {scales.map((scale) => (
          <option key={scale.id} value={scale.id}>
            {scale.name}
          </option>
        ))}
      </select>
    </label>
  )
}
