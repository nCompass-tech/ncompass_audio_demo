# Cleaner Transcription Example

Example code for running denoising and then transcription.

## Dependencies
`pip install asyncio websockets wave deepgram-sdk`

## Running Instructions
Edit the run.sh file provided to set the following arguments.

## Arguments:
- `wav_file`:         Input file to be denoised and transcribed. mp3 and wav are valid file types
- `deepgram_api_key`: Deepgram API Key
- `ncompass_api_key`: nCompass API Key
- `in_file_type`:     Type of input audio stream. Can be one of ['pcm' or 'mp3']
- `out_file_type`:    Type of output audio stream. Can be one of ['pcm' or 'mp3']
- `chunk_size_ms`:    Chunk size in ms of the chunks of input audio stream sent for denoising. Max value is 10000ms
- `out_frame_rate`:   Output sampling frequency of the returned denoised audio stream

