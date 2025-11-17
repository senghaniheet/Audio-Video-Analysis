import { Component, signal } from '@angular/core';
import { AudioUploadComponent } from './components/audio-upload/audio-upload.component';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('audio-app');
}
