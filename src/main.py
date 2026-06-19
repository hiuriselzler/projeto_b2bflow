import os
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client = (
    create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None
)


def _buscar_contatos():
    if not supabase_client:
        raise RuntimeError(
            "Supabase não configurado. Verifique SUPABASE_URL e SUPABASE_KEY."
        )
    logger.info("Buscando contatos no Supabase...")
    response = supabase_client.table("contatos").select("*").execute()
    contatos = response.data
    logger.info(f"{len(contatos)} contato(s) encontrado(s).")
    return contatos


def _enviar_mensagem_individual(telefone: str, nome: str):
    instance_id = os.getenv("ZAPI_INSTANCE_ID")
    token = os.getenv("ZAPI_TOKEN")
    if not instance_id or not token:
        raise RuntimeError(
            "Z-API não configurada. Verifique ZAPI_INSTANCE_ID e ZAPI_TOKEN."
        )

    url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-messages"
    mensagem = f"Olá, {nome} tudo bem com você?"
    payload = {"phone": telefone, "message": mensagem}
    headers = {"Content-Type": "application/json"}

    logger.debug(f"Enviando mensagem para {nome} ({telefone})...")
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    logger.info(f"Mensagem enviada com sucesso para {nome} ({telefone})")


def enviar_mensagens_para_contatos():
    contatos = _buscar_contatos()

    for contato in contatos:
        nome = contato.get("nome_contato", "cliente")
        telefone = contato.get("telefone")
        if not telefone:
            logger.warning(f"Contato '{nome}' não possui telefone. Ignorando.")
            continue
        try:
            _enviar_mensagem_individual(telefone, nome)
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede/API ao enviar para {nome} ({telefone}): {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar para {nome}: {e}")


if __name__ == "__main__":
    enviar_mensagens_para_contatos()
