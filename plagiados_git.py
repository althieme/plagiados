""" Detecção de plágio
Fazer uma versão para vários arquivos. Configurar primeiro os arquivos.
André L Thieme """
from duckduckgo_search import DDGS
import requests
import os
from itertools import islice
from time import sleep


arquivos = os.listdir('/home/(...)/analisar') #Caminho para a pasta onde estão os arquivos a serem analisados

def correspondencia(frase:str) -> list:
	resultados = DDGS().text(keywords= frase, safesearch="off")
	paginas = []
	try:
		for pagina in islice(resultados, 4):
			pag = pagina['href']
			pag_ = requests.get(pag)
			pagina_check = pagina['title']
			print(pagina_check)
			texto = pag_.text
			if frase in texto:
				paginas.append(pag)
			elif frase[2:-2].lower() in texto.lower():
				paginas.append(pag)
			else:
				picado = frase.split(',')
				for trecho in picado:
					if len(trecho) < 16:
						continue
					elif trecho in texto:
						paginas.append(trecho)
						paginas.append(pag)                    
		return paginas
	finally:
		return paginas


for arquivo in arquivos:

	documento = open(f"/home/(...)/analisar{arquivo}")  #Caminho para a pasta onde estão os arquivos a serem analisados

	texto_raw = documento.readlines()
	Aluno = texto_raw[0]
	relatório = open(f'/home/(...)/relatório/relatorio_{Aluno}.txt', 'w') #Gera o output com as informações detectadas

	frases = []
	for frase in texto_raw[:-1]:
		texto = frase.split('.')
		for oracao in texto:
			for c in r'[]{}_+=<>"':
				oracao = oracao.replace(c, '')
			if len(oracao) > 13:
				frases.append(oracao)

	print(f'Incício da checagem, tempo previsto: {len(frases)*0.3} minutos')
	relatório.write(f'Texto de {Aluno}\n')
	p = 0
	c = 0
	for frase in frases:
		plagio = correspondencia(frase)
		if len(plagio) > 0:
			relatório.write(str(frase) + ': ' + str(plagio) + '\n')
			p += 1
		c += 1
		print(f'Concluído: {c/len(frases)*100:.2f}%')
		sleep(0.2)
	porcent = p/len(frases)*100
	relatório.write(str(porcent) + '% de plágio detectado aproximadamente.')
	resultado = f'Finalizado. Porcentagem de plágio: {porcent:.2f}% \nAlune(s): {Aluno}'

	print(resultado) 
	documento.close()
	relatório.close()

