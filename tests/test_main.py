from unittest.mock import patch, MagicMock
from src.main import enviar_mensagens_para_contatos


@patch("src.main.supabase_client")
@patch("src.main.requests.post")
def test_deve_enviar_mensagem_para_cada_contato(mock_post, mock_supabase):
    mock_table = MagicMock()
    mock_table.select.return_value.execute.return_value.data = [
        {"nome_contato": "Maria", "telefone": "5511988888888"},
        {"nome_contato": "João", "telefone": "5511977777777"},
    ]
    mock_supabase.table.return_value = mock_table

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    enviar_mensagens_para_contatos()

    assert mock_post.call_count == 2

    primeira_chamada = mock_post.call_args_list[0]
    assert primeira_chamada[0][0].startswith("https://api.z-api.io/instances/")
    payload = primeira_chamada[1]["json"]
    assert payload["message"] == "Olá Maria, tudo bem com você?"
    assert payload["phone"] == "5511988888888"
