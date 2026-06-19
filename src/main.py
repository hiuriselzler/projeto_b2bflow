import os
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client = (
    create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None
)


def enviar_mensagens_para_contatos():
    if not supabase_client:
        raise RuntimeError("Supabase não configurado.")

    response = supabase_client.table("contatos").select("*").execute()
    contatos = response.data

    instance_id = os.getenv("ZAPI_INSTANCE_ID")
    token = os.getenv("ZAPI_TOKEN")
    url_base = (
        f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-messages"
    )

    for contato in contatos:
        nome = contato.get("nome_contato", "cliente")
        telefone = contato.get("telefone")
        if not telefone:
            continue

        mensagem = f"Olá, {nome} tudo bem com você?"
        payload = {"phone": telefone, "message": mensagem}
        headers = {"Content-Type": "application/json"}

        try:
            resp = requests.post(url_base, json=payload, headers=headers)
            resp.raise_for_status()
        except Exception as e:
            print(f"Erro ao enviar para {nome}: {e}")
