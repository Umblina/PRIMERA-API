import httpx  # Importo la librería httpx para hacer solicitudes HTTP asíncronas

API_KEY = "78a1ba408aa89a812e7625ba"  # Esta es la API key que me dio ExchangeRate-API

async def obtener_tasa_cambio(moneda_origen: str, moneda_destino: str) -> float:  # Defino una función asincrónica que recibe las monedas
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{moneda_origen}/{moneda_destino}"  # Construyo la URL para obtener la tasa de cambio entre dos monedas

    async with httpx.AsyncClient() as client:  # Creo un cliente HTTP asíncrono
        response = await client.get(url)  # Hago la solicitud a la API
        print("Respuesta cruda:", response.text)  # Imprimo la respuesta tal cual para verificar que esté bien
        data = response.json()  # Convierto la respuesta en un diccionario (JSON)

    if response.status_code == 200 and data.get("result") == "success":  # Verifico que la respuesta haya sido exitosa
        return data["conversion_rate"]  # Si todo está bien, devuelvo la tasa de conversión
    
    return None  # Si algo falla, devuelvo None para manejar el error después
