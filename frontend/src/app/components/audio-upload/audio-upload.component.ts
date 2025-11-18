import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AudioAnalysisService, AudioAnalysisResult } from '../../services/audio-analysis.service';

@Component({
  selector: 'app-audio-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audio-upload.component.html',
  styleUrls: ['./audio-upload.component.css']
})
export class AudioUploadComponent implements OnInit, OnDestroy {

  selectedFile: File | null = null;
  result: AudioAnalysisResult | null = null;
  isLoading: boolean = false;
  error: string | null = null;

  // Recording state
  isRecording: boolean = false;
  mediaRecorder: MediaRecorder | null = null;
  recordedChunks: Blob[] = [];
  recordingTime: number = 0;
  recordingInterval: any;

  // Audio playback
  audioPlayer: HTMLAudioElement | null = null;
  isPlayingAudio: boolean = false;

  constructor(private audioService: AudioAnalysisService) {}

  ngOnInit() {
    // Check for browser support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.warn('MediaRecorder API not supported');
    }
  }

  ngOnDestroy() {
    this.stopRecording();
    this.stopAudio();
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.result = null;
      this.error = null;
    }
  }

  async startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.recordedChunks = [];
      this.isRecording = true;
      this.recordingTime = 0;

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.recordedChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        const blob = new Blob(this.recordedChunks, { type: 'audio/webm' });
        this.selectedFile = new File([blob], 'recording.webm', { type: 'audio/webm' });
        stream.getTracks().forEach(track => track.stop());
      };

      this.mediaRecorder.start();
      
      // Start timer
      this.recordingInterval = setInterval(() => {
        this.recordingTime++;
      }, 1000);

    } catch (error) {
      console.error('Error starting recording:', error);
      this.error = 'Failed to start recording. Please check microphone permissions.';
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
      if (this.recordingInterval) {
        clearInterval(this.recordingInterval);
        this.recordingInterval = null;
      }
    }
  }

  formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  upload() {
    if (!this.selectedFile) return;

    this.isLoading = true;
    this.error = null;
    this.result = null;
    this.stopAudio(); // Stop any playing audio

    this.audioService.analyzeAudio(this.selectedFile).subscribe({
      next: (res) => {
        this.result = res;
        this.isLoading = false;
        if (res.error) {
          this.error = res.error;
        }
      },
      error: (err) => {
        console.error('Error:', err);
        this.error = err.error?.error || 'Failed to analyze audio. Please try again.';
        this.isLoading = false;
      }
    });
  }

  playAudio() {
    if (!this.result?.audio_url) return;

    const audioUrl = this.audioService.getAudioUrl(this.result.audio_url);
    if (!audioUrl) return;

    this.stopAudio(); // Stop any existing audio

    this.audioPlayer = new Audio(audioUrl);
    this.isPlayingAudio = true;

    this.audioPlayer.onended = () => {
      this.isPlayingAudio = false;
    };

    this.audioPlayer.onerror = () => {
      this.isPlayingAudio = false;
      this.error = 'Failed to play audio response.';
    };

    this.audioPlayer.play().catch(err => {
      console.error('Error playing audio:', err);
      this.isPlayingAudio = false;
      this.error = 'Failed to play audio.';
    });
  }

  stopAudio() {
    if (this.audioPlayer) {
      this.audioPlayer.pause();
      this.audioPlayer = null;
      this.isPlayingAudio = false;
    }
  }

  reset() {
    this.stopRecording();
    this.stopAudio();
    this.selectedFile = null;
    this.result = null;
    this.error = null;
    this.isLoading = false;
    this.recordingTime = 0;
    
    // Reset file input
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }
}
