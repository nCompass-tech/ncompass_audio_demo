# nCompass Voice Isolation Demo

Example code for running voice isolation and then offline transcription with your choice of STT.

## Dependencies
### Voice Isolation only
`pip install asyncio websockets wave`
### To add deepgram transcription: 
`pip install deepgram-sdk`

## Running Instructions
Edit the run.sh file provided to set the following arguments.

## Arguments:
### Voice Isolation arguments
- `--wav_file <PATH_TO_FILE>`:       Input file to be denoised and transcribed. *File must be a .wav file*
- `--ncompass_api_key <API_KEY>`:    nCompass API Key
- `--chunk_size_ms <CHUNK_SIZE_MS>`: Chunk size in ms of the chunks of input audio stream sent for denoising. Max value is 10000ms
- `--out_frame_rate <FRAME_RATE>`:   Output sampling frequency of the returned denoised audio stream

### To enable transcription after isolation
- `--transcribe`
- `--deepgram_api_key <API KEY>`: Deepgram API Key

