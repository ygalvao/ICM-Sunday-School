import requests as req
import json, html, time

def program_end():
    print('\nFim do programa.')
    time.sleep(5)

def confirm(text):
    confirm = input(text)
    print()
    
    if confirm not in ('n', 'N', 'Não', 'NÃO', 'não'):
        return 'Sim'
    else:
        program_end()
        return

def envia_contribuicoesICM():
##    url = 'https://webhook.site/6eba867b-2481-4b68-b7a0-811349e68186'
    url = 'https://intregracao-site.presbiterio.org.br/api-ebd/cadastro-contribuicao'
    headers = {'Host': 'intregracao-site.presbiterio.org.br', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json;charset=utf-8', 'Origin': 'https://www.igrejacristamaranata.org.br', 'Connection': 'keep-alive', 'Referer': 'https://www.igrejacristamaranata.org.br/'}
    
    qtd = int(input('''Digite a quantidade de contribuições a serem enviadas de uma mesma pessoa: '''))
    cpf = input('CPF (apenas números): ')
    dados = req.get('''https://intregracao-site.presbiterio.org.br/api-ebd/consultacpf/''' + cpf, timeout=7)
    dadosj = json.loads(dados.text)
    nome = dadosj['nome']
    print()
    print('##################################')
    for item in dadosj.items():
        print(item[0], ': ', item[1], sep='')
    print('##################################')
    print()
    denominacao = 21
##    ddd = input('Digite o DDD (apenas números): ')
##    if ddd == '11':
##        celular = '(11) ' + input('Nº de celular (apenas números): ')
##    else:
##        celular = '(13) ' + input('Nº de celular (apenas números): ')
    celular = dadosj['celular']
##    email = input('Email: ')
    email = dadosj['email']
##    cidade = input('Cidade: ')
    cidade = dadosj['cidade']
##    uf = 'SP'
    uf = dadosj['uf']
    funcao = input('''Digite o nº correspondente:
9  - Membro
1  - Obreiro
5   - Senhora de Frente
10 - Professora
''')
    
    ult_ebd_id = '1241'
    ebd_id = input('Digite o ID da EBD (o ID da EBD 27 é/foi ' + ult_ebd_id + '): ')
    
    if ebd_id in ('', '0', None):
        ebd_id = ult_ebd_id
        
    trabalho = '21'
    categoria = '2'
    confirma = confirm('Serão enviadas ' + str(qtd) + ' contribuições de ' +  nome + '. Confirma (s/n)? ')
    for i in range(qtd):
        contribuicao = input('Digite ou cole o texto da contribuição nº ' + str(i+1)+': ')
        contribuicao = html.escape(contribuicao)
        data = {'nome': nome, 'cpf': cpf, 'denominacao_id': denominacao, 'denominacao_outras': '', 'celular': celular, 'email': email, 'cidade': cidade, 'uf': uf, 'funcao': '', 'funcao_id': funcao, 'trabalho_id': trabalho, 'ebd_id': ebd_id, 'categoria_id': categoria, 'contribuicao': '<p>' + contribuicao + '</p>', 'aceite_termo':True}
        r = req.post(url, data=json.dumps(data), headers=headers)
        if r.ok:
            print('Contribuição', i + 1, 'enviada com sucesso!')
        else:
            print('Houve algum erro no envio! O programa será interrompido!')
            time.sleep(3)
            break
        
    global Confirma    
    Confirma = confirm('Deseja enviar outra contribuição (s/n)? ')

if __name__ == '__main__':
    envia_contribuicoesICM()

while Confirma == 'Sim':
    envia_contribuicoesICM()
