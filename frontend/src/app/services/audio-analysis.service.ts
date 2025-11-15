import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AudioAnalysisResult {
  transcript: string;
  summary: string;
  sentiment: string;
  keywords: string[];
  issues: string[];
  actionItems: string[];
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AudioAnalysisService {

  private apiUrl = 'http://localhost:8000/analyze-audio';

  constructor(private http: HttpClient) {}

  analyzeAudio(file: File): Observable<AudioAnalysisResult> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<AudioAnalysisResult>(this.apiUrl, formData);
  }
}

