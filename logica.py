'''e (Evento):

Quando o valor do campo de texto muda, a função on_change_valor é chamada automaticamente.
O parâmetro e representa o evento que foi disparado, contendo informações sobre o campo que disparou o evento.

e.control refere-se ao controle (ou componente) que está gerando o evento, neste caso, o TextField.
e.control.value:

Esse é o valor atual do campo de texto (o que o usuário digitou).
filter(str.isdigit, e.control.value):

A função filter aplica uma condição a cada caractere do valor digitado (e.control.value).
str.isdigit é uma função que verifica se um caractere é um dígito (ou seja, se é um número de 0 a 9).

Portanto, fil
ter(str.isdigit, e.control.value) retorna apenas os caracteres que são dígitos, ignorando qualquer letra ou símbolo que não seja numérico.


'''