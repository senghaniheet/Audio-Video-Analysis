import { Component } from '@angular/core';
import { AudioAnalysisService, AudioAnalysisResult } from '../../services/audio-analysis.service';

@Component({
  selector: 'app-audio-upload',
  templateUrl: './audio-upload.component.html',
  styleUrls: ['./audio-upload.component.css']
})
export class AudioUploadComponent {

  selectedFile: File | null = null;
  result: AudioAnalysisResult | null = null;
  isLoading: boolean = false;
  error: string | null = null;

  constructor(private audioService: AudioAnalysisService) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.result = null;
      this.error = null;
    }
  }

  upload() {
    if (!this.selectedFile) return;

    this.isLoading = true;
    this.error = null;
    this.result = null;

    this.audioService.analyzeAudio(this.selectedFile).subscribe(
      (res) => {
        this.result = res;
        this.isLoading = false;
        if (res.error) {
          this.error = res.error;
        }
      },
      (err) => {
        console.error('Error:', err);
        this.error = err.error?.error || 'Failed to analyze audio. Please try again.';
        this.isLoading = false;
      }
    );
  }

  reset() {
    this.selectedFile = null;
    this.result = null;
    this.error = null;
    this.isLoading = false;
    // Reset file input
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }
}

