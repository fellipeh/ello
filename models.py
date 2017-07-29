import os.path
from peewee import *

db = SqliteDatabase('senado.db')


class BaseModel(Model):
    class Meta:
        database = db


class Exercicio(BaseModel):
    CodigoExercicio = IntegerField(null=True)
    DataInicio = CharField(null=True)
    DataFim = CharField(null=True)
    SiglaCausaAfastamento = CharField(null=True)
    DescricaoCausaAfastamento = CharField(null=True)


class Suplente(BaseModel):
    CodigoParlamentar = IntegerField(null=True)
    NomeParlamentar = CharField(null=True)
    DescricaoParticipacao = CharField(null=True)


class Mandato(BaseModel):
    CodigoMandato = IntegerField(null=True)
    NomeParlamentar = CharField(null=True)
    UfParlamentar = CharField(null=True)
    Mandado1_NumeroLegislatura = IntegerField(null=True)
    Mandado1_DataInicio = CharField(null=True)
    Mandado1_DataFim = CharField(null=True)
    Mandado2_NumeroLegislatura = IntegerField(null=True)
    Mandado2_DataInicio = CharField(null=True)
    Mandado2_DataFim = CharField(null=True)
    DescricaoParticipacao = CharField(null=True)


class RelMandatoSuplente(BaseModel):
    mandato = ForeignKeyField(Mandato, related_name='mandato_sup')
    suplente = ForeignKeyField(Suplente, related_name='suplente')

    class Meta:
        indexes = (
            (('mandato', 'suplente'), True),
        )


class RelMandatoExercicio(BaseModel):
    mandato = ForeignKeyField(Mandato, related_name='mandato_ex')
    exercicio = ForeignKeyField(Exercicio, related_name='exercicio')

    class Meta:
        indexes = (
            (('mandato', 'exercicio'), True),
        )


class Parlamentar(BaseModel):
    CodigoParlamentar = IntegerField(null=True)
    NomeParlamentar = CharField(null=True)
    NomeCompletoParlamentar = CharField(null=True)
    SexoParlamentar = CharField(null=True)
    FormaTratamento = CharField(null=True)
    UrlFotoParlamentar = CharField(null=True)
    UrlPaginaParlamentar = CharField(null=True)
    EmailParlamentar = CharField(null=True)
    SiglaPartidoParlamentar = CharField(null=True)
    UfParlamentar = CharField(null=True)


class RelParlamentarMandato(BaseModel):
    parlamentar = ForeignKeyField(Mandato, related_name='parlamentar')
    mandato = ForeignKeyField(Mandato, related_name='mandato_par')

    class Meta:
        indexes = (
            (('parlamentar', 'mandato'), True),
        )


def create_tables(null=True):
    if os.path.exists('senado.db'):
        os.remove('senado.db')
    db.connect()
    db.create_tables(
        [Exercicio, Suplente, Mandato, RelMandatoSuplente, RelMandatoExercicio, Parlamentar, RelParlamentarMandato])
