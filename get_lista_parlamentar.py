import requests
import json

from models import *

DEFAULT_URL = 'http://legis.senado.gov.br/dadosabertos/senador/lista/atual'
DEFAULT_HEADERS = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

print('Creating table...')
create_tables()

print('Request API data...')

#######
# Using API Request
####
# r = requests.get(url=DEFAULT_URL, headers=DEFAULT_HEADERS)
# return_json = json.loads(r.content)

#######
# Using JSON
####
with open('senadores.json') as json_data:
    return_json = json.load(json_data)

for row in return_json['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']:
    print('Add %s into database' % row['IdentificacaoParlamentar']['NomeParlamentar'])

    with db.transaction():
        parlamentar = Parlamentar.create(
            CodigoParlamentar=row['IdentificacaoParlamentar']['CodigoParlamentar'],
            NomeParlamentar=row['IdentificacaoParlamentar']['NomeParlamentar'],
            NomeCompletoParlamentar=row['IdentificacaoParlamentar']['NomeCompletoParlamentar'],
            SexoParlamentar=row['IdentificacaoParlamentar']['SexoParlamentar'],
            FormaTratamento=row['IdentificacaoParlamentar']['FormaTratamento'],
            UrlFotoParlamentar=row['IdentificacaoParlamentar']['UrlFotoParlamentar'],
            UrlPaginaParlamentar=row['IdentificacaoParlamentar']['UrlPaginaParlamentar'],
            EmailParlamentar=row['IdentificacaoParlamentar']['EmailParlamentar'],
            SiglaPartidoParlamentar=row['IdentificacaoParlamentar']['SiglaPartidoParlamentar'],
            UfParlamentar=row['IdentificacaoParlamentar']['UfParlamentar']
        )
        parlamentar.save()

        mandato = Mandato.create(
            CodigoMandato=row['Mandato']['CodigoMandato'],
            NomeParlamentar=row['Mandato']['CodigoMandato'],
            UfParlamentar=row['Mandato']['CodigoMandato'],
            Mandado1_NumeroLegislatura=row['Mandato']['CodigoMandato'],
            Mandado1_DataInicio=row['Mandato']['CodigoMandato'],
            Mandado1_DataFim=row['Mandato']['CodigoMandato'],
            Mandado2_NumeroLegislatura=row['Mandato']['CodigoMandato'],
            Mandado2_DataInicio=row['Mandato']['CodigoMandato'],
            Mandado2_DataFim=row['Mandato']['CodigoMandato'],
            DescricaoParticipacao=row['Mandato']['CodigoMandato']
        )
        mandato.save()

        lista_suplentes = row.get('Mandato').get('Suplentes').get('Suplente')
        if lista_suplentes:
            if isinstance(lista_suplentes, list):
                for s in lista_suplentes:
                    suplente = Suplente.create(
                        CodigoParlamentar=s.get('CodigoParlamentar'),
                        NomeParlamentar=s['NomeParlamentar'],
                        DescricaoParticipacao=s['DescricaoParticipacao']
                    )
                    suplente.save()

                    relmandato_suplente = RelMandatoSuplente.create(mandato=mandato, suplente=suplente)
                    relmandato_suplente.save()
            else:
                suplente = Suplente.create(
                    CodigoParlamentar=s.get('CodigoParlamentar'),
                    NomeParlamentar=s['NomeParlamentar'],
                    DescricaoParticipacao=s['DescricaoParticipacao']
                )
                suplente.save()

                relmandato_suplente = RelMandatoSuplente.create(mandato=mandato, suplente=suplente)
                relmandato_suplente.save()

        lista_exercicios = row.get('Mandato').get('Exercicios').get('Exercicio')
        if lista_exercicios:
            if isinstance(lista_exercicios, list):
                for e in row['Mandato']['Exercicios']['Exercicio']:
                    exercicio = Exercicio.create(
                        CodigoExercicio=e.get('CodigoExercicio'),
                        DataInicio=e.get('DataInicio'),
                        DataFim=e.get('DataFim'),
                        SiglaCausaAfastamento=e.get('SiglaCausaAfastamento'),
                        DescricaoCausaAfastamento=e.get('DescricaoCausaAfastamento')
                    )
                    exercicio.save()

                    relmandato_exercicio = RelMandatoExercicio.create(mandato=mandato, exercicio=exercicio)
                    relmandato_exercicio.save()
            else:
                exercicio = Exercicio.create(
                    CodigoExercicio=e.get('CodigoExercicio'),
                    DataInicio=e.get('DataInicio'),
                    DataFim=e.get('DataFim'),
                    SiglaCausaAfastamento=e.get('SiglaCausaAfastamento'),
                    DescricaoCausaAfastamento=e.get('DescricaoCausaAfastamento')
                )
                exercicio.save()

                relmandato_exercicio = RelMandatoExercicio.create(mandato=mandato, exercicio=exercicio)
                relmandato_exercicio.save()

    db.commit()

print('Finished')
