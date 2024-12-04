import requests

class DiscordNotifier:
    def __init__(self, webhook_url: str):
        """
        Inicializa el notificador de Discord con la URL del webhook.
        :param webhook_url: URL del webhook de Discord.
        """
        self.webhook_url = webhook_url

    def send_message(self, message: str, level: str = "info"):
        """
        Envía un mensaje al canal de Discord.
        :param message: Mensaje a enviar.
        :param level: Nivel del mensaje (info, success, error).
        """
        # Define colores para diferentes niveles
        colors = {
            "info": 3447003,  # Azul
            "success": 3066993,  # Verde
            "error": 15158332  # Rojo
        }

        # Construye el payload del mensaje
        payload = {
            "embeds": [
                {
                    "title": f"Notificación: {level.capitalize()}",
                    "description": message,
                    "color": colors.get(level, 3447003)  # Color por defecto: azul
                }
            ]
        }

        # Envía el mensaje al webhook de Discord
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar notificación a Discord: {str(e)}")

    def notify_success(self, message: str):
        """
        Envía un mensaje de éxito.
        :param message: Mensaje de éxito a enviar.
        """
        self.send_message(message, level="success")

    def notify_error(self, message: str):
        """
        Envía un mensaje de error.
        :param message: Mensaje de error a enviar.
        """
        self.send_message(message, level="error")

    def notify_info(self, message: str):
        """
        Envía un mensaje informativo.
        :param message: Mensaje informativo a enviar.
        """
        self.send_message(message, level="info")