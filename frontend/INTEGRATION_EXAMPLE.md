# Integration Example

## For Angular < 17 (Using NgModule)

### app.module.ts
```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { AudioUploadComponent } from './components/audio-upload/audio-upload.component';
import { AudioAnalysisService } from './services/audio-analysis.service';

@NgModule({
  declarations: [
    AppComponent,
    AudioUploadComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [AudioAnalysisService],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

### app.component.html
```html
<app-audio-upload></app-audio-upload>
```

## For Angular 17+ (Standalone Components)

### audio-upload.component.ts (Update)
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AudioAnalysisService, AudioAnalysisResult } from '../../services/audio-analysis.service';

@Component({
  selector: 'app-audio-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './audio-upload.component.html',
  styleUrls: ['./audio-upload.component.css']
})
export class AudioUploadComponent {
  // ... rest of the component code
}
```

### audio-analysis.service.ts (Update)
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AudioAnalysisService {
  // ... service code
}
```

### app.config.ts
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient()
  ]
};
```

### app.component.ts
```typescript
import { Component } from '@angular/core';
import { AudioUploadComponent } from './components/audio-upload/audio-upload.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AudioUploadComponent],
  template: '<app-audio-upload></app-audio-upload>'
})
export class AppComponent {
  title = 'Voice Transcription App';
}
```

