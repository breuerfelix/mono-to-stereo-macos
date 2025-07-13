
import sounddevice as sd
import numpy as np
import time
import multiprocessing

INPUT_CHANNEL = 0        # Channel index for input (0-based)
OUTPUT_CHANNELS = [0, 1] # Output channels to map to (channel 1 and 2)

def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(f"Stream status: {status}")
        raise Exception(f"Stream status error {status}")
    
    outdata[:, OUTPUT_CHANNELS] = np.tile(indata[:, INPUT_CHANNEL], (len(OUTPUT_CHANNELS), 1)).T

def main():
    samplerate = 96000       # 96 kHz

    devices = sd.query_devices()
    print("Available devices:")
    for i, d in enumerate(devices):
        print(f"{i}: {d['name']} (in: {d['max_input_channels']}, out: {d['max_output_channels']})")

    input_device_index = next((i for i, d in enumerate(devices) if d['name'].lower().startswith('scarlett')), None)
    output_device_index = next((i for i, d in enumerate(devices) if d['name'].lower().startswith('blackhole')), None)

    if input_device_index is None or output_device_index is None:
        print("Could not find Scarlett input or Blackhole output device.")
        return

    print(f"Using input device {input_device_index}: {devices[input_device_index]['name']}")
    print(f"Using output device {output_device_index}: {devices[output_device_index]['name']}")

    with sd.Stream(device=(input_device_index, output_device_index),
                    channels=(INPUT_CHANNEL+1, max(OUTPUT_CHANNELS)+1),
                    dtype='float32',
                    samplerate=samplerate,
                    blocksize=0,
                    latency=0.1,
                    callback=audio_callback) as s:

        print(f"Routing audio at {samplerate} Hz... Press Ctrl+C to stop.")

        while s.active:
            time.sleep(1)

        print("Stream not active anymore.")

    print("Stream closed.")

def run_main_on_core():
    while True:
        p = multiprocessing.Process(target=main)
        p.start()
        p.join()
        print("Main function stopped. Waiting 10 seconds before restarting...")
        time.sleep(10)

if __name__ == "__main__":
    run_main_on_core()