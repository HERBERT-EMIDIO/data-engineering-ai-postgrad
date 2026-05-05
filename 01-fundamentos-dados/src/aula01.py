import logging
from pydantic import BaseModel, field_validator
from typing import List

# Configuração de Log Profissional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegistroPaciente(BaseModel):
    id: int
    nome: str
    setor: str

    @field_validator('setor')
    def validar_setor(cls, v):
        setores = ['UTI', 'Emergência', 'Radiologia']
        if v not in setores:
            raise ValueError('Setor inválido')
        return v

def processar_dados(dados: List[dict]):
    for item in dados:
        try:
            paciente = RegistroPaciente(**item)
            logger.info(f"Paciente {paciente.id} validado.")
        except Exception as e:
            logger.error(f"Erro no registro {item.get('id')}: {e}")

if __name__ == "__main__":
    dados_exemplo = [{"id": 1, "nome": "Herbert", "setor": "UTI"}]
    processar_dados(dados_exemplo)