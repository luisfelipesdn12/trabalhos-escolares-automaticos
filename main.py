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
#para pegar URL da Google Images:
from googleapiclient.discovery import build
#credenciais:
from credentials import credentials


def retornaPequisa():
  '''
  Pergunta para o usuário
  o termo de pesquisa e
  retorna o input.
  '''
  return(str(input('Pequisa: ')))

def retornaPercentual():
  '''
  Pergunta para o usuário
  o percentual do resumo 
  e retorna o input.
  '''
  return(float(input('Percentual do resumo (0 a 1): ')))

def retornaWikiPage(pesquisa):
  '''
  A partir de um termo de pesquisa
  captura conteúdo da wikipedia e
  retorna uma estancia da página.
  '''
  print(f'CAPITURANDO CONTEÚDO DA WIKIPEDIA DE "{pesquisa}"...')
  page = wk.page(pesquisa)
  print('CONTEÚDO CAPTURADO :)')
  return(page)

def retornaConteudoLimpo(SourceContent):
  '''
  A partir do conteúdo, 
  limpa retirando o markdown 
  e as linhas vazias.
  '''
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

def retornaResumo(conteudo, percent):
  '''
  A partir do conteúdo limpo,
  resume em x por cento
  e retorna o resumo.
  '''
  print('RESUMINDO CONTEÚDO...')
  t = sumarizacao.Texto(conteudo)
  resumo = t.resumir(percent = percent)
  print('CONTEÚDO RESUMIDO :)')
  return(resumo)

def separaERetornaParagrafos(resumo):
  '''
  A partir do resumo, separa
  e retorna uma lista de
  parágrafos.
  '''
  print('SEPARANDO PARÁGRAFOS...')
  paragrafos = resumo.split('##PARAGRAFO##')

  for paragrafo in paragrafos:
    if paragrafo in ('', ' ', '  ', '\n', None):
      paragrafos.remove(paragrafo)

  print('PARAGRAFOS SEPARADOS :)')
  return(paragrafos)

def retornaIBMAuth():
  '''
  Autentica a API da IBM Cloud/
  Watson, e retorna uma estância
  autenticada.
  '''
  #AUTENTICA:
  print('AUTENTICANDO O IBM WATSON...')
  authenticator = IAMAuthenticator(credentials['IBM'])
  print('IBM WATSON AUTENTICADO :)')
  return(authenticator)

def retornaKeyword(paragrafo, authenticator):
  '''
  Para cada parágrafo, analisa e
  estabelece palavras-chave,
  que serão usadas para a procura
  de imagens.
  (Tem uma nota de corte baseada na
  relevância da palavra-chave, se
  a relevância for menor, retorna None)
  '''
  natural_language_understanding = NaturalLanguageUnderstandingV1(
      version='2019-07-12',
      authenticator=authenticator
  )
  natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/99046149-caff-413c-b9c4-12866481c76f')
  #USA:
  print(f'ANALISANDO TEXTO E EXTRAINDO PALAVRAS CHAVE DE "{paragrafo[:20]}..." ...')
  response = natural_language_understanding.analyze(
  text= paragrafo,
  features=Features(
        keywords=KeywordsOptions(limit=1))).get_result()

  keywords = response['keywords']

  print('TEXTO ANALIZADO E PALAVRAS CHAVE EXTRAIDAS :)')
  if keywords[0]['relevance'] >= 0.76:
    return(keywords[0])
  else: return(None)

def retornaImagem(pesquisa):
  '''
  Busca no Google Images e
  retorna URLs de imagens
  baseada em uma pesquisa
  (nesse caso, a palavra-chave).
  Retorna None se der algum erro
  na busca, como por exemplo:
  a cota diária da API se esgotou.
  '''
  print(f'PROCURANDO IMAGENS NO GOOGLE DE "{pesquisa}"...')
  my_api_key = credentials['GCP']['my_api_key']
  my_cse_id = credentials['GCP']['my_cse_id']

  def google_search(search_term, api_key, cse_id, **kwargs):
      service = build("customsearch", "v1", developerKey=api_key)
      res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
      return res['items']

  try:
    results = google_search(
        pesquisa,
        my_api_key,
        my_cse_id,
        num=2,
        searchType = 'image',
        filter = '1',
        safe = 'active',
        imgSize = 'large') 

    imagens = list()
    for result in results:
        imagens.append(results[0]['link'])
    print('IMAGENS ACHADAS :)')
    return(imagens)
  
  except: return(None)



def retornaParagrafosEInfos(pesquisa, paragrafos_separados, authenticator):
  '''
  Define e retorna uma lista
  de dicionários contendo os
  parágrafos e informações como
  palavra-chave e imagens.
  '''
  paragrafos_e_infos = list()

  for paragrafo in paragrafos_separados:
    infos = dict()
    infos['text'] = paragrafo
    try: infos['keyword'] = retornaKeyword(paragrafo, authenticator)['text']
    except TypeError: infos['keyword'] = None
    if infos['keyword'] != None:
      if pesquisa != infos['keyword']:
        infos['image'] = retornaImagem(pesquisa + ' ' + infos['keyword'])
      else: infos['image'] = retornaImagem(infos['keyword'])
    else: infos['image'] = None
    paragrafos_e_infos.append(infos)

  return(paragrafos_e_infos)

def formataERetornaTexto(pesquisa, paragrafos_e_infos):
  '''
  Formata, em markdown, 
  o texto final.
  '''
  print('FORMATANDO PESQUISA...')
  texto = list()
  texto.append(f'# Pesquisa sobre: {pesquisa}')
  texto.append('> Pesquisa feita automáticamente por [trabalhos-escolares-automaticos](https://github.com/luisfelipesdn12/trabalhos-escolares-automaticos). :) \n\n')
  
  for paragrafo in paragrafos_e_infos:
    texto.append(paragrafo['text'])
    if paragrafo['image'] != None:
      texto.append(f'> ![{paragrafo["keyword"]}]({paragrafo["image"][0]})')

  print('PESQUISA FORMATADA :)')

  texto_final = '\n\n  '.join(texto)
  return(texto_final)

def exportaArquivo(pesquisa, texto):
  '''
  Cria o aquivo final na pasta
  './pesquisas', nomeado como:
  "Termo da Pesquisa_pesquisa.md".
  '''
  print(f'EXPORTANDO O ARQUIVO "{pesquisa}_pesquisa.md" ...')

  try:
    import os
    os.mkdir(r'.\pesquisas')
  except FileExistsError: pass
    
  file = open(f'.\pesquisas\{pesquisa}_pesquisa.md', 'w+', encoding="utf-8")
  file.write(texto)
  file.close()

  print(f'ARQUIVO "{pesquisa}_pesquisa.md" EXPORTADO :)')
  

def main():
  '''
  Orquestrador.
  '''
  pesquisa = retornaPequisa()

  percent = retornaPercentual()

  page = retornaWikiPage(pesquisa)

  conteudo_limpo = retornaConteudoLimpo(page.content)

  resumo = retornaResumo(conteudo_limpo, percent)

  paragrafos_separados = separaERetornaParagrafos(resumo)

  authenticator = retornaIBMAuth()

  paragrafos_e_infos = retornaParagrafosEInfos(pesquisa, paragrafos_separados, authenticator)

  texto = formataERetornaTexto(pesquisa, paragrafos_e_infos)

  exportaArquivo(pesquisa, texto)

  from pprint import pprint
  pprint(paragrafos_e_infos)

main()
