# coletor_twitter
#### Desenvovido por Alexandre Prates ####


##Descrição##

Essa aplicação utiliza a streamapi do twitter para coletar tweet com informações de geolocalização. Essa aplicação utiliza o REdis para persistir a informação, abaixo observamos 
como instalar o redis.

Exemplo de inicialização do Redis n máquina local:

```ruby
$ redis-server
```

Exemplo de uso de redis no docker

```ruby
$ docker run --name redis -d -p 6379:6379 redis
```

A implementação e testes foram feito utilizando Ubuntu linux.

##Procedimento de instalação:##

- Crie um diretório;
- Utilize o virtualenv para criar um container python2.7
```ruby
$ virtualenv diretorio
```

- Entre no diretório e copia a pasta do projeto;
- Mude o source do bash para usar a versão do Python instalada no diretorio:

```ruby
$ source bin/activate
```

- Instale as dependências do python, elas estão no arquivo requiment.txt do projeto. Para instalá-las usei o pip:

```ruby
$ pip install -r requeriment.txt
```

- Após instalar as dependência execute o coletor da seguinte maneira:

```ruby
$ python geoteste.py "nome da cidade" raio em relaçãop ao centro.
```


