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
- `--wav_file <PATH_TO_FILE>`

     Input file to be denoised and transcribed. **File must be a .wav file**
- `--ncompass_api_key <API_KEY>`

   nCompass API Key
- `--chunk_size_ms <CHUNK_SIZE_MS>`

  Chunk size in ms of the chunks of input audio stream sent for denoising. **Max value is 10000ms**.

  **Note:** This field is only necessary here as the code converts the audio file into a stream with the specified chunk size in order to emulate realtime voice isolation. If you already have a stream of chunk size, you can simply pass this via our websocket API to be denoised. Our API can handle arbitrary chunk sizes.
- `--out_frame_rate <FRAME_RATE>`

  Output sampling frequency of the returned denoised audio stream.

  **Note:** This is important as we up/downsample your audio stream to the desired frequency on the server.

### To enable transcription after isolation
- `--transcribe`

  True or false that sets if we should transcribe your audio after it is denoised.
- `--deepgram_api_key <API KEY>`: Deepgram API Key

  We have provided an example for deepgram transcription, but you can edit this to use any STT of your choice.

