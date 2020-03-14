# trabalhos-escolares-automaticos

Um programa que, a partir de um tema,  extrai conteúdo da Wikipedia, resume e adiciona imagens; depois formata e exporta um documento em formato de trabalho escolar.

---

## Ideia:

Digitar um tema e esperar. Depois de um tempo, ter em mãos um arquivo formatado com imagens e conteúdo resumido da Wikipedia. A ideia não é necessariamente ter o resultado final, mas ter algo próximo disso: algo que precisemos apenas fazer algumas alterações pequenas.

## Uso:

1. **Tenha Python** instalado;
2. **Clone ou baixe** o repositório;
3. Vá na pasta `requirements` e **clique em `install_all.bat`**; isso vai instalar todos os pacotes e bibliotecas necessárias e instalar o plugin `punkt` do módulo `nltk`.
4. **Execute o arquivo `main.py`** e digite o termo de pesquisa, e o percentual de resumo.
5. **Vá para a pasta `pesquisa`** criada automaticamente na pasta onde o script foi executado; leia e faça aperfeiçoamentos, se necessário na sua pesquisa automática :)

  **Algum problema ou sugestão?** Abra uma `issue`!

## Funcionamento:

> Nota: em aperfeiçoamento.



- O programa recolhe o **input** do usuário, contendo o tema da pesquisa;

- A partir desse input, faz a **pesquisa automática** na Wikipedia;

  > Usei a biblioteca `wikipedia` para extrair o conteúdo.

- Com o conteúdo dessa pesquisa, **limpa** espaços e conteúdos indesejados;

- Com o conteúdo limpo, **resume** o texto;

  > Utilizei, como base, uma gist de sumarização do GitHub, [clique aqui](https://gist.github.com/ryukinix/15e3381286177a3b41bd) para ver.

- Separa o conteúdo em parágrafos e **define palavras chave** para cada;

  > Para isso, usei um algoritmo de `Compreensão de Linguagem Natural` por inteligência artificial do `IBM Cloud/ Watson`, [clique aqui](https://cloud.ibm.com/catalog/services/natural-language-understanding) para ver.

- Faz o **download de imagens** com base em palavras-chave extraídas do resumo;

  > Usei a API do `Google Cloud Platform` chamada `Custom Search`, [clique aqui](https://developers.google.com/custom-search/docs/overview) para ver.

- Com todas as informações, formata um arquivo de texto com as imagens e o conteúdo;

- Gera e exporta o documento final.
