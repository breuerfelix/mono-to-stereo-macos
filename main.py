import sounddevice as sd
import numpy as np

# Set your input and output device indices (use sd.query_devices() to find them)
INPUT_DEVICE_INDEX = 1  # Replace with your input device index
OUTPUT_DEVICE_INDEX = 3  # Replace with your output device index
INPUT_CHANNEL = 0        # Channel index for input (0-based)
OUTPUT_CHANNELS = [0, 1] # Output channels to map to (channel 1 and 2)
SAMPLERATE = 96000  # 192 kHz

def audio_callback(indata, outdata, frames, time, status):
    # Map the selected input channel to output channels 1 and 2
    outdata[:, OUTPUT_CHANNELS] = np.tile(indata[:, INPUT_CHANNEL], (len(OUTPUT_CHANNELS), 1)).T

if __name__ == "__main__":
    print("Available devices:")
    print(sd.query_devices())
    import sys
    with sd.Stream(device=(INPUT_DEVICE_INDEX, OUTPUT_DEVICE_INDEX),
                   channels=(INPUT_CHANNEL+1, max(OUTPUT_CHANNELS)+1),
                   dtype='float32',
                   samplerate=SAMPLERATE,
                   blocksize=0,
                   latency=0.1,
                   callback=audio_callback):
        print(f"Routing audio at {SAMPLERATE} Hz... Press Ctrl+C to stop.")
        input()
