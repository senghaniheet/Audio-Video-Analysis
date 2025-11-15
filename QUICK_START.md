# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Backend Setup (2 minutes)

```bash
cd backend
pip install -r requirements.txt
```

Set your OpenAI API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_key_here"

# Windows CMD
set OPENAI_API_KEY=your_key_here

# macOS/Linux
export OPENAI_API_KEY=your_key_here
```

Start the backend:
```bash
python main.py
```

✅ Backend running on `http://localhost:8000`

### Step 2: Frontend Setup (3 minutes)

If you don't have an Angular project yet:
```bash
npm install -g @angular/cli
ng new frontend
cd frontend
```

Copy the provided files to your Angular project:
- `src/app/services/audio-analysis.service.ts`
- `src/app/components/audio-upload/` (all 3 files)

Update your `app.module.ts` (Angular < 17) or `app.config.ts` (Angular 17+):
- See `frontend/INTEGRATION_EXAMPLE.md` for details
- Add `HttpClientModule` or `provideHttpClient()`

Add to `app.component.html`:
```html
<app-audio-upload></app-audio-upload>
```

Start the frontend:
```bash
ng serve
```

✅ Frontend running on `http://localhost:4200`

### Step 3: Test It!

1. Open `http://localhost:4200` in your browser
2. Click "Choose Audio File"
3. Select an audio file (MP3, WAV, etc.)
4. Click "Transcribe & Analyze"
5. Wait for results! 🎉

## 📋 What You Get

- ✅ Full transcription of audio
- ✅ AI-generated summary
- ✅ Sentiment analysis (Positive/Neutral/Negative)
- ✅ Extracted keywords
- ✅ Identified issues
- ✅ Action items

## 🔧 Troubleshooting

**Backend won't start?**
- Check Python version (3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Set OpenAI API key

**Frontend can't connect?**
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**No transcription?**
- Check audio file has speech
- Verify Whisper model downloaded (first run takes time)
- Check console for errors

**OpenAI errors?**
- Verify API key is correct
- Check you have API credits
- Ensure API key has proper permissions

## 📚 More Info

- Full documentation: See `README.md`
- Backend details: See `backend/README.md`
- Frontend details: See `frontend/README.md`
- Integration examples: See `frontend/INTEGRATION_EXAMPLE.md`

