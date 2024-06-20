import wave
import asyncio
import argparse
import websockets
from typing import AsyncIterator, cast
from deepgram import DeepgramClient, PrerecordedOptions

def deepgram_transcription(audio_file: str
                           , api_key:  str) -> str:
    '''
    This function takes in an audio file in wav format and runs deepgram transcription with your
    deepgram API key. This can be swapped out for any transcription provider you choose.
    '''
    print(f"INFO => Running Deepgram transcription...")
    deepgram = DeepgramClient(api_key)

    with open(audio_file, "rb") as buffer_data:
        payload = { "buffer": buffer_data }

        options = PrerecordedOptions(
            smart_format=True, model="nova-2", language="en-US"
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        return response["results"]["channels"][0]["alternatives"][0]["transcript"]

def get_url(api_key:            str
            , input_freq:       int
            , output_freq:      int
            , bytes_per_sample: int
            , in_file_type:     str
            , out_file_type:    str) -> str:
    '''
    The websocket API format is as follows:
    wss://<url>/denoise/<input_format>/<output_format>/<api_key>/<bytes_per_sample>
        /<input_sampling_frequency>/<output_sampling_frequency>
    Note here that the API is set to take in and return bytes in PCM format, i.e. the wav header
    should be parsed.
    '''
    return (f"wss://{api_key}.ncompass.tech/denoise/{in_file_type}/{out_file_type}/{api_key}"
            f"/{bytes_per_sample}/{input_freq}/{output_freq}")

def get_bytes_per_chunk(chunk_size_ms: int, frame_rate: int, bytes_per_frame: int) -> int:
    return int(bytes_per_frame * ((chunk_size_ms / 1000) * frame_rate))

async def chunk_audio(audio_frames:       bytes
                      , chunk_size_ms:    int
                      , in_frame_rate:    int
                      , bytes_per_sample: int) -> AsyncIterator[bytes] :
    ''' 
    This function takes the input audio file read in as bytes and chunks it into chunks based on
    the chunk size specified. The chunks are yielded followed by a async sleep to yield back
    control to the running thread from an infinite while loop. 
    '''
    bytes_per_chunk = get_bytes_per_chunk(chunk_size_ms, in_frame_rate, bytes_per_sample)
    chunk_start = 0
    while True:
        if chunk_start >= len(audio_frames): break
        end = chunk_start + bytes_per_chunk
        chunk_end = end if end < len(audio_frames) else len(audio_frames)
        chunk = audio_frames[chunk_start:chunk_end]
        chunk_start = chunk_end
        yield chunk
        await asyncio.sleep(0)

async def ncompass_denoising(wav_file:         str
                             , api_key:        str
                             , chunk_size_ms:  int
                             , out_frame_rate: int) -> str:
    print(f"INFO => Denoising audio file {wav_file}...")
    output_file_name = "denoised_audio.wav"
    '''
    First open the file with the wave library to parse the wav header correctly and convert to a
    PCM format.
    '''
    with wave.open(wav_file, "rb") as wh:
        in_frame_rate = wh.getframerate()
        bytes_per_sample = wh.getsampwidth()
        audio_frames = wh.readframes(wh.getnframes())
        
        '''
        Out frame rate is hardcoded to 8000 as our model currently performs all computations at
        8000 Hz. Hence, if a different input and output frame rate is provided, we first down/up
        sample the input to 8kHz and then down/up sample the resulting audio to the desired output
        sampling frequency. We hardcode the value to 8kHz here to avoid the second resampling since
        we are only using the resulting audio for transcription.
        '''
        out_frame_rate = out_frame_rate
        
        '''
        Chunk size is hardcoded to 10s as this is the maximum chunk size currently supported by our
        model and we are running in offline mode.
        '''
        chunk_size_ms = chunk_size_ms
        async with websockets.connect(get_url(api_key
                                              , in_frame_rate
                                              , out_frame_rate
                                              , bytes_per_sample
                                              , "pcm"  
                                              , "pcm")) as ws:
                num_frames_received = 0
                denoised_audio = bytearray(b"")
                async for chunk in chunk_audio(audio_frames
                                               , chunk_size_ms
                                               , in_frame_rate
                                               , bytes_per_sample):
                    await ws.send(chunk)
                    res = cast(bytes, await ws.recv())
                    
                    '''
                    As the return type is set to pcm in the websocket request, we can directly
                    accumulate the bytes into a bytearray.
                    '''
                    denoised_audio += res
        
        # Note: for now the API only supports single input and output channels
        with wave.open(output_file_name, "wb") as out_file: 
            out_file.setnchannels(1)
            out_file.setsampwidth(bytes_per_sample)
            out_file.setframerate(out_frame_rate)
            if num_frames_received != 0: out_file.setnframes(num_frames_received)
            out_file.writeframes(denoised_audio)

    return output_file_name

async def isolate_voice(wav_file:           str
                        , ncompass_api_key: str
                        , chunk_size_ms:    int
                        , out_frame_rate:   int) -> str:
    return await ncompass_denoising(wav_file
                                    , ncompass_api_key
                                    , chunk_size_ms
                                    , out_frame_rate)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--ncompass_api_key"
                            , type=str
                            , required=True
                            , help = "API Key for nCompass denoising")
    arg_parser.add_argument("--wav_file"
                            , type=str
                            , required=True
                            , help = "File to denoise in .wav format")
    arg_parser.add_argument("--chunk_size_ms"
                            , type=int
                            , default=10000
                            , help = "Chunk size for realtime processing")
    arg_parser.add_argument("--out_frame_rate"
                            , type=int
                            , default=8000
                            , help = "Frame rate for returned audio")
    
    arg_parser.add_argument("--transcribe"
                            , action="store_true"
                            , default=False
                            , help="Run offline transcription after denoising or not")
    arg_parser.add_argument("--deepgram_api_key"
                            , type=str
                            , default=None
                            , help = "API Key for deepgram transcription")
    
    args = arg_parser.parse_args()
    denoised_audio_file = asyncio.run(isolate_voice(args.wav_file
                                                    , args.ncompass_api_key
                                                    , args.chunk_size_ms
                                                    , args.out_frame_rate))
    
    if args.transcribe:
        transcription = deepgram_transcription(denoised_audio_file, args.deepgram_api_key)
        print("INFO => Transcription: ")
        print(transcription)
