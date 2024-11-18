# Thresholds no Dashboard IoT

## O que são Thresholds?
Thresholds (limiares) são limites definidos para identificar valores que se desviam do comportamento esperado ou aceitável. No contexto do dashboard IoT, eles ajudam a monitorar valores de temperatura e umidade, permitindo:
- Detectar anomalias.
- Gerar alertas para valores fora dos limites definidos.
- Auxiliar na análise do comportamento dos sensores.

## Escolha dos Thresholds

### Percentis (5% e 95%)
Optamos por usar os percentis 5% e 95% para definir os limites inferior e superior porque:
1. **Robustez a Outliers**: Percentis são menos sensíveis a valores extremos, garantindo que outliers não distorçam os limites.
2. **Adaptação aos Dados**: Percentis ajustam-se automaticamente ao comportamento dos dados, refletindo tendências ou variações sazonais.
3. **Simples de Interpretar**: Percentis mostram claramente o intervalo em que a maioria dos dados está contida, sem suposições sobre a distribuição.

Os thresholds são calculados da seguinte forma:
\[
	ext{Limite Inferior} = 5^{	ext{º}} 	ext{ Percentil}
\]
\[
	ext{Limite Superior} = 95^{	ext{º}} 	ext{ Percentil}
\]

### Alternativa: Média e Desvio Padrão
Outra abordagem comum seria:
\[
	ext{Limite Inferior} = 	ext{Média} - 2 	imes 	ext{Desvio Padrão}
\]
\[
	ext{Limite Superior} = 	ext{Média} + 2 	imes 	ext{Desvio Padrão}
\]
Essa fórmula assume uma **distribuição normal** dos dados, onde 95% das observações estão dentro de dois desvios padrão da média.

### Por que Escolhemos Percentis?
- **Não depende de uma suposição de normalidade**: Os dados de sensores nem sempre seguem distribuições normais.
- **Maior robustez contra anomalias**: Outliers extremos não afetam significativamente os percentis.
- **Mais adaptável**: Percentis são adequados para qualquer tipo de distribuição.

## Vantagens do Método de Percentis
1. **Resistência a variações extremas**: Outliers ocasionais não impactam os limites significativamente.
2. **Apropriado para distribuições não normais**: Dados reais frequentemente não seguem padrões normais.
3. **Visualmente intuitivo**: É fácil visualizar os limites em gráficos e interpretar as anomalias.

## Implementação no Dashboard
Os thresholds são aplicados diretamente no dashboard:
1. **Visualização no Gráfico de Dados**:
   - Linhas de limite superior e inferior são exibidas para temperatura e umidade.
   - Valores fora desses limites são claramente identificados como anomalias.
2. **Monitoramento e Alertas**:
   - Caso valores ultrapassem os limites, o dashboard pode destacar essas anomalias visualmente e com mensagens de alerta.

### Código para Calcular Percentis
No código Python, os percentis são calculados com:
```python
def calculate_thresholds(values):
    lower = np.percentile(values, 5)
    upper = np.percentile(values, 95)
    return lower, upper
```

## Conclusão
A escolha dos percentis como thresholds fornece um método confiável, adaptável e robusto para monitorar sensores IoT. Isso melhora a análise e o diagnóstico de problemas, garantindo maior confiança nos dados apresentados no dashboard.
