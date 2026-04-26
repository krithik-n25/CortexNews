import time
from twilio.rest import Client
from app.core.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, TWILIO_WHATSAPP_TO
from app.core.logger import get_logger

logger = get_logger(__name__)

MAX_MESSAGE_LENGTH = 1500  # Keep under Twilio's 1600 char limit with some buffer

def _split_message(body: str) -> list[str]:
    """Split a long message into chunks that fit within Twilio's character limit.
    Splits at double-newlines (between insights) to keep formatting clean."""
    
    if len(body) <= MAX_MESSAGE_LENGTH:
        return [body]

    chunks = []
    sections = body.split("\n\n")
    current_chunk = ""

    for section in sections:
        # If adding this section would exceed the limit, save current chunk and start new one
        if current_chunk and len(current_chunk) + len(section) + 2 > MAX_MESSAGE_LENGTH:
            chunks.append(current_chunk.strip())
            current_chunk = section
        else:
            current_chunk = current_chunk + "\n\n" + section if current_chunk else section

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def send_message(body: str) -> bool:
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.error("Twilio credentials not found. Cannot send WhatsApp message.")
        return False
        
    if not TWILIO_WHATSAPP_FROM or not TWILIO_WHATSAPP_TO:
        logger.error("Twilio phone numbers not found. Cannot send WhatsApp message.")
        return False

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        chunks = _split_message(body)
        
        logger.info(f"Message split into {len(chunks)} part(s). Sending to {len(TWILIO_WHATSAPP_TO)} recipient(s).")
        
        for recipient in TWILIO_WHATSAPP_TO:
            logger.info(f"Sending to {recipient}...")
            for i, chunk in enumerate(chunks):
                message = client.messages.create(
                    body=chunk,
                    from_=TWILIO_WHATSAPP_FROM,
                    to=recipient
                )
                logger.info(f"  Part {i+1}/{len(chunks)} sent. SID: {message.sid}")
                
                # Small delay between messages to maintain order
                if i < len(chunks) - 1:
                    time.sleep(1)
            
            logger.info(f"All parts sent to {recipient}.")
        
        logger.info("All WhatsApp messages sent successfully to all recipients.")
        return True
    except Exception as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
        return False
