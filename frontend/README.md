# ClauseAI Frontend

Modern React frontend for the ClauseAI Legal Contract Analyzer.

## Features

- 🎨 Beautiful dark-themed UI with smooth animations
- 📤 Drag & drop file upload
- 📊 Real-time contract analysis results
- 🔍 Clause extraction with category tabs
- ⚠️ Risk identification with severity levels
- 💬 Agent discussion threads
- 📱 Fully responsive design

## Tech Stack

- **React 18** - UI framework
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **React Icons** - Icon library

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will run on **http://localhost:3000**

### 3. Start Backend API

In a separate terminal, from the project root:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Start Flask API server
python api_server.py
```

The backend will run on **http://localhost:8000**

## File Structure

```
frontend/
├── index.html              # HTML entry point
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── src/
│   ├── main.jsx           # React entry point
│   ├── App.jsx            # Main app component
│   ├── components/
│   │   ├── FileUpload.jsx # File upload with drag-drop
│   │   └── Results.jsx    # Analysis results display
│   └── styles/
│       └── App.css        # Main stylesheet
└── public/                # Static assets
```

## Build for Production

```bash
npm run build
```

Built files will be in the `dist/` folder.

## API Endpoints

- **POST /analyze** - Analyze contract document
  - Accepts: multipart/form-data with 'file' field
  - Returns: JSON with analysis results

- **GET /health** - Health check
  - Returns: Service status

## Supported File Types

- PDF (.pdf)
- Word Documents (.docx, .doc)
- Text Files (.txt)

## Color Scheme

- Primary: #2563eb (Blue)
- Secondary: #8b5cf6 (Purple)
- Success: #10b981 (Green)
- Warning: #f59e0b (Orange)
- Danger: #ef4444 (Red)
- Dark Background: #0f172a
- Card Background: #1e293b
