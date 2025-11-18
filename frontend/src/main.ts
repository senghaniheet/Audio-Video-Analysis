import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';
import { Routes, provideRouter } from '@angular/router';

import { VoiceAssistantComponent } from './app/components/voice-assistant/voice-assistant';
import { AudioUploadComponent } from './app/components/audio-upload/audio-upload.component';

const routes: Routes = [
  { path: '', component: VoiceAssistantComponent },
  { path: 'Details', component: AudioUploadComponent },
];

bootstrapApplication(App, {
  ...appConfig,
  providers: [
    ...(appConfig.providers || []),
    provideRouter(routes),
  ]
}).catch((err) => console.error(err));
