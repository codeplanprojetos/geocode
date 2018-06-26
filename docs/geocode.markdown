# GEOCODE API

O acesso a GEOCODE API não é feito diretamente, mas pelo aplicativo [GEOCODE UI][1] ou pelo [Portal GEOCODE][2], que o consomem como um serviço. O GEOCODE API possui apenas um _endpoint_ de acesso [REST][3], que transforma endereço (ou parte dele) em coordenadas no mapa (latitude e longitude). O endereço em questão deve ser passado como parâmetro pelo método _GET_ ao servidor pela variável `localidade`. O _endpoint_ aceita um outro parâmetro opcional chamado `limite` que limita o máximo de resultados obtidos. O parâmetro `localidade` não faz distinção no uso de acentos ou caixa alta/baixa. O resultado obtido de retorno segue o padrão [GeoJSON][4] de codificação.

A GEOCODE API oferece resultados mais rápidos de busca em relação a solução anterior porque a indexação dos termos referencia diretamente as coordenadas na base local, que é construída pela biblioteca Whoosh. Para maiores detalhes não esqueça de acessar o `README.md` do [projeto][5].

### Operadores lógicos

O parâmetro localidade aceita operadores lógicos como `OR` (ou lógico), `AND` (e lógico) e agrupamento com parênteses.

```
?localidade=unb OR (universidade AND brasilia)
```

Se o operador não for especificado, o GEOCODE API considera como se o operador `AND` estivesse interligando os termos:

```
?localidade=mane AND garrincha
```

é igual a:

```
?localidade=mane garrincha
```

### Busca difusa (fuzzy)

Por padrão o GEOCODE API aceita que você realize buscas em que os termos não são precisos. Isso aumenta o número de _matches_ no caso de erros de ortografia ou variações na forma de escrever o endereço. Por exemplo:

```
?localidade=mano~1
```

O número depois do til (~) indica a distância de [Damerau-Levenshtein][6] usada na busca e é opcional. Ou seja, ele define quantas alterações do tipo inserção, deleção ou transposição podem existir entre o termo usado e o termo encontrado. Quanto maior este valor, mais lenta deverá ser a busca, portanto é melhor não usar um valor maior do que 2. Não especificar valor nenhum equivale à distância de valor 1.


Referências
* https://github.com/codeplanprojetos/geocode-ui
* http://geocode.codeplan.df.gov.br/
* https://restfulapi.net/
* http://geojson.org
* https://github.com/codeplanprojetos/geocode/blob/master/README.md
* https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

[1]: https://github.com/codeplanprojetos/geocode-ui
[2]: https://geocode.codeplan.df.gov.br/
[3]: https://restfulapi.net/
[4]: http://geojson.org
[5]: https://github.com/codeplanprojetos/geocode/blob/master/README.md
[6]: https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
