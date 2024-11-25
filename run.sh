NC_API_KEY=<YOUR_NCOMPASS_API_KEY>

CHUNK_SIZE_MS=100 # chunk size for denoising, max is 10000ms can be as low as 70ms if on-prem
OUT_FRAME_RATE=8000 # out frame rate is the sampling freq of the returned deonised audio

INPUT_FILE=./multiple_speakers.wav # input file

python isolate_voice.py --wav_file         ${INPUT_FILE} \
                        --ncompass_api_key ${NC_API_KEY} \
                        --chunk_size_ms    ${CHUNK_SIZE_MS} \
                        --out_frame_rate   ${OUT_FRAME_RATE} 
                        # To run offline transcription after isolation, uncomment the following
                        # lines
                        # --transcribe     \
                        # --deepgram_api_key <YOUR DEEPGRAM API KEY>
