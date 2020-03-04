import wikipedia as wk #para webscrapping da wikipedia
from collections import defaultdict
import sumarizacao

wk.set_lang('pt')
userInput = dict()

def retornaPequisa():
  return(str(input('Pequisa: ')))

def retornaPrefixo():
  return(str(input('Prefixo: ')))

def retornaWikiPage(pesquisa):
  page = wk.page(pesquisa)

  return(page)

userInput['pesquisa'] = retornaPequisa()
userInput['prefixo'] = retornaPrefixo()
page = retornaWikiPage(userInput['pesquisa'])

print('Título:', userInput['prefixo'], userInput['pesquisa'])

t = sumarizacao.Texto(page.summary)
resumo = t.resumir()

print('\n---\nSumário da Wikipedia:\n\n', page.summary)
print('\n---\nSumário da Wikipedia RESUMIDO AUTOMÁTICAMENTE:\n\n', resumo)