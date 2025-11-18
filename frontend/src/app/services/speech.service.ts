import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SpeechService {
  speechSupported = signal(false);
  voices = signal<SpeechSynthesisVoice[]>([]);
  selectedVoiceIndex = signal(0);
  rate = signal(1);
  pitch = signal(1);
  volume = signal(1);

  private synth: SpeechSynthesis | null = null;

  constructor() {
    if ('speechSynthesis' in window) {
      this.speechSupported.set(true);
      this.synth = window.speechSynthesis;
      this.loadVoices();

      speechSynthesis.onvoiceschanged = () => this.loadVoices();
    }
  }

  private loadVoices() {
    if (!this.synth) return;
    this.voices.set(this.synth.getVoices());
  }

  speak(text: string, onEnd?: () => void) {
    if (!this.synth || !text.trim()) return;

    this.synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);

    const voices = this.voices();
    if (voices.length > 0) {
      utterance.voice = voices[this.selectedVoiceIndex()];
    }

    utterance.rate = this.rate();
    utterance.pitch = this.pitch();
    utterance.volume = this.volume();

    utterance.onend = () => {
      if (onEnd) onEnd();
    };

    this.synth.speak(utterance);
  }

  stop() {
    this.synth?.cancel();
  }
}
