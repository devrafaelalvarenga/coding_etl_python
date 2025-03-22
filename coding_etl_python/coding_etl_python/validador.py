from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import date
from enum import Enum
from decimal import Decimal
import math


class TipoDiaEnum(str, Enum):
    dia_util = "Dia útil"
    fim_de_semana = "Final de Semana"


class TipoAnuncioEnum(str, Enum):
    estatistico = "Estático"
    video = "Video"


class Anuncio(BaseModel):
    Organizador: int = Field(..., ge=0,
                             description="Número identificador do organizador da campanha.")
    Ano_Mes: str = Field(...,
                         description="Ano e mês da campanha no formato '2024 | Março'.")
    Dia_da_Semana: str = Field(
        ..., description="Nome do dia da semana em que a campanha foi realizada, como 'Sexta-Feira'.")
    Tipo_Dia: TipoDiaEnum = Field(
        ..., description="Tipo de dia (ex: 'Dia útil' ou 'Fim de semana').")
    Objetivo: str = Field(...,
                          description="Objetivo da campanha (ex: 'Leads').")
    Date: date = Field(...,
                       description="Data da campanha no formato 'YYYY-MM-DD'.")
    AdSet_name: str = Field(..., description="Nome do conjunto de anúncios.")
    Amount_spent: Decimal = Field(
        ..., gt=0, description="Valor gasto na campanha, com precisão de 2 casas decimais.", example=0.01)
    Link_clicks: Optional[int] = Field(
        None, ge=0, description="Número de cliques no link, opcional. Não pode ser negativo.", example=0)
    Impressions: int = Field(
        ..., ge=0, description="Número de impressões do anúncio, não pode ser negativo.")
    Conversions: Optional[int] = Field(
        None, description="Número de conversões, opcional. Não pode ser negativo.", example=0)
    Segmentação: str = Field(
        ..., description="Segmentação do público da campanha (ex: 'LookALike_Compradores_1').")
    Tipo_de_Anúncio: TipoAnuncioEnum = Field(
        ..., description="Tipo de anúncio, como 'Estático' ou 'Vídeo'.")
    Fase: str = Field(
        ..., description="Fase do lançamento da campanha (ex: '2º Lançamento | Leads').")

    # Pré-processamento de dados antes da validação do modelo
    # @model_validator(mode='before') é um decorador que indica que o método pre_process_data
    # deve ser executado antes da validação do modelo
    @model_validator(mode='before')
    # classmethod é um decorador que indica que o método pre_process_data é um método de classe
    @classmethod
    # método pre_process_data que realiza o pré-processamento dos dados antes da validação do modelo
    def pre_process_data(cls, data):
        if isinstance(data, dict):
            # Tratar Link_clicks
            if 'Link_clicks' in data and (data['Link_clicks'] is None or
                                          (isinstance(data['Link_clicks'], float) and math.isnan(data['Link_clicks']))):
                data['Link_clicks'] = None

            # Tratar Conversions
            if 'Conversions' in data and (data['Conversions'] is None or
                                          (isinstance(data['Conversions'], float) and math.isnan(data['Conversions']))):
                data['Conversions'] = None

            # Tratar Amount_spent - se for zero, definir como valor mínimo permitido
            if 'Amount_spent' in data and (data['Amount_spent'] == 0 or data['Amount_spent'] == 0.0):
                data['Amount_spent'] = Decimal(
                    '0.01')  # valor mínimo permitido

        return data
