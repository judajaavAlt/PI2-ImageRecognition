import pytest
import io
from unittest.mock import patch, MagicMock
from app.services.speechService import SpeechService


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    """Mock de variables de entorno para Azure Speech."""
    monkeypatch.setenv("AZURE_KEY", "fake_key")
    monkeypatch.setenv(
        "AZURE_URL", "https://fake-region.api.cognitive.microsoft.com/")
    # Reinicia la configuración del cliente entre tests
    SpeechService.cliente = None


# --- Pruebas de text_to_audio ---

@patch("app.services.speechService.speechsdk")
def test_text_to_audio_devuelve_binarios(mock_speechsdk):
    """Debe devolver binarios cuando se convierte texto a audio."""
    mock_audio_data = b"FAKEAUDIOBYTES"

    # Mock de ResultReason
    mock_speechsdk.ResultReason.SynthesizingAudioCompleted = "OK"

    # Simula el resultado del sintetizador
    mock_result = MagicMock()
    mock_result.reason = "OK"
    mock_result.audio_data = mock_audio_data

    synth = mock_speechsdk.SpeechSynthesizer.return_value
    speak_future = synth.speak_text_async.return_value
    speak_future.get.return_value = mock_result

    output = SpeechService.text_to_audio("Hola mundo")

    assert isinstance(output, bytes)
    assert output == mock_audio_data


@patch("app.services.speechService.speechsdk")
def test_text_to_audio_lanza_excepcion_si_falla(mock_speechsdk):
    """Debe lanzar excepción si el SDK devuelve error."""
    mock_speechsdk.ResultReason.SynthesizingAudioCompleted = "OK"
    mock_speechsdk.ResultReason.Canceled = "CANCEL"

    mock_result = MagicMock()
    mock_result.reason = "CANCEL"
    mock_result.cancellation_details.reason = "Fallo"
    mock_result.cancellation_details.error_details = "Error de prueba"

    synth = mock_speechsdk.SpeechSynthesizer.return_value
    speak_future = synth.speak_text_async.return_value
    speak_future.get.return_value = mock_result

    with pytest.raises(RuntimeError):
        SpeechService.text_to_audio("Error forzado")


# --- Pruebas de audio_to_text ---

@patch("app.services.speechService.speechsdk")
def test_audio_to_text_retorna_texto(mock_speechsdk):
    """Debe retornar texto cuando el audio se transcribe correctamente."""
    mock_speechsdk.ResultReason.RecognizedSpeech = "OK"

    mock_result = MagicMock()
    mock_result.reason = "OK"
    mock_result.text = "Hola mundo"

    recognizer = mock_speechsdk.SpeechRecognizer.return_value
    recognize_future = recognizer.recognize_once_async.return_value
    recognize_future.get.return_value = mock_result

    fake_audio = io.BytesIO(b"FakeWavData")
    output = SpeechService.audio_to_text(fake_audio.read())

    assert isinstance(output, str)
    assert output == "Hola mundo"


@patch("app.services.speechService.speechsdk")
def test_audio_to_text_lanza_excepcion_si_falla(mock_speechsdk):
    """Debe lanzar excepción si el reconocimiento falla."""
    mock_speechsdk.ResultReason.RecognizedSpeech = "OK"
    mock_speechsdk.ResultReason.NoMatch = "FAIL"

    mock_result = MagicMock()
    mock_result.reason = "FAIL"

    recognizer = mock_speechsdk.SpeechRecognizer.return_value
    recognize_future = recognizer.recognize_once_async.return_value
    recognize_future.get.return_value = mock_result

    fake_audio = io.BytesIO(b"FakeData")
    with pytest.raises(RuntimeError):
        SpeechService.audio_to_text(fake_audio.read())


# --- Prueba adicional: variables de entorno faltantes ---

def test_configurar_lanza_error_sin_variables(monkeypatch):
    """Debe lanzar ValueError si faltan las variables AZURE_KEY o AZURE_URL."""
    monkeypatch.delenv("AZURE_KEY", raising=False)
    monkeypatch.delenv("AZURE_URL", raising=False)
    SpeechService.cliente = None

    with pytest.raises(ValueError):
        SpeechService.configurar()
