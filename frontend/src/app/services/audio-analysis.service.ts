import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface OrderStatus {
  status: string;
  delivery_date: string | null;
  last_update: string | null;
}

export interface AudioAnalysisResult {
  transcript: string;
  mobile_number: string | null;
  order_id: string | null;
  customer_name: string | null;
  topic: string;
  intent: string;
  status_found: boolean;
  order_status: OrderStatus | null;
  response_text: string;
  response_voice_text: string;
  audio_url: string | null;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AudioAnalysisService {

  private apiUrl = 'http://localhost:8000/process-audio';
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  analyzeAudio(file: File): Observable<AudioAnalysisResult> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<AudioAnalysisResult>(this.apiUrl, formData);
  }

  getAudioUrl(audioUrl: string | null): string | null {
    if (!audioUrl) return null;
    return `${this.baseUrl}${audioUrl}`;
  }
}

