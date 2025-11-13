import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Carga variables desde .env (solo necesario en local)
load_dotenv()


class SpeechService:
    def __init__(self):
        """Inicializa el cliente de Azure Speech
        usando las variables de entorno."""
        azure_key = os.getenv("AZURE_KEY")
        azure_url = os.getenv("AZURE_URL")

        if not azure_key or not azure_url:
            raise ValueError(
                "Las variables AZURE_KEY y AZURE_URL"
                "deben estar definidas en el entorno.")

        # Extrae la región del endpoint
        region = azure_url.split("//")[1].split(".")[0]

        # Configuración principal del servicio
        self.cliente = speechsdk.SpeechConfig(
            subscription=azure_key, region=region)

        # Configuración global
        # Voz masculina en español colombiano
        # Idioma de reconocimiento
        self.cliente.speech_synthesis_voice_name = "es-CO-GonzaloNeural"
        self.cliente.speech_recognition_language = "es-CO"

        # Ajustamos el formato de salida a WAV
        self.cliente.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
        )

    def text_to_audio(self, text: str) -> bytes:
        """Convierte un texto en audio (WAV) y retorna los binarios."""
        if not text.strip():
            raise ValueError("El texto no puede estar vacío.")

        # Creamos el sintetizador con salida en memoria
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.cliente, audio_config=None)
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            raise RuntimeError(
                f"Error en TTS: {cancellation_details.reason},"
                f"{cancellation_details.error_details}")
        else:
            raise RuntimeError("Error desconocido en la síntesis de voz.")

    def audio_to_text(self, audio_bytes: bytes) -> str:
        """Transcribe un audio (binario WAV) a texto."""
        if not audio_bytes:
            raise ValueError("El archivo de audio está vacío.")

        # Guardamos temporalmente el audio en un archivo WAV
        #   (Azure SDK requiere un path)
        temp_filename = "temp_audio.wav"
        try:
            with open(temp_filename, "wb") as f:
                f.write(audio_bytes)

            audio_input = speechsdk.AudioConfig(filename=temp_filename)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.cliente,
                audio_config=audio_input
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
                    f"{result.cancellation_details.error_details}")
            else:
                raise RuntimeError("Error desconocido en la transcripción.")
        finally:
            # Elimina el archivo temporal
            if os.path.exists(temp_filename):
                try:
                    os.remove(temp_filename)
                except PermissionError:
                    # Windows puede mantener el archivo bloqueado brevemente;
                    # lo ignoramos
                    pass
