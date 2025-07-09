# TTS Dataset Recording Studio

This project provides a web-based recording studio designed for collaboratively recording audio for Text-to-Speech (TTS) datasets. It supports multiple speakers and manages recordings and metadata in a PiperTTS-compatible format.

## Features

- __Collaborative Recording:__ Designed for two speakers to record sentences.

- __JSON Upload:__ Upload conversation JSON files containing speaker-tagged sentences.

- __Queued Sentences:__ Sentences are queued and presented one at a time for recording.

- __One-Click Recording:__ Record button toggles re-recording without repeated microphone permission prompts.

- __Real-time Waveform:__ Displays a real-time audio waveform sensitive to human speech.

- __Recording Timer & Limit:__ Shows elapsed time during recording with a visible 15-second recording limit.

- __Local Storage:__ All recordings and metadata are stored on the local filesystem.

- __Dataset Merging:__ New JSON uploads merge with existing datasets, rather than replacing them.

- __Multi-Speaker Dataset Management:__

  - Maintains separate datasets for each speaker (e.g., `data/speaker1/wav/` and `data/speaker1/metadata.csv`).
  - Generates a combined multi-speaker dataset (`data/combined/wav/` and `data/combined/metadata.csv`) including speaker identifiers.
  - All metadata files are in PiperTTS-compatible format.

- __Session Persistence:__ All recorded data persists across sessions.

## Technologies Used

- __Backend:__

  - [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
  - [Uvicorn](https://www.uvicorn.org/): An ASGI server for FastAPI.
  - [aiofiles](https://github.com/Tinche/aiofiles): Asynchronous file operations.
  - [python-multipart](https://pypi.org/project/python-multipart/): For handling form data, including file uploads.

- __Frontend:__

  - HTML, CSS, JavaScript
  - [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API): For real-time audio processing and visualization.
  - [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder_API): For recording audio from the microphone.
  - [JSZip](https://stuk.github.io/jszip/): For creating ZIP archives for export.

- __Containerization:__

  - [Docker](https://www.docker.com/): For packaging the application and its dependencies.
  - [Docker Compose](https://docs.docker.com/compose/): For defining and running multi-container Docker applications.

## Project Structure

```javascript
.
├── backend/
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   └── static/
│       └── index.html      # Frontend HTML, CSS, and JavaScript
├── data/                   # Persistent storage for recordings and metadata
│   ├── speaker1/
│   │   ├── wav/            # WAV audio files for speaker 1
│   │   └── metadata.csv    # Metadata for speaker 1 (PiperTTS format)
│   ├── speaker2/
│   │   ├── wav/            # WAV audio files for speaker 2
│   │   └── metadata.csv    # Metadata for speaker 2 (PiperTTS format)
│   └── combined/
│       ├── wav/            # Combined WAV audio files
│       └── metadata.csv    # Combined metadata with speaker identifiers
├── Dockerfile              # Docker build instructions for the backend service
├── docker-compose.yml      # Docker Compose configuration
├── README.md               # This file
└── sample-json.json        # Example conversation JSON file
```

## Setup and Running

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Engine and Docker Compose)

### Steps

1. __Clone the repository:__

   ```bash
   git clone <repository_url>
   cd recording_studio
   ```

2. __Build and run the Docker containers:__

   ```bash
   docker-compose up --build
   ```

   This command will:

   - Build the Docker image for the `web` service based on the `Dockerfile`.
   - Start the `web` service, mapping port `8000` from the container to port `8000` on your host machine.
   - Mount the `./backend` directory into `/app/backend` inside the container for hot-reloading during development.
   - Mount the `./data` directory into `/app/data` inside the container to ensure recordings and metadata persist on your local filesystem even if the container is removed.

3. __Access the application:__ Open your web browser and navigate to:

   ```javascript
   http://localhost:8000
   ```

## Usage

1. __Upload JSON:__ Click the "Upload JSON" button and select a conversation JSON file. The JSON should be an array of objects, each with `speaker` and `text` fields:

   ```json
   [
     {"speaker": "speaker1", "text": "Hello, how are you today?"},
     {"speaker": "speaker2", "text": "I am doing great, thanks for asking!"}
   ]
   ```

   You can upload multiple JSON files; new sentences will be appended to the existing queue.

2. __Record Sentences:__

   - The current sentence and speaker will be displayed.
   - Click "Start Recording" to begin. The button will change to "Stop Recording".
   - Click "Stop Recording" or wait for the 15-second limit to automatically stop.
   - A real-time waveform will visualize the audio input.
   - After recording, you can click "Play Recording" to review.
   - If satisfied, click "Accept" to save the recording and move to the next sentence.
   - If not satisfied, click "Start Recording" again to re-record the current sentence.
   - Click "Skip" to move to the next sentence without recording.

3. __Export Recordings:__

   - Once all sentences are processed, the "Export Recordings" section will appear.

   - Buttons will be generated for each unique speaker (e.g., "Export speaker1 Recordings").

   - Click an "Export" button to download a ZIP file containing:

     - A `speakerX.txt` file with metadata in PiperTTS format (`id|text`).
     - A `speakerX/` directory containing the recorded `.wav` files (e.g., `0001.wav`).

## Development

### Backend (FastAPI)

The `backend/main.py` file contains the FastAPI application. It handles:

- Serving the `index.html` frontend.
- Receiving audio uploads (`/upload-recording`).
- Saving WAV files and updating `metadata.csv` for individual speakers.
- The Docker Compose setup includes hot-reloading, so changes to `backend/main.py` will automatically restart the server.

### Frontend (HTML, CSS, JavaScript)

The `backend/static/index.html` file contains the entire frontend. Key JavaScript functionalities include:

- Handling JSON file uploads and parsing.
- Managing the sentence queue and UI updates.
- Microphone access and real-time audio visualization using Web Audio API.
- Audio recording using MediaRecorder API.
- Converting recorded audio to WAV format (16-bit PCM, 16kHz sample rate).
- Uploading recordings to the backend.
- Generating and downloading ZIP archives of recordings using JSZip.

### Data Persistence

The `data/` directory is mounted as a Docker volume, ensuring that all recorded `.wav` files and `metadata.csv` files persist on your host machine even if the Docker containers are stopped or removed. This means your recorded datasets will not be lost.

## Version Control (Git)

This project uses Git for version control. Follow these best practices:

- __Commit Frequently:__ Make small, atomic commits that represent a single logical change.
- __Descriptive Commit Messages:__ Write clear and concise commit messages that explain *what* was changed and *why*.
- __Branching:__ Use feature branches for new features or bug fixes to keep the `main` branch stable.
- __Pull Requests:__ Submit pull requests for code review before merging into `main`.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.
