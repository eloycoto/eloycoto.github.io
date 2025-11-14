How I dictate to my computer with Kroko AI
============================================
:date: 2025-11-14 23:00
:language: en-GB
:author: eloycoto
:tags: AI, productivity
:head: Ditching cloud transcription for local AI speech recognition with Kroko
:index_title: Local Speech Recognition with Kroko AI: A Privacy-First Approach
:metatitle: How I Use Kroko AI for Local Speech-to-Text Transcription
:metatags: Kroko AI, speech recognition, local AI, privacy, transcription, ONNX, dictation
:description: A practical guide to setting up local speech recognition using Kroko AI instead of cloud-based services, prioritizing privacy and offline capabilities.
:keywords: Kroko AI, speech-to-text, local transcription, privacy, offline AI, ONNX, dictation workflow

I've been experimenting with dictation for a while now. The problem with most speech-to-text solutions is that they all send your audio to the cloud. Whether it's Google, OpenAI's Whisper API, or any other service, your voice data leaves your machine. That's always bothered me. Not because I'm saying anything particularly sensitive, but because I believe in local-first tools whenever possible.

That's why I built my own dictation setup using `Kroko AI <https://github.com/kroko-ai>`_, an ONNX-based speech recognition model that runs entirely on your machine. No cloud, no API keys, no latency, no privacy concerns.

Why Kroko?
**********

Kroko is interesting for a few reasons:

1. **It's local-first**: Everything runs on your machine. Your audio never leaves your computer.
2. **It's fast**: ONNX models are optimized for inference. On my laptop, transcription happens in near real-time.
3. **Multiple languages**: Kroko has community models for English and Spanish.
4. **Simple HTTP interface**: I wanted something I could curl from the command line, and I built a server that runs this.

The setup is straightforward. I run a simple HTTP server that accepts WAV files and returns transcriptions. No complex dependencies, just a simple Docker container with a simple Python script and the model files.

The implementation
******************

My setup consists of a simple HTTP server that wraps Kroko's ONNX inference engine. Here's how it works:

The architecture is simple: the server loads ONNX models on demand and caches them. When you send a POST request with audio, it:

1. Accepts the WAV file
2. Converts it to the format Kroko expects (mono, 16-bit samples normalized to float32)
3. Runs inference through the ONNX model
4. Returns the transcription as JSON

Here's the key part of the transcription logic:

.. code-block:: python

    def transcribe_audio(self, audio_data, model_key="en-64"):
        """Transcribe audio data using the recognizer."""
        recognizer = self.get_recognizer(model_key)

        # Parse WAV file
        wav_io = io.BytesIO(audio_data)
        with wave.open(wav_io, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            audio_bytes = wav_file.readframes(n_frames)

            # Convert to float32 normalized samples
            samples = np.frombuffer(audio_bytes, dtype=np.int16)
            samples = samples.astype(np.float32) / 32768.0

        # Process through Kroko
        stream = recognizer.create_stream()
        stream.accept_waveform(sample_rate, samples)
        stream.input_finished()

        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)

        return recognizer.get_result(stream)

Model management
****************

One thing I appreciate about Kroko is the model selection. You can choose between two size variants for most languages:

- **64-variant**: Smaller, faster, around 156MB
- **128-variant**: Larger, more accurate, but requires more resources

For my use case, the 64-variant works perfectly. The accuracy is good enough, and the speed is excellent.

My dictation workflow
*********************

I have a simple bash script (``~/bin/dictate.sh``) that:

1. Records audio from my microphone using ``arecord``
2. Saves it as a WAV file
3. Sends it to my local Kroko server
4. Returns the transcription


The process is simple: CMD+B starts the recording, CMD+B stops it. When the model finishes, all my text is inserted as keyboard input and I can fix any problems after. The code looks terribly simple:


.. code-block:: bash
    stop_recording() {
        if [ ! -f "$PID_FILE" ]; then
            notify-send "Dictation" "No recording in progress" -t 2000
            exit 1
        fi

        # Get the model type from the stored file
        local model_type="en-64"
        if [ -f "$MODEL_FILE" ]; then
            model_type=$(cat "$MODEL_FILE")
            rm -f "$MODEL_FILE"
        fi

        # Stop recording
        kill $(cat "$PID_FILE") 2>/dev/null || true
        rm -f "$PID_FILE"

        notify-send "Dictation" "Processing with $model_type model..." -t 2000

        # Wait a moment for file to be written
        sleep 0.5

        # Check if audio file exists
        if [ ! -f "$AUDIO_FILE" ]; then
            notify-send "Dictation" "No audio file found" -t 2000
            exit 1
        fi

        # Transcribe with Kroko ASR server
        RESPONSE=$(curl -s -X POST -H "Content-Type: audio/wav" \
                        --data-binary "@$AUDIO_FILE" \
                        "${KROKO_URL}?model=${model_type}")

        # Extract transcription from JSON response
        TRANSCRIPTION=$(echo "$RESPONSE" | jq -r '.transcription // empty' | \
                        tr -d '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

        # Clean up audio file
        #rm -f "$AUDIO_FILE"

        # Type the transcription
        if [ -n "$TRANSCRIPTION" ]; then
            echo "type $TRANSCRIPTION" | dotool
            notify-send "Dictation" "Text inserted: ${TRANSCRIPTION:0:50}..." -t 3000
        else
            notify-send "Dictation" "No speech detected" -t 2000
        fi
    }

This setup solves a few problems I had with other dictation tools:

1. **Privacy**: My voice data stays on my machine. No cloud providers, no terms of service changes, no data retention policies to worry about.
2. **Cost**: No API costs. The models are free (community-contributed), and the compute is local.
3. **Reliability**: Works offline. No internet? No problem. The transcription still works.
4. **Simplicity**: It's just an HTTP server. I can integrate it anywhere: shell scripts, editors, custom tools, whatever I need.

Compared to cloud solutions like Whisper API or Google Speech-to-Text, this is dramatically simpler and more private. Yes, Whisper might be more accurate for certain use cases, but for my daily dictation needs, Kroko is more than good enough.

What's next
***********

I'm thinking about a few improvements:

- **Streaming support**: Right now I record first, then transcribe. Kroko supports streaming, so I could transcribe in real-time as I speak.
- **Custom vocabulary**: For technical terms or names I use frequently, I could add some customization on top of that—something I need to explore.

But honestly, the current setup works great. It's fast, private, and simple. That's all I need.

If you're interested in local-first AI tools, give Kroko a try. The `GitHub repo <https://github.com/kroko-ai/>`_ has everything you need to get started. The community models are solid, and the ONNX runtime is well-optimized.

Local AI doesn't have to be complicated. Sometimes, a simple HTTP server and a good model are all you need to solve a real problem.
