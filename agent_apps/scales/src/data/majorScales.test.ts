import { describe, expect, it } from 'vitest'
import { MAJOR_SCALES, buildTab } from './majorScales'

describe('major scale data', () => {
  it('includes all twelve major keys', () => {
    expect(MAJOR_SCALES).toHaveLength(12)
  })

  it('builds an eight-note tab for each scale', () => {
    for (const scale of MAJOR_SCALES) {
      const tab = buildTab(scale)
      expect(tab).toHaveLength(8)
      expect(tab[0]?.label).toBe(scale.root)
      expect(tab[7]?.label).toBe(scale.notes[7])
      expect(tab.every((note) => note.fret >= 0)).toBe(true)
    }
  })

  it('marks open strings as finger 0 for E major', () => {
    const eMajor = MAJOR_SCALES.find((s) => s.id === 'e-major')!
    const tab = buildTab(eMajor)
    expect(tab[0]).toMatchObject({ fret: 0, finger: 0, label: 'E' })
    expect(tab[3]).toMatchObject({ fret: 0, finger: 0, label: 'A' })
  })
})
