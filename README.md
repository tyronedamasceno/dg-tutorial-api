# dg-tutorial

Olá, esse é um tutorial sobre [Django Rest Framework](https://www.django-rest-framework.org/), preparado para o Curso de Verão de Django Rest Framework e ReactNative, promovidos por [Grupy-RN](https://meetup.grupyrn.org/), [Natal JS](https://github.com/NatalJS) com apoio da [B2SOFT](https://b2soft.com.br/).

Os modelos aqui utilizados são baseados no tutorial de Django do [Django Girls](https://tutorial.djangogirls.org/pt/).

O que será abordado por aqui?

- O que é API e REST
    - Verbos HTTP
- O que é Django Rest Framework
- Modelo de dados
- Serializers
- Views baseadas em função
- Views baseadas em classe
- Autenticação e Permissões
    - Baseada em Token
- Routers
- Consumindo a API
    - Curl (Usar Postman)


## O que é API? E API Rest?

API é um acrônimo do inglês *application programming interface*, ou interface de programação de aplicações em português.

Em linhas gerais, uma API é um ponto de acesso de uma certa aplicação X, para que outras aplicações Y, W e Z consigam acessar funcionalidades desta, sem necessariamente conhecer detalhes da implementação da aplicação ou acessar diretamente seus servidores, etc.

Resumidamente, APIs permitem de forma rápida, prática e segura (ou pelo menos deveriam) comunicação entre aplicações.

Certo, então o que é uma API Rest?

Bem, tudo começa com uma sigla que provavelmente você já viu: **HTTP**. Este é o principal protocolo de comunicação entre sistemas web usado no mundo, que já existe a mais de 20 anos.

O HTTP trata de resolver requisições entre aplicações, para isso existem alguns **verbos HTTP**, entre eles estão *GET*, *POST*, *DELETE*, mas existem diversos outros, e eles existem pra facilitar o entendimento de nós humanos sobre o que está ocorrendo na web. É simples perceber que uma requisição de *GET* tem como objetivo "pegar" informações, enquanto *DELETE* visa apagar algo (sempre tenham cuidado com o delete).

Esses princípios são o que definem o REST, que significa *Representational State Transfer*, ou em português, Transferência de Estado Representacional. Em resumo, é uma abstração da arquitetura web, e esses princípios, padrões e regras (que iremos aprender), quando são seguidas permitem a criação de um sistema ou projeto, no nosso caso uma API com interfaces bem definidas, o que facilita sua comunicação com outras aplicações.

## O que é Django Rest Framework

** *O framework Django REST é um kit de ferramentas poderoso e flexível para criar APIs da Web.* **  (Tradução do google da definição do próprio site do DRF).

O django rest framework é uma biblioteca python que se acopla em projetos django, e entregam uma super base para construção de APIs REST, com toda a robustez do Django, altamente extensível e confiável.

Além disso, o django rest framework é tão simples de instalar em usar como qualquer pacote python. 

Considerando que você já tem o pip instalado (afinal, você deve ter feito o tutorial do Django girls né?!), já ativou sua virtualenv, basta UM ÚNICO COMANDO.

Se você nao lembra, para ativar virtualenv, basta este comando:

`$ source venv/bin/activate`

Para instalar o django rest framework use este comando:
`$ pip install djangorestframework`

O legal é que caso você ainda não tenha o django instalado, ao instalar o djangorestframework ele automaticamente também instala o django!

Como estamos dando continuidade ao tutorial do django girls, não vamos iniciar um novo projeto, apenas adicionaremos o djangorestframework nas configurações do projeto no arquivo settings.py localizado na pasta mysite.

```
INSTALLED_APPS = [
   ...,
   'rest_framework',
]
```

Pronto! Já temos o Django rest framework em nosso projeto!


## Modelos de dados

TODO

## Serializers

Os Serializadores do DRF permitem que dados "complexos", como objetos e querysets sejam convertidos em tipos de dados Python, para assim serem renderizados em formato JSON (ou outros formatos como xml, yml, etc.) e assim permite que a comunicação entre as aplicações ocorra de forma correta, que é o objetivo de uma API.

Para quem já conhece, os serializadores do DRF parecem muito com os Form e ModelForm do Django.

No caso da nossa aplicação, usaremos o `ModelSerializer`, que é um serializador completo pré-pronto, com operações padrão, para instanciações e consultas de nossos modelos.

No nosso caso, faremos um serializador para o modelo Post, o exemplo veremos abaixo:

Crie um arquivo serializers.py dentro da pasta blog:

```
from rest_framework import serializers

from .models import Post

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')
```

Como nós usamos um ModelSerializer, precisamos definir uma classe Meta (responsável por configurar o serializer), onde diremos ao DRF sobre qual modelo aquele serializador irá atuar, bem como quais atributos, *fields*, ele irá serializar.


## Views baseadas em função

Neste tipo é necessário implementar tudo do zero. Neste tutorial usaremos Views baseadas em classe.

## Views baseadas em classe

Uma class based views é um padrão poderoso, que permite reutilizar funcionalidades comuns em views, além de nos ajudar a manter um código limpo.

Além disso, o DRF nos permite combinar um conjunto de views relacionadas em uma única view, isso chamamos de ViewSet.

Uma classe ViewSet é simplesmente uma View baseada em classe que não fornece nenhum método por padrão.

Neste tutorial iremos usar uma especialização da ViewSet, o ModelViewSet, que provê todas as funcionalidades básicas necessárias para nossa API.

Edite sua classe views.py localizada na pasta blog, para ficar semelhante ao código abaixo:

```
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from rest_framework import viewsets
from .serializers import PostModelSerializer


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'blog/post_list.html', {'posts': posts})

class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-title')
    serializer_class = PostModelSerializer
```

O ModelViewSet exige que nós digamos pra ele qual serializador usar para criar a view, neste caso usaremos o serializador que criamos, PostSerializer.


## URL e Routers

Até agora já definimos nossos modelos, serializadores, views, porém como acessá-los? Através de urls, também conhecidos como *endpoints*.

Como vocês viram no tutorial de django, as url podem ser definidas manualmente e acopladas em suas views, porém a arquitetura REST segue um padrão, então seus endpoints devem atender a algumas regras.

Para não termos problemas com isso, o DRF nos dá de presente os  **ROUTERS**, que juntos a um viewset fazem todo o roteamento das requisições.

Veremos no exemplo abaixo como funcionam no arquivo `urls.py` do app blog:

```
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('posts', views.PostModelViewSet)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('api/v1/', include(router.urls))
]
```

Neste momento, salvamos os arquivos, e rodamos o nosso servidor local.

`$ python manage.py runserver`

E acessaremos o endpoint da API:

`localhost:8000/api/v1`

