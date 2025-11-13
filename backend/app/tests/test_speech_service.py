import pytest
import io
from unittest.mock import patch, MagicMock
from app.services.speechService import SpeechService


@pytest.fixture
def service():
    """Instancia del servicio con valores mockeados."""
    return SpeechService()


# --- Pruebas de text_to_audio ---

@patch("app.services.speechService.speechsdk")
def test_text_to_audio_devuelve_binarios(mock_speechsdk, service):
    """Debe devolver binarios cuando se convierte texto a audio."""
    mock_audio_data = b"FAKEAUDIOBYTES"

    # Configuramos el mock de ResultReason
    mock_speechsdk.ResultReason.SynthesizingAudioCompleted = "OK"

    # Simulamos el resultado del sintetizador
    mock_result = MagicMock()
    mock_result.reason = "OK"
    mock_result.audio_data = mock_audio_data

    # Mock del sintetizador y su método
    mock_speechsdk.SpeechSynthesizer.return_value.speak_text_async.return_value.get.return_value = mock_result

    output = service.text_to_audio("Hola mundo")

    assert isinstance(output, bytes)
    assert output == mock_audio_data


@patch("app.services.speechService.speechsdk.SpeechSynthesizer")
def test_text_to_audio_lanza_excepcion_si_falla(mock_synthesizer, service):
    """Debe lanzar excepción si el SDK devuelve error."""
    mock_result = MagicMock()
    mock_result.reason = 1  # Simulamos fallo
    mock_synthesizer.return_value.speak_text.return_value = mock_result

    with pytest.raises(Exception):
        service.text_to_audio("Error forzado")


# --- Pruebas de audio_to_text ---

@patch("app.services.speechService.speechsdk")
def test_audio_to_text_retorna_texto(mock_speechsdk, service):
    """Debe retornar texto cuando el audio se transcribe correctamente."""
    # Simulamos la constante usada en el código
    mock_speechsdk.ResultReason.RecognizedSpeech = "OK"

    mock_result = MagicMock()
    mock_result.reason = "OK"
    mock_result.text = "Hola mundo"

    # Simulamos la llamada asíncrona .recognize_once_async().get()
    mock_speechsdk.SpeechRecognizer.return_value.recognize_once_async.return_value.get.return_value = mock_result

    fake_audio = io.BytesIO(b"FakeWavData")
    output = service.audio_to_text(fake_audio.read())

    assert isinstance(output, str)
    assert output == "Hola mundo"


@patch("app.services.speechService.speechsdk.SpeechRecognizer")
def test_audio_to_text_lanza_excepcion_si_falla(mock_recognizer, service):
    """Debe lanzar excepción si el reconocimiento falla."""
    mock_result = MagicMock()
    mock_result.reason = 1
    mock_recognizer.return_value.recognize_once.return_value = mock_result

    fake_audio = io.BytesIO(b"FakeData")
    with pytest.raises(Exception):
        service.audio_to_text(fake_audio.read())
