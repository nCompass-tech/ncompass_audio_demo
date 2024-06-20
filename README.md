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

## API Docs
This section details the fields of the websocket API call that is required to denoise an audio
chunk.
The structure of an API call is as follows: 
```
wss://<api_key>.ncompass.tech/denoise/<in_t>/<out_t>/<api_key>/<bps>/<in_freq>/<out_freq>
```
- `<api_key>` 

  Your nCompass API key.

- `<in_t>`

  Input type. **Only valid option is pcm**. Kept in the API in order to potentially support server
  side file encoding in the future. This is important as it tells the server that that the incoming
  chunk is only audio data and doesn't have anything else like .wav headers for instance.

- `<out_t>`

  Output type. **Only valid option is pcm**. Kept in the API in order to potentially support server
  side file encoding in the future. 

- `<bps>`

  Bytes per sample. Needs to be specified so the server knows how to correctly read the binary
  chunk.

- `<in_freq>`

  The sampling frequency of the audio passed in. This needs to be specified in the API as we don't 
  pass the .wav headers to the server so cannot be inferred.

- `<out_freq>`

  The desired sampling frequency of the returned audio.
