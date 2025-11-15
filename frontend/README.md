# Frontend Setup Instructions

## Quick Start

1. **Install Angular CLI (if not already installed):**
```bash
npm install -g @angular/cli
```

2. **Create Angular project (if starting fresh):**
```bash
ng new frontend
cd frontend
```

3. **Copy the component and service files:**
   - Copy `src/app/services/audio-analysis.service.ts`
   - Copy `src/app/components/audio-upload/` directory

4. **Update app module/config:**

   **For Angular < 17 (app.module.ts):**
   ```typescript
   import { HttpClientModule } from '@angular/common/http';
   import { AudioUploadComponent } from './components/audio-upload/audio-upload.component';
   import { AudioAnalysisService } from './services/audio-analysis.service';
   
   @NgModule({
     declarations: [AudioUploadComponent, ...],
     imports: [HttpClientModule, ...],
     providers: [AudioAnalysisService],
     ...
   })
   ```

   **For Angular 17+ (app.config.ts):**
   ```typescript
   import { provideHttpClient } from '@angular/common/http';
   
   export const appConfig: ApplicationConfig = {
     providers: [provideHttpClient(), ...]
   };
   ```

5. **Add component to app.component.html:**
```html
<app-audio-upload></app-audio-upload>
```

6. **Run development server:**
```bash
ng serve
```

The app will be available at `http://localhost:4200`

## Notes

- Make sure the backend is running on port 8000
- If backend is on a different port, update `apiUrl` in `audio-analysis.service.ts`

