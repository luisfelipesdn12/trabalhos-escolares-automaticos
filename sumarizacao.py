#!/usr/bin/env python
#
#   Python Script
#
#   Copyright © Juca Crispim
#
#   original source: https://goo.gl/NhfKET

import math
import nltk
import networkx as nx


class Texto:

    def __init__(self, raw_text):
        """
        ``raw_text`` é o text puro a ser resumido.
        """

        self.raw_text = raw_text
        self._sentences = None
        self._graph = None

    def resumir(self):
        """
        Aqui a gente extrai as frases com maior pontuação.
        O tamanho do resumo será 20% do número de frases original
        """
        # aqui definindo a quantidade de frases
        qtd = int(len(self.sentences) * 0.2) or 1

        # ordenando as frases de acordo com a pontuação
        # e extraindo a quantidade desejada.
        sentencas = sorted(
            self.sentences, key=lambda s: s.pontuacao, reverse=True)[:qtd]

        # ordenando as sentenças de acordo com a ordem no texto
        # original.
        ordenadas = sorted(sentencas, key=lambda s: self.sentences.index(s))

        return ' '.join([s.raw_text for s in ordenadas])

    @property
    def sentences(self):
        """
        Quebra o texto em sentenças utilizando o sentence tokenizer
        padrão do nltk.
        """

        if self._sentences is not None:
            return self._sentences

        # nltk.sent_tokenize é quem divide o texto em sentenças.
        self._sentences = [Sentenca(self, s)
                           for s in nltk.sent_tokenize(self.raw_text)]
        return self._sentences

    @property
    def graph(self):
        """
        Aqui cria o grafo, colocando as sentenças como nós as arestas
        (com peso) são criadas com base na semelhança entre sentenças.
        """

        if self._graph is not None:
            return self._graph

        graph = nx.Graph()
        # Aqui é o primeiro passo descrito acima. Estamos criando os
        # nós com as unidades de texto relevantes, no nosso caso as
        # sentenças.
        for s in self.sentences:
            graph.add_node(s)

        # Aqui é o segundo passo. Criamos as arestas do grafo
        # baseadas nas relações entre as unidades de texto, no nosso caso
        # é a semelhança entre sentenças.
        for node in graph.nodes():
            for n in graph.nodes():
                if node == n:
                    continue

                semelhanca = self._calculate_similarity(node, n)
                if semelhanca:
                    graph.add_edge(node, n, weight=semelhanca)

        self._graph = graph
        return self._graph

    def _calculate_similarity(self, sentence1, sentence2):
        """
        Implementação da fórmula de semelhança entre duas sentenças.
        """
        w1, w2 = set(sentence1.palavras), set(sentence2.palavras)

        # Aqui a gente vê quantas palavras que estão nas frases se
        # repetem.
        repeticao = len(w1.intersection(w2))
        # Aqui a normalização.
        semelhanca = repeticao / (math.log(len(w1)) + math.log(len(w2)))

        return semelhanca


class Sentenca:

    def __init__(self, texto, raw_text):
        """
        O parâmetro ``texto`` é uma instância de Texto.
        ``raw_text`` é o texto puro da sentença.
        """

        self.texto = texto
        self.raw_text = raw_text
        self._palavras = None
        self._pontuacao = None

    @property
    def palavras(self):
        """
        Quebrando as sentenças em palavras. As palavras
        da sentença serão usadas para calcular a semelhança.
        """
        if self._palavras is not None:
            return self._palavras

        # nltk.word_tokenize é quem divide a sentenças em palavras.
        self._palavras = nltk.word_tokenize(self.raw_text)
        return self._palavras

    @property
    def pontuacao(self):
        """
        Implementação do algorítimo simplificado para pontuação
        dos nós do grafo.
        """
        if self._pontuacao is not None:
            return self._pontuacao

        # aqui a gente simplesmente soma o peso das arestas
        # relacionadas a este nó.
        pontuacao = 0.0
        for n in self.texto.graph.neighbors(self):
            pontuacao += self.texto.graph.get_edge_data(self, n)['weight']

        self._pontuacao = pontuacao
        return self._pontuacao

    def __hash__(self):
        """
        Esse hash aqui é pra funcionar como nó no grafo.
        Os nós do NetworkX tem que ser 'hasheáveis'
        """
        return hash(self.raw_text)