# Documentación: Manejo de Imágenes en Base64

## Resumen
Las imágenes se almacenan en la base de datos como strings base64 para facilitar el transporte y almacenamiento. El módulo `imageUtils.py` proporciona utilidades para convertir entre formato binario y base64.

## Utilidades Disponibles

### ImageUtils.binary_to_base64(binary_data: bytes) -> str
Convierte datos binarios de imagen a string base64.

**Ejemplo:**
```python
from services.imageUtils import ImageUtils

# Leer una imagen desde archivo
with open('photo.jpg', 'rb') as f:
    binary_data = f.read()

# Convertir a base64
base64_string = ImageUtils.binary_to_base64(binary_data)
```

### ImageUtils.base64_to_binary(base64_string: str) -> bytes
Convierte string base64 a datos binarios. Automáticamente maneja el prefijo `data:image/...;base64,` si está presente.

**Ejemplo:**
```python
from services.imageUtils import ImageUtils

# Convertir base64 a binario
binary_data = ImageUtils.base64_to_binary(base64_string)

# Guardar como archivo
with open('output.jpg', 'wb') as f:
    f.write(binary_data)
```

### ImageUtils.validate_base64(base64_string: str) -> bool
Valida si un string es base64 válido.

**Ejemplo:**
```python
from services.imageUtils import ImageUtils

if ImageUtils.validate_base64(photo_string):
    print("String base64 válido")
else:
    print("String base64 inválido")
```

### ImageUtils.ensure_base64_prefix(base64_string: str, mime_type: str = "image/jpeg") -> str
Agrega el prefijo `data:image/...;base64,` si no existe.

**Ejemplo:**
```python
from services.imageUtils import ImageUtils

# Agregar prefijo para uso en HTML/frontend
photo_with_prefix = ImageUtils.ensure_base64_prefix(base64_string, "image/jpeg")
# Resultado: "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
```

## Integración con Database

### Guardar Worker con Foto
```python
from db.database import Database

# La foto puede ser string base64 o bytes
# Si es bytes, se convertirá automáticamente a base64
payload = {
    "name": "Juan Pérez",
    "document": "1234567890",
    "role": 1,
    "photo": base64_string  # o binary_data (bytes)
}

result = Database.create_worker(payload)
```

### Actualizar Worker con Foto
```python
from db.database import Database

payload = {
    "photo": new_base64_string  # o binary_data (bytes)
}

result = Database.update_worker(worker_id=1, payload=payload)
```

### Obtener Worker con Foto
```python
from db.database import Database

result = Database.get_worker(worker_id=1)
# result.data[0]['photo'] contiene el string base64
worker = result.data[0]
photo_base64 = worker['photo']
```

## Uso en el Frontend

El frontend puede usar las fotos directamente en elementos `<img>`:

```javascript
// Asumiendo que photo ya tiene el prefijo data:image/...;base64,
<img src={worker.photo} alt="Worker photo" />

// Si no tiene prefijo, agregarlo:
const photoSrc = worker.photo.startsWith('data:') 
    ? worker.photo 
    : `data:image/jpeg;base64,${worker.photo}`;
```

## Conversión al Recibir desde Frontend

Cuando el frontend envía una imagen (por ejemplo, desde un input file):

```javascript
// En el frontend
const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onloadend = () => {
        const base64String = reader.result; // Ya incluye prefijo data:image/...;base64,
        // Enviar al backend
        fetch('/workers/', {
            method: 'POST',
            body: JSON.stringify({
                name: "...",
                photo: base64String
            })
        });
    };
    
    reader.readAsDataURL(file);
};
```

El backend recibirá el string base64 con prefijo, y `ImageUtils.base64_to_binary()` lo manejará correctamente si es necesario convertirlo a binario.

## Notas Importantes

1. **Formato de almacenamiento**: Las fotos se almacenan en la DB como strings base64 (texto).

2. **Conversión automática**: Los métodos de `Database` y `WorkerManager` convierten automáticamente bytes a base64 antes de guardar.

3. **Prefijos data URI**: El método `base64_to_binary()` maneja automáticamente la remoción del prefijo `data:image/...;base64,`.

4. **Validación**: Use `validate_base64()` para verificar datos antes de procesarlos.

5. **Tamaño**: Las imágenes base64 son aproximadamente 33% más grandes que el binario equivalente. Considere comprimir imágenes grandes antes de codificarlas.
