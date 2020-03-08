# coding: UTF-8

#para webscrapping da wikipedia:
import wikipedia as wk
wk.set_lang('pt')
#para resumo:
import sumarizacao
#para análise de linguagem natural:
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def retornaPequisa():
  return(str(input('Pequisa: ')))

def retornaWikiPage(pesquisa):
  print('CAPITURANDO CONTEÚDO DA WIKIPEDIA...')
  page = wk.page(pesquisa)
  print('CONTEÚDO CAPTURADO :)')
  return(page)

def retornaConteudoLimpo(SourceContent):
    print('LIMPANDO CONTEÚDO...')
    linhas = SourceContent.split('\n')

    linhas_limpas = []

    for linha in linhas:
        #FILTRA E REMOVE LINHAS VAZIAS E COM == MARKDOWN ==
        if linha == '':
            pass
        elif linha[:2] == '==' and linha[-2:] == "==":
            linhas_limpas.append('##PARAGRAFO##')
        else: linhas_limpas.append(linha)

    conteudoLimpo = '\n'.join(linhas_limpas)

    print('CONTEÚDO LIMPO :)')
    return(conteudoLimpo)

def retornaResumo(conteudo):
  print('RESUMINDO CONTEÚDO...')
  t = sumarizacao.Texto(conteudo)
  resumo = t.resumir()
  print('CONTEÚDO RESUMIDO :)')
  return(resumo)

def separaERetornaParagrafos(resumo):
  print('SEPARANDO PARÁGRAFOS...')
  paragrafos = resumo.split('##PARAGRAFO##')

  for paragrafo in paragrafos:
    if paragrafo in ('', ' ', '  ', '\n', None):
      paragrafos.remove(paragrafo)

  print('PARAGRAFOS SEPARADOS :)')
  return(paragrafos)

def retornaIBMAuth():
  #AUTENTICA:
  print('AUTENTICANDO O IBM WATSON...')
  authenticator = IAMAuthenticator('XHxEsN5LiOhXMv68KMVVHXiOoyjuExT-Jft1HNhpv9X4')
  print('IBM WATSON AUTENTICADO :)')
  return(authenticator)

def retornaKeyword(paragrafo, authenticator):
  natural_language_understanding = NaturalLanguageUnderstandingV1(
      version='2019-07-12',
      authenticator=authenticator
  )
  natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/99046149-caff-413c-b9c4-12866481c76f')
  #USA:
  print("ANALISANDO TEXTO E EXTRAINDO PALAVRAS CHAVE...")
  response = natural_language_understanding.analyze(
  text= paragrafo,
  features=Features(
        keywords=KeywordsOptions(limit=1))).get_result()

  keywords = response['keywords']

  print('TEXTO ANALIZADO E PALAVRAS CHAVE EXTRAIDAS :)')
  if keywords[0]['relevance'] >= 0.76:
    return(keywords[0])
  else: return(None)

def retornaParagrafosEInfos(paragrafos_separados, authenticator):
  paragrafos_e_infos = list()

  for paragrafo in paragrafos_separados:
    infos = dict()
    infos['text'] = paragrafo
    try: infos['keyword'] = retornaKeyword(paragrafo, authenticator)['text']
    except TypeError: infos['keywords'] = None
    infos['image'] = None #Por enquanto
    paragrafos_e_infos.append(infos)

  return(paragrafos_e_infos)
  

def main():
  #pesquisa = retornaPequisa()
  pesquisa = 'Michael Jackson'

  page = retornaWikiPage(pesquisa)

  conteudo_limpo = retornaConteudoLimpo(page.content)

  resumo = retornaResumo(conteudo_limpo)

  paragrafos_separados = separaERetornaParagrafos(resumo)

  authenticator = retornaIBMAuth()

  paragrafos_e_infos = retornaParagrafosEInfos(paragrafos_separados, authenticator)

  for pei in paragrafos_e_infos:
    print(f'\n\{pei}n')

main()
