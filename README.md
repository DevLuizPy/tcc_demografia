![Simbolo da UFRRJ](https://guiadoestudante.abril.com.br/wp-content/uploads/sites/4/2019/04/resumo-atualidades-demografia-e-envelhecimento-populacional.png?w=1024)
# Os dividendos demográficos da região metropolitana do rio de janeiro
Este é um projeto destinado a compartilhar com outros estudantes da area de economia, interessados na parte de demografia economica, a respeito da metodologia e dos códigos necessários para o cálculo do dividendo demográfico de uma determinada região.

OBS: A base desse projeto será o tcc de minha autoria, que está em andamento, com previsão de conclusão até dezembro de 2025.

**Ultimos uptades**
- [ ] Elaboração da escrita do tcc
- [ ] Calculo do Bonus demografico
- [ ] Tratamento da base de dados
- [x] Criação do pré-projeto

## Sumário

## Introdução 

A população humana durante toda sua existência, sofreu com inúmeras mudanças em seu tamanho e composição, onde diversas disciplinas diferentes buscaram estudar esses processos e explicá-los de maneira coerente. Entretanto ao fim do século XIX, a disciplina chamada demografia alcançou o posto de principal referência, se constituindo como o estudo estatístico das populações humanas, com o foco principal nos agregados em comparação com os indivíduos isoladamente.

A demografia, como uma ciência, tem como característica importante o fato de compartilhar seu estudo com outras diversas áreas de conhecimento. Entre elas, temos a demografia econômica, uma subárea da demografia social, possuindo como dos temais centrais, o estudo do impacto das variáveis populacionais no crescimento e no desenvolvimento economico. Sendo um tema extremamente importante no século XX, especialmente pelo contexto de forte crescimento populacional nos países em desenvolvimento e sua relação com o crescimento da renda per capita.

Em meados daquele século, existia o receio de que o crescimento acelerado da população comprometeria o crescimento da renda, trazendo a necessidade de maiores investimentos em infraestrutura e produtividade. Entretanto, outro grupo de pesquisadores afirmava o contrário; a expansão do crescimento populacional seria benéfica para esses países, devido o potencial aumento da inovação, especialização no mercado de trabalho e nos investimentos, que seriam mais do que suficientes para elevar a produtividade geral da economia.

Nesse contexto, diversos autores passaram a realizar testes econométricos com regressões lineares entre as variáveis de PIB per capita e tamanho da população, obtendo resultados neutros, ou seja, com baixa correlação entre as duas variáveis. Nesse sentido, uma terceira visão, que apontava a neutralidade dessa relação ganhou muita força no debate acadêmico. Somado ao fato de as décadas posteriores serem marcadas por uma queda acentuada no crescimento populacional e por uma melhora nas condições socioeconômicas devido a fatores não relacionados diretamente com a demografia, foram responsáveis pelo fim desse debate.

No século XXI, um novo problema surge, a redução nas taxas de natalidade nos países desenvolvidos e em alguns países emergentes, leva a patamares inferiores a taxa de reposição, 2,1 filhos por mulher, o que traz por consequencia a redução da população no futuro e o envelhecimento da estrutura etária da sociedade. Nesse contexto, diversos estudos a respeito desse problema estão sendo feitos, principalmente em relação aos efeitos econômicos adversos da redução da população em idade ativa.

## Objetivo

Esse trabalho visa a mensuração do efeito do crescimento demográfico em relação ao desenvolvimento economico na região metropolitana do Rio de Janeiro, com base nas informações demográficas previstas nos censos de 1960 até 2010. Para tal, o conceito de dividendo demográfico será apresentado, mostrando a relação entre as variáveis populacionais e variáveis econômicas. Além disso, mudanças na escolaridade e na inserção das mulheres no mercado de trabalho, serão apresentados como parte do dividendo demográfico de educação e gênero.

## Metodologia

Será introduzido o conceito de ciclo de vida economico, o qual compreende que as atividades econômicas variam entre os indivíduos de diferentes faixas etárias. Assim, atribuindo a ideia de indivíduos com renda deficitária e dependente, como as crianças e os idosos, e indivíduos com renda superavitária e não-dependente, como os adultos. Dessa forma, a dinâmica das mudanças na estrutura etária da população será estudada por meio de um modelo de ciclo de vida economico.

Para o cálculo das variáveis desse modelo, será utilizado os microdados dos censos brasileiros presentes no projeto IPUMS International coordenado pela Universidade de Minnesota, devido a sua simplificação e facilidade de utilização. Ademais para a estimativa da população em idade ativa, utilizaremos a variável razão de suporte, que representa a razão da população em idade de trabalho pela população dependente, crianças e idosos. Após isso, será calculado a variação anual da razão de suporte de 1960 até 2010, estabelecendo uma comparação com o crescimento do PIB per capita da região em cada década. Por fim, variáveis de renda, educação e gênero irão compor o restante da análise.
