import { useCallback, useEffect, useRef, useState } from 'react'

type MetronomeOptions = {
  bpm: number
  /** Called on each beat while running; index is 0-based within the loop length */
  onBeat?: (beatIndex: number) => void
  beatCount: number
}

/**
 * Web Audio metronome. Advances a beat callback in sync so tabs can highlight with the click.
 */
export function useMetronome({ bpm, onBeat, beatCount }: MetronomeOptions) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [beatIndex, setBeatIndex] = useState(-1)
  const audioCtxRef = useRef<AudioContext | null>(null)
  const nextNoteTimeRef = useRef(0)
  const beatIndexRef = useRef(0)
  const timerRef = useRef<number | null>(null)
  const onBeatRef = useRef(onBeat)
  const bpmRef = useRef(bpm)
  const beatCountRef = useRef(beatCount)

  useEffect(() => {
    onBeatRef.current = onBeat
  }, [onBeat])

  useEffect(() => {
    bpmRef.current = bpm
  }, [bpm])

  useEffect(() => {
    beatCountRef.current = beatCount
  }, [beatCount])

  const click = useCallback((time: number, accent: boolean) => {
    const ctx = audioCtxRef.current
    if (!ctx) return
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.frequency.value = accent ? 1200 : 800
    gain.gain.setValueAtTime(0.0001, time)
    gain.gain.exponentialRampToValueAtTime(0.25, time + 0.005)
    gain.gain.exponentialRampToValueAtTime(0.0001, time + 0.06)
    osc.start(time)
    osc.stop(time + 0.07)
  }, [])

  const scheduler = useCallback(() => {
    const ctx = audioCtxRef.current
    if (!ctx) return
    const scheduleAhead = 0.1
    while (nextNoteTimeRef.current < ctx.currentTime + scheduleAhead) {
      const index = beatIndexRef.current
      click(nextNoteTimeRef.current, index === 0)
      setBeatIndex(index)
      onBeatRef.current?.(index)
      const secondsPerBeat = 60 / bpmRef.current
      nextNoteTimeRef.current += secondsPerBeat
      beatIndexRef.current = (index + 1) % Math.max(beatCountRef.current, 1)
    }
  }, [click])

  const stop = useCallback(() => {
    if (timerRef.current !== null) {
      window.clearInterval(timerRef.current)
      timerRef.current = null
    }
    setIsPlaying(false)
    setBeatIndex(-1)
    beatIndexRef.current = 0
  }, [])

  const start = useCallback(async () => {
    if (!audioCtxRef.current) {
      audioCtxRef.current = new AudioContext()
    }
    if (audioCtxRef.current.state === 'suspended') {
      await audioCtxRef.current.resume()
    }
    beatIndexRef.current = 0
    nextNoteTimeRef.current = audioCtxRef.current.currentTime + 0.05
    setIsPlaying(true)
    timerRef.current = window.setInterval(scheduler, 25)
    scheduler()
  }, [scheduler])

  const toggle = useCallback(() => {
    if (isPlaying) stop()
    else void start()
  }, [isPlaying, start, stop])

  useEffect(() => () => stop(), [stop])

  // Reset highlight when beat count changes (e.g. new scale)
  useEffect(() => {
    beatIndexRef.current = 0
    if (!isPlaying) setBeatIndex(-1)
  }, [beatCount, isPlaying])

  return { isPlaying, beatIndex, toggle, stop }
}
