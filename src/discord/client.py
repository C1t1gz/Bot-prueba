"""
Cliente de Discord para el bot
"""

import discord
from src.core.chat import chat, mensaje_ayuda, tirar_dados, girar_ruleta, lanzar_moneda

class Timbero(discord.Client):
    """
    Cliente de Discord que maneja las interacciones del bot.
    """
    
    async def on_ready(self):
        """Evento que se ejecuta cuando el bot se conecta exitosamente."""
        print(f'✅ Bot conectado como {self.user}!')
        print(f'🆔 ID del bot: {self.user.id}')
        print(f'📊 Servidores conectados: {len(self.guilds)}')

    async def on_message(self, message):
        """
        Maneja los mensajes recibidos en Discord.
        
        Args:
            message: Objeto mensaje de Discord
        """
        # Ignorar mensajes del propio bot
        if message.author == self.user:
            return
            
        # Manejar comandos específicos
        if message.content.startswith("!help"): 
            await message.channel.send(mensaje_ayuda())
        elif message.content.startswith("!dados"):
            await message.channel.send(tirar_dados())
        elif message.content.startswith("!ruleta"):
            await message.channel.send(girar_ruleta())
        elif message.content.startswith("!coinflip"):
            await message.channel.send(lanzar_moneda())
        else:
            # Procesar mensaje con el sistema de chat
            try:
                response = chat(
                    message.content, 
                    user_id=str(message.author.id), 
                    roles=[role.name for role in getattr(message.author, 'roles', [])]
                )
                await message.channel.send(response)
            except Exception as e:
                print(f"❌ Error procesando mensaje: {e}")
                await message.channel.send("❌ Lo siento, hubo un error procesando tu mensaje.")
