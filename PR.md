1. criei protege com os conceitos base + 4 dataProperties : nome, idade, periodo e titulo

   adicionei também, ao objectProperty surgeEm, no seu dominio, o Mestre
   sendo agora "Conceito or Mestre -> PeriodoHistorico"

2. comando para correr a migração:

```
python .\populateSapientia.py
```

3. a migração foi feita com os ficheiros na pasta onde o sript é corrido

4. todas as queries foram feitas no ficheiro sparql incluindo os inserts e constructs, a definição dos novos objectProperties foram feitos também no GraphDB
