# coletor_twitter


# Desenvovido por Alexandre Prates



Descrição

Essa aplicação utiliza a streamapi do twitter para coletar tweet com informações de geolocalização. Essa aplicação utiliza o REdis para persistir a informação, abaixo observamos 
como instalar o redis.

Exemplo de inicialização do Redis n máquina local:
$redis-server

Exemplo de uso de redis no docker

# docker run --name redis -d -p 6379:6379 redis

A implementação e testes foram feito utilizando Ubuntu linux.



Procediemnto de instalação:

1 - Crie um diretorio;
2 - Utilize o virtualenv para criar um container python2.7
$virtualenv diretorio
3 - Entre no diretorio e copia a pasta do projeto;
4 - Mude o source do bash para usar a versão do Python instalada no diretorio:
$ source bin/active
5 - Instale as dependencias do python, elas estão no arquivo requiment.txt do projeto. Para instala-las usei o pip:
$pip install -r requeriment.txt
6 - Apos instala r as dependencia execute o coletor da seguinte maneira:
$ python geoteste.py "nome da cidade" raio em relaçãop ao centro.

