export type GuitarNote = {
  /** 1 = high e, 6 = low E */
  string: 1 | 2 | 3 | 4 | 5 | 6
  fret: number
  /** 0 = open, 1–4 = fretting fingers */
  finger: 0 | 1 | 2 | 3 | 4
  label: string
}

export type MajorScale = {
  id: string
  name: string
  root: string
  /** Root fret on the low E string for the E-shape pattern */
  rootFret: number
  notes: string[]
  relativeMinor: string
  explanation: string
  youtubeId: string
  youtubeTitle: string
  fingerOrder: string
  tip: string
}

const STRING_NAMES = ['e', 'B', 'G', 'D', 'A', 'E'] as const

/** Absolute frets for the one-octave E-shape major pattern (offsets from root). */
const PATTERN: Array<{ string: GuitarNote['string']; fretOffset: number; finger: GuitarNote['finger'] }> = [
  { string: 6, fretOffset: 0, finger: 1 },
  { string: 6, fretOffset: 2, finger: 3 },
  { string: 6, fretOffset: 4, finger: 4 },
  { string: 5, fretOffset: 0, finger: 1 },
  { string: 5, fretOffset: 2, finger: 3 },
  { string: 5, fretOffset: 4, finger: 4 },
  { string: 4, fretOffset: 1, finger: 2 },
  { string: 4, fretOffset: 2, finger: 3 },
]

const NOTE_CYCLE = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'] as const

function scaleNotes(root: string): string[] {
  const start = NOTE_CYCLE.indexOf(root as (typeof NOTE_CYCLE)[number])
  if (start < 0) throw new Error(`Unknown root ${root}`)
  const intervals = [0, 2, 4, 5, 7, 9, 11, 12]
  return intervals.map((i) => NOTE_CYCLE[(start + i) % 12]!)
}

export function buildTab(scale: MajorScale): GuitarNote[] {
  return PATTERN.map((step, index) => {
    const fret = scale.rootFret + step.fretOffset
    return {
      string: step.string,
      fret,
      finger: fret === 0 ? 0 : step.finger,
      label: scale.notes[index] ?? scaleNotes(scale.root)[index]!,
    }
  })
}

export function stringName(stringNumber: GuitarNote['string']): string {
  return STRING_NAMES[stringNumber - 1]!
}

