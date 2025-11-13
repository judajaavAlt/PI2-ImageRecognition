import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Carga variables desde .env (solo necesario en local)
load_dotenv()


class SpeechService:
    """Servicio estático para síntesis
    y reconocimiento de voz con Azure Speech."""

    # --- Atributo de clase (compartido por todos los métodos) ---
    cliente = None

    @classmethod
    def configurar(cls):
        """Inicializa el cliente de Azure Speech si no está configurado."""
        if cls.cliente is not None:
            return  # Ya está configurado

        azure_key = os.getenv("AZURE_KEY")
        azure_url = os.getenv("AZURE_URL")

        if not azure_key or not azure_url:
            raise ValueError(
                "Las variables AZURE_KEY y AZURE_URL"
                "deben estar definidas en el entorno."
            )

        # Extrae la región del endpoint
        region = azure_url.split("//")[1].split(".")[0]

        # Configuración principal del servicio
        cls.cliente = speechsdk.SpeechConfig(
            subscription=azure_key, region=region
        )

        # Configuración global: voz y lenguaje
        cls.cliente.speech_synthesis_voice_name = "es-CO-GonzaloNeural"
        cls.cliente.speech_recognition_language = "es-CO"

        # Ajustamos el formato de salida a WAV
        cls.cliente.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )

    # --- Métodos de clase ---

    @classmethod
    def text_to_audio(cls, text: str) -> bytes:
        """Convierte texto a audio (WAV) y retorna binarios."""
        cls.configurar()

        if not text.strip():
            raise ValueError("El texto no puede estar vacío.")

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=cls.cliente, audio_config=None
        )
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            raise RuntimeError(
                f"Error en TTS: {result.cancellation_details.reason}, "
                f"{result.cancellation_details.error_details}"
            )
        else:
            raise RuntimeError("Error desconocido en la síntesis de voz.")

    @classmethod
    def audio_to_text(cls, audio_bytes: bytes) -> str:
        """Transcribe un audio (WAV) a texto."""
        cls.configurar()

        if not audio_bytes:
            raise ValueError("El archivo de audio está vacío.")

        temp_filename = "temp_audio.wav"
        try:
            with open(temp_filename, "wb") as f:
                f.write(audio_bytes)

            audio_input = speechsdk.AudioConfig(filename=temp_filename)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=cls.cliente, audio_config=audio_input
            )
            result = recognizer.recognize_once_async().get()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                raise RuntimeError(
                    "No se pudo reconocer el habla en el audio.")
            elif result.reason == speechsdk.ResultReason.Canceled:
                raise RuntimeError(
                    f"Error en STT:"
                    f"{result.cancellation_details.error_details}"
                )
            else:
                raise RuntimeError("Error desconocido en la transcripción.")
        finally:
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except PermissionError:
                    pass
