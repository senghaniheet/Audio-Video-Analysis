import { Component, signal } from '@angular/core';
import { AudioUploadComponent } from './components/audio-upload/audio-upload.component';

@Component({
  selector: 'app-root',
  imports: [AudioUploadComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('audio-app');
}
