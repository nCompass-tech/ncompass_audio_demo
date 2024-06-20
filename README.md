# nCompass Voice Isolation Demo

Example code for running voice isolation and then offline transcription with your choice of STT.

## Dependencies
### Voice Isolation only
`pip install asyncio websockets wave`
### To add deepgram transcription: 
`pip install deepgram-sdk`

## Running Instructions
Edit the run.sh file provided to set the following arguments.

### Arguments:
#### Voice Isolation arguments
- `--wav_file <PATH_TO_FILE>`

     Input file to be denoised and transcribed. **File must be a .wav file**
- `--ncompass_api_key <API_KEY>`

   nCompass API Key
- `--chunk_size_ms <CHUNK_SIZE_MS>`

  Chunk size in ms of the chunks of input audio stream sent for denoising. **Max value is 10000ms**.

  **Note:** The chunk size field is only necessary when emulating streaming audio with an audio file as this requires the file to be chunked into a stream with elements of the specified chunk size. If you already have streaming audio, you can simply pass the stream's chunks via our websocket API to be denoised. Our API will automatically handle arbitrary chunk sizes.
- `--out_frame_rate <FRAME_RATE>`

  Output sampling frequency of the returned denoised audio stream.

  **Note:** This is important as we up/downsample your audio stream to the desired frequency on the server.

#### To enable transcription after isolation
- `--transcribe`

  Flag that runs offline-transcription of your audio after it is denoised.
- `--deepgram_api_key <API KEY>`: Deepgram API Key

  We have provided an example for deepgram transcription, but you can edit this to use any STT of your choice.
