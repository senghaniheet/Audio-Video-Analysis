import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VoiceAssistantComponent } from './components/voice-assistant/voice-assistant';
import { AudioUploadComponent } from './components/audio-upload/audio-upload.component';

const routes: Routes = [
  { path: '', component: VoiceAssistantComponent },
  { path: 'Details', component: AudioUploadComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
