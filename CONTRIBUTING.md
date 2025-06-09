# Contributing

## Fluxo de colaboração

O fluxo de colaboração adotado em nosso projeto foi o GitFlow, na qual teremos a Branch Main, a Branch Develop, e cada membro fará uma branch para as features, atuando nas features de sua especialidade/preferência, seja no front ou no back.

Dessa forma, ao clonar o repositório e fazer sua própria branch, cada colaborador trabalhará em uma feature em questão, e, quando concluída, revisará seu próprio código e fará o seu commit. Após finalizada a sua feature na branch, deverá realizar um Pull request para o Develop, que será análisado por colegas que estão trabalhando na mesma parte do sistema em que aquela feature estava sendo elaborada, por algum colega relacionado à aquela parte ou apenas alguem que tenha experiência. Após a avaliação dos colegas e implementações das features escolhida para cada sprint, será então dado a merge na Main para salvar o versionamento da aplicação naquela sprint.

Em caso de erros ao na branch develop ou main, deve-se abrir uma issue e comunicar aos colegas para realizar uma correção, esta que será feita em conjunto por pessoas que estavam trabalhando na área em que deu erro e até outros membros com experiência na área, e então criarão uma branch hotfix para solucionar o erro em conjunto e em seguida fazer o merge da versão corrigida tanto para a main quanto para o develop.

No fim haverá a divisão de foco por front e back, na qual teremos 3 colaboradores em 1 parte, e 4 em outra, em cada uma dessas áreas haverá a divisão por feature, a revisão de código e definição de pronto será feita em conjunto após a análise individual da parte da feature que a pessoa estava responsável e por fim, após as adições das features e versões do código, o merge final será feito com a análise conjunta de todos para a realização da branch release e merge final da aplicação.

## Nomes de branches e mensagens de commit

Para os nomes de commit, convencionamos que o ideal é que o colaborador coloque a área da feature que está implementando, a feature em questão, e uma descrição curta do que é a feature e como funcionará, no seguinte formato

front(feat): descrição crurta
back(feat): descrição curta

*com apenas 1 espaçamento após os 2 pontos.*

Em caso de correção, ao invés de feat, colocar "fix", também entre os parênteses e explicando qual vai ser a correção e o porquê.

Já a nomeação das branches terão que ter informando se é uma correção ou uma implementação, e o nome do que será feito na branch separados por "-", da seguinte forma:

feat/rota-login\
fix/erro-esqueci-minha-senha

## Revisão de código

Para revisão de código definimos os seguintes parâmetros:

* Todo PR deve ser revisado por pelo menos 1 membro;

* A Revisão deve verificar:  

  * Clareza e legibilidade do código.\
  * Funcionalidade e testes.\
  * Conformidade com o estilo e o padrão do projeto.
* As sugestões devem ser feitas de forma construtiva
* Alterações Solicitas devem ser aplicadas antes do merge
* A feature deve atender aos requisitos esperados

## Configuração local

Para a configuração local decidimos que cada colaborador trabalhará em uma branch pessoal/local para a feature que estiver responsável, antes de iniciar, utiliza o git fecth para atualizar o seu repositório local, faz a codagem da feature em questão, faz o commit para sua própria branch, e, antes de fazer o pull resquest, novamente dá um pull para se certificar que estará fazendo a adição da feature sem conflitar com a forma que estiver o código na branch develop, e, posteriormente, na main.
