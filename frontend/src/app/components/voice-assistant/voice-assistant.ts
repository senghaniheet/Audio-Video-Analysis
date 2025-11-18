import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AudioAnalysisResult, AudioAnalysisService } from '../../services/audio-analysis.service';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  text: string;
  audioUrl?: string;
  hasAudio?: boolean;
  timestamp: string;
}

@Component({
  selector: 'app-voice-assistant',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './voice-assistant.html',
  styleUrls: ['./voice-assistant.css'],
})
export class VoiceAssistantComponent implements OnInit, OnDestroy {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef;
  @ViewChild('fileInput') fileInput!: ElementRef;
  messages: Message[] = [];
  isRecording = false;
  isPlaying = false;
  currentPlayingId: string | null = null;
  recordingDuration = 0;
  recordedAudio: Blob | null = null;
  showHistory = false;
  isLoading = false;
  isProcessing = false;
  private mediaRecorder!: MediaRecorder;
  private audioChunks: Blob[] = [];
  private audio: HTMLAudioElement | null = null;
  private recordingInterval: any;

  ngOnInit(): void {
    this.loadHistory();
  }

  ngOnDestroy(): void {
    this.cleanup();
  }
  constructor(private audioService: AudioAnalysisService) {}
  private cleanup(): void {
    if (this.recordingInterval) {
      clearInterval(this.recordingInterval);
    }

    if (this.audio) {
      this.audio.pause();
      this.audio = null;
    }

    if (this.mediaRecorder) {
      this.mediaRecorder.stream.getTracks().forEach((track) => track.stop());
    }
  }

  async loadHistory(): Promise<void> {
    try {
      const stored = localStorage.getItem('voice_assistant_messages');
      if (stored) {
        this.messages = JSON.parse(stored);
      }
    } catch (error) {
      console.log('No previous history found');
    }
  }

  async saveMessageToHistory(message: Message): Promise<void> {
    try {
      const currentMessages = [...this.messages];
      localStorage.setItem('voice_assistant_messages', JSON.stringify(currentMessages));
    } catch (error) {
      console.error('Failed to save message:', error);
    }
  }

  async clearHistory(): Promise<void> {
    try {
      localStorage.removeItem('voice_assistant_messages');
      this.messages = [];
      this.showHistory = false;
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  }

  async startRecording(): Promise<void> {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm', // native format (no lag)
      });

      this.audioChunks = [];

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.start(100); // small chunks → no lag

      this.isRecording = true;

      this.recordingDuration = 0;
      this.recordingInterval = setInterval(() => {
        this.recordingDuration++;
      }, 1000);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Unable to access microphone. Please check permissions.');
    }
  }

  stopRecording(): Promise<File> {
    return new Promise((resolve) => {
      if (!this.mediaRecorder || !this.isRecording) {
        resolve(null as any);
        return;
      }

      this.mediaRecorder.onstop = () => {
        const finalBlob = new Blob(this.audioChunks, { type: 'audio/webm' });

        const finalFile = new File([finalBlob], 'audio.webm', {
          type: 'audio/webm',
          lastModified: Date.now(),
        });

        this.recordedAudio = finalFile;

        // Stop mic
        this.mediaRecorder.stream.getTracks().forEach((t) => t.stop());

        resolve(finalFile);
      };

      this.mediaRecorder.stop();
      this.isRecording = false;
      clearInterval(this.recordingInterval);
    });
  }

  async toggleRecording(): Promise<void> {
    if (this.isRecording) {
      const file = await this.stopRecording(); // WAIT FOR audio
      console.log('Recording ready:', file);
    } else {
      this.startRecording();
    }
  }

  onFileUpload(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.isLoading = true;
      // Simulate processing time for upload
      setTimeout(() => {
        this.recordedAudio = input.files![0];
        this.isLoading = false;
        input.value = '';
      }, 1000);
    }
  }

  async callAPI(audioBlob: Blob): Promise<string> {
    this.isProcessing = true;

    try {
      const audioFile = new File([audioBlob], 'audio.wav', { type: 'audio/wav' });

      return new Promise<string>((resolve) => {
        this.audioService.analyzeAudio(audioFile).subscribe({
          next: (res: AudioAnalysisResult) => {
            this.isProcessing = false;

            // Error from server
            if (res.error) {
              resolve(
                'Sir, I was not able to understand the audio properly. Could you please try again once?'
              );
              return;
            }

            // Success
            resolve(
              res.response_text || 'Sir, I understood your message. How else can I help you?'
            );
          },

          error: () => {
            this.isProcessing = false;

            resolve('Sorry sir, I couldn’t process your audio right now. Please try once again.');
          },
        });
      });
    } catch {
      return 'Sir, there seems to be a small issue while reading your audio. Please try again sir.';
    } finally {
      this.isLoading = false;
    }
  }

  async sendMessage(): Promise<void> {
    if (!this.recordedAudio) return;
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      type: 'user',
      text: '🎤 Voice message sent',
      audioUrl: URL.createObjectURL(this.recordedAudio),
      timestamp: new Date().toISOString(),
    };

    this.messages.push(userMessage);

    await this.saveMessageToHistory(userMessage);

    const currentAudio = this.recordedAudio;
    this.recordedAudio = null;

    // Scroll to bottom

    setTimeout(() => this.scrollToBottom(), 100);

    // Call API with the audio
    const responseText = await this.callAPI(currentAudio);

    const assistantMessage: Message = {
      id: `assistant-${Date.now()}`,
      type: 'assistant',
      text: responseText,
      hasAudio: true,
      timestamp: new Date().toISOString(),
    };

    this.messages.push(assistantMessage);

    await this.saveMessageToHistory(assistantMessage);

    // Scroll to bottom

    setTimeout(() => this.scrollToBottom(), 100);
  }

  playAudio(audioUrl: string, messageId: string): void {
    if (this.isPlaying && this.currentPlayingId === messageId) {
      this.audio?.pause();
      this.isPlaying = false;
      this.currentPlayingId = null;
      return;
    }

    if (this.audio) {
      this.audio.pause();
    }

    this.audio = new Audio(audioUrl);
    this.currentPlayingId = messageId;
    this.isPlaying = true;
    this.audio.onended = () => {
      this.isPlaying = false;
      this.currentPlayingId = null;
    };

    this.audio.play();
  }

  speakText(text: string, messageId: string): void {
    if ('speechSynthesis' in window) {
      if (this.isPlaying && this.currentPlayingId === messageId) {
        window.speechSynthesis.cancel();
        this.isPlaying = false;
        this.currentPlayingId = null;
        return;
      }

      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      this.currentPlayingId = messageId;
      this.isPlaying = true;
      utterance.onend = () => {
        this.isPlaying = false;
        this.currentPlayingId = null;
      };

      window.speechSynthesis.speak(utterance);
    }
  }

  formatTime(timestamp: string): string {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  formatDate(timestamp: string): string {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
  }

  shouldShowDate(index: number): boolean {
    if (index === 0) return true;
    const currentDate = this.formatDate(this.messages[index].timestamp);
    const previousDate = this.formatDate(this.messages[index - 1].timestamp);
    return currentDate !== previousDate;
  }

  toggleHistory(): void {
    this.showHistory = !this.showHistory;
  }

  private scrollToBottom(): void {
    if (this.messagesContainer) {
      const element = this.messagesContainer.nativeElement;
      element.scrollTop = element.scrollHeight;
    }
  }
}