export const MAJOR_SCALES: MajorScale[] = [
  {
    id: 'c-major',
    name: 'C Major',
    root: 'C',
    rootFret: 8,
    notes: ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'],
    relativeMinor: 'A minor',
    explanation:
      'C major is the reference major scale—no sharps or flats. On guitar, play it as an E-shape pattern with the root on the 8th fret of the low E string. Hear how the bright, open quality comes from the major 3rd (E) and major 7th (B).',
    youtubeId: 'BmDiDy_Dzn8',
    youtubeTitle: 'The Essential Guide to Mastering the Major Scale on Guitar',
    fingerOrder: '1 → 3 → 4 on string 6, then 1 → 3 → 4 on string 5, then 2 → 3 on string 4',
    tip: 'Keep your thumb behind the neck and leave each finger hovering over its fret when possible.',
  },
  {
    id: 'g-major',
    name: 'G Major',
    root: 'G',
    rootFret: 3,
    notes: ['G', 'A', 'B', 'C', 'D', 'E', 'F#', 'G'],
    relativeMinor: 'E minor',
    explanation:
      'G major has one sharp (F#). Root sits on the 3rd fret of the low E string. This key is everywhere in rock and folk—get comfortable shifting the same E-shape pattern you used for C.',
    youtubeId: 'dCg2Ir5GEmo',
    youtubeTitle: 'Major Scales | Music Theory for Guitar I',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 (same movable pattern, root at fret 3)',
    tip: 'Watch the F# on the D string—finger 2 covers the 4th fret (relative +1 from the root fret).',
  },
  {
    id: 'd-major',
    name: 'D Major',
    root: 'D',
    rootFret: 10,
    notes: ['D', 'E', 'F#', 'G', 'A', 'B', 'C#', 'D'],
    relativeMinor: 'B minor',
    explanation:
      'D major has two sharps (F#, C#). Root on fret 10 of the low E. The pattern is identical—only the starting fret changes—so use this key to lock in muscle memory up the neck.',
    youtubeId: 'i4zGDoRvn5o',
    youtubeTitle: 'Scale for Beginners. Start Here.',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 10',
    tip: 'If fret 10 feels cramped, practice slowly at 60 BPM before speeding up.',
  },
  {
    id: 'a-major',
    name: 'A Major',
    root: 'A',
    rootFret: 5,
    notes: ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#', 'A'],
    relativeMinor: 'F# minor',
    explanation:
      'A major has three sharps. Root on the 5th fret—one of the most comfortable positions on the neck. Great key for connecting scale practice to open A chords and bluesy licks later.',
    youtubeId: 'BmDiDy_Dzn8',
    youtubeTitle: 'The Essential Guide to Mastering the Major Scale on Guitar',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 5',
    tip: 'Say the note names out loud as you play—A B C# D E F# G# A.',
  },
  {
    id: 'e-major',
    name: 'E Major',
    root: 'E',
    rootFret: 0,
    notes: ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#', 'E'],
    relativeMinor: 'C# minor',
    explanation:
      'E major has four sharps. With the root on the open low E, this is the open-position version of the same pattern. Open strings ring freely—ideal for hearing each degree of the scale clearly.',
    youtubeId: 'dCg2Ir5GEmo',
    youtubeTitle: 'Major Scales | Music Theory for Guitar I',
    fingerOrder: 'Open E (0) → 2 → 4 on string 6, then open A → 2 → 4, then 1 → 2 on string 4',
    tip: 'Treat open notes as finger 0—lift cleanly so fretted notes do not buzz against open strings.',
  },
  {
    id: 'b-major',
    name: 'B Major',
    root: 'B',
    rootFret: 7,
    notes: ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#', 'B'],
    relativeMinor: 'G# minor',
    explanation:
      'B major has five sharps. Root on fret 7. Same shape—use it to practice accuracy in the middle of the neck where frets are tighter than open position.',
    youtubeId: 'i4zGDoRvn5o',
    youtubeTitle: 'Scale for Beginners. Start Here.',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 7',
    tip: 'Keep fretting-hand knuckles arched; collapsed fingers mute neighboring strings.',
  },
  {
    id: 'f-sharp-major',
    name: 'F# Major',
    root: 'F#',
    rootFret: 2,
    notes: ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#', 'F#'],
    relativeMinor: 'D# minor',
    explanation:
      'F# major has six sharps (enharmonic with Gb). Root on fret 2. Excellent for training your ear on a bright, tightly voiced major sound high in sharps.',
    youtubeId: 'BmDiDy_Dzn8',
    youtubeTitle: 'The Essential Guide to Mastering the Major Scale on Guitar',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 2',
    tip: 'Alternate picking: down-up-down-up through the whole octave with the metronome.',
  },
  {
    id: 'f-major',
    name: 'F Major',
    root: 'F',
    rootFret: 1,
    notes: ['F', 'G', 'A', 'Bb', 'C', 'D', 'E', 'F'],
    relativeMinor: 'D minor',
    explanation:
      'F major has one flat (Bb). Root on fret 1—close to the nut, so leave extra clearance for clean fretting. This key connects well to barre-chord shapes based on F.',
    youtubeId: 'dCg2Ir5GEmo',
    youtubeTitle: 'Major Scales | Music Theory for Guitar I',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 1',
    tip: 'Press just behind the fret wire for the clearest tone with the least effort.',
  },
  {
    id: 'b-flat-major',
    name: 'Bb Major',
    root: 'Bb',
    rootFret: 6,
    notes: ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A', 'Bb'],
    relativeMinor: 'G minor',
    explanation:
      'Bb major has two flats. Root on fret 6. Common in jazz and horn-friendly keys—practice it to feel at home outside of open-string guitar keys.',
    youtubeId: 'i4zGDoRvn5o',
    youtubeTitle: 'Scale for Beginners. Start Here.',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 6',
    tip: 'Practice ascending, then descending, without stopping the metronome.',
  },
  {
    id: 'e-flat-major',
    name: 'Eb Major',
    root: 'Eb',
    rootFret: 11,
    notes: ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D', 'Eb'],
    relativeMinor: 'C minor',
    explanation:
      'Eb major has three flats. Root on fret 11. Use a lighter touch up here—frets are closer, and small motions keep the scale even.',
    youtubeId: 'BmDiDy_Dzn8',
    youtubeTitle: 'The Essential Guide to Mastering the Major Scale on Guitar',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 11',
    tip: 'If the stretch to +4 on string 6 is hard, roll your wrist slightly forward—not your shoulder.',
  },
  {
    id: 'a-flat-major',
    name: 'Ab Major',
    root: 'Ab',
    rootFret: 4,
    notes: ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G', 'Ab'],
    relativeMinor: 'F minor',
    explanation:
      'Ab major has four flats. Root on fret 4. Same movable major shape—focus on even timing between the string changes (6→5 and 5→4).',
    youtubeId: 'dCg2Ir5GEmo',
    youtubeTitle: 'Major Scales | Music Theory for Guitar I',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 4',
    tip: 'Mute unused strings lightly with spare fingers or the picking-hand palm.',
  },
  {
    id: 'd-flat-major',
    name: 'Db Major',
    root: 'Db',
    rootFret: 9,
    notes: ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C', 'Db'],
    relativeMinor: 'Bb minor',
    explanation:
      'Db major has five flats (enharmonic with C#). Root on fret 9. Finish the circle of keys here—once all twelve roots feel familiar, you can move the pattern anywhere.',
    youtubeId: 'i4zGDoRvn5o',
    youtubeTitle: 'Scale for Beginners. Start Here.',
    fingerOrder: '1 → 3 → 4 · 1 → 3 → 4 · 2 → 3 starting at fret 9',
    tip: 'Loop the octave with the synced tab until you can play it without looking at the screen.',
  },
]

export function getScaleById(id: string): MajorScale {
  return MAJOR_SCALES.find((scale) => scale.id === id) ?? MAJOR_SCALES[0]!
}
