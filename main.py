import wikipedia as wk #para webscrapping da wikipedia

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
print(page.content)
