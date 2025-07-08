from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import csv
import aiofiles
from pathlib import Path
import uvicorn  # Explicitly import uvicorn for the __main__ block

app = FastAPI()

# Get the directory of the current file
current_dir = Path(__file__).parent
DATA_DIR = current_dir.parent / "data"

# Ensure the base data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main recording_studio.html file."""
    index_path = current_dir / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "index.html not found"}


@app.post("/upload-recording")
async def upload_recording(
    speaker_name: str = Form(...),
    text: str = Form(...),
    audio_file: UploadFile = File(...)
):
    try:
        speaker_dir = DATA_DIR / speaker_name
        speaker_wav_dir = speaker_dir / "wav"
        speaker_dir.mkdir(parents=True, exist_ok=True)
        speaker_wav_dir.mkdir(parents=True, exist_ok=True)

        metadata_path = speaker_dir / "metadata.csv"
        next_id = 1

        if metadata_path.exists():
            async with aiofiles.open(metadata_path, mode="r", encoding="utf-8") as f:
                lines = await f.readlines()
                if lines:
                    # Find the last ID used
                    last_line = lines[-1].strip()
                    if last_line:
                        try:
                            last_id_str = last_line.split('|')[0]
                            next_id = int(last_id_str) + 1
                        except ValueError:
                            # next_id remains 1 if parsing fails
                            pass

        # Format ID with leading zeros
        formatted_id = str(next_id).zfill(4)
        wav_filename = f"{formatted_id}.wav"
        wav_filepath = speaker_wav_dir / wav_filename

        # Save the audio file
        async with aiofiles.open(wav_filepath, mode="wb") as f:
            while content := await audio_file.read(1024 * 1024):
                await f.write(content)

        # Append metadata to CSV
        async with aiofiles.open(metadata_path, mode="a", encoding="utf-8",
                                  newline='') as f:
            writer = csv.writer(f, delimiter='|')
            await writer.writerow([formatted_id, text])

        return JSONResponse(content={"message": "Recording saved successfully",
                                      "id": formatted_id,
                                      "speaker": speaker_name})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload recording: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
