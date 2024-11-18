
# Projeto IoT - Conexão de Dispositivos e Dashboard

## Visão Geral

Este projeto implementa uma solução de IoT composta por dois dispositivos IoT que enviam dados para um servidor central utilizando o protocolo MQTT. Os dados são armazenados em um banco de dados e exibidos em tempo real em um dashboard interativo, onde thresholds adaptativos e correlações entre os sensores são analisados e exibidos.

---

## Arquitetura

A arquitetura do sistema é composta por:

1. **Dispositivos IoT**:
   - Dois sensores simulados (temperatura e umidade) que enviam dados para um broker MQTT.
   - Os dados enviados incluem:
     - ID único
     - Timestamp
     - Valor medido
     - Unidade
     - Localização
     - Status e validação do dado

2. **Servidor**:
   - Broker MQTT privado configurado para autenticação.
   - Servidor Flask para processamento e armazenamento dos dados recebidos.
   - Armazenamento em um banco SQLite.

3. **Dashboard**:
   - Desenvolvido com Dash.
   - Gráficos de:
     - Leituras dos sensores com thresholds adaptativos baseados no desvio padrão.
     - Correlação entre os dados dos sensores.

---

## Funcionamento

### Dispositivos IoT
Os dispositivos simulados:
- Conectam-se ao Wi-Fi e ao broker MQTT configurado.
- Medem os dados de temperatura e umidade (valores simulados).
- Publicam os dados periodicamente no broker MQTT nos tópicos:
  - `iot-gerson-danilo/temperatura`
  - `iot-gerson-danilo/humidade`.

### Servidor
1. **Broker MQTT**:
   - Configurado com autenticação para receber os dados publicados pelos sensores.
2. **Servidor Flask**:
   - Escuta mensagens MQTT e insere os dados recebidos no banco de dados SQLite.
3. **Banco de Dados**:
   - Estrutura:
     - ID do dado
     - Tipo de sensor
     - Valor medido
     - Unidade
     - Timestamp
     - Localização
     - Status e validação

### Dashboard
- Periodicamente, busca os dados no endpoint `/data` do servidor Flask.
- Exibe dois gráficos:
  1. **Gráfico de Thresholds Adaptativos**:
     - Mostra os valores medidos pelos sensores com thresholds calculados a partir do desvio padrão.
  2. **Gráfico de Correlação**:
     - Analisa a correlação entre as leituras de temperatura e umidade e exibe a relação gráfica.
     - Destaca a correlação com uma métrica e status ("OK" ou "ALERTA").

---

## Requisitos do Trabalho
Conforme o enunciado:
1. **Dois Dispositivos IoT**:
   - Implementados com simulação de sensores DHT22.
2. **Conexão MQTT**:
   - Comunicação eficiente e robusta com autenticação.
3. **Dashboard com Gráficos**:
   - Utiliza thresholds adaptativos (desvio padrão).
   - Exibe correlação entre os sensores.
4. **Explicação das Escolhas**:
   - Thresholds adaptativos oferecem flexibilidade para condições dinâmicas.
   - A correlação permite identificar relações entre variáveis (ex.: umidade alta pode impactar na temperatura).

---

## Passo a Passo de Execução

### Configuração do Broker MQTT
1. Suba o container Docker com o Mosquitto configurado:
   ```bash
   docker-compose up -d
   ```
2. Certifique-se de que o arquivo de configuração do Mosquitto inclua autenticação.

### Inicialização do Servidor
1. Execute o container do servidor Flask e Dashboard:
   ```bash
   docker-compose up --build
   ```

### Execução dos Dispositivos IoT
1. Substitua o endereço do broker e credenciais nos códigos dos dispositivos.
2. Execute os scripts em dispositivos simulados (ex.: Wokwi) ou placas físicas.

### Acesso ao Dashboard
- Acesse o Dashboard no navegador:
  ```url
  http://<ENDEREÇO_DO_SERVIDOR>:8050
  ```

---

## Requisitos Atendidos
1. **Conexão IoT com MQTT**: Implementada com autenticação e dados simulados.
2. **Dashboard Interativo**: Atualização em tempo real com gráficos explicativos.
3. **Thresholds e Correlação**: Calculados dinamicamente com visualização clara.

--- 

## Tecnologias Utilizadas
- **Python**: Backend (Flask, Paho MQTT) e IoT (MicroPython).
- **SQLite**: Banco de dados.
- **Dash**: Desenvolvimento do dashboard.
- **Docker**: Contêineres para fácil implantação.
- **MQTT**: Protocolo de comunicação eficiente.

---

## Sensores

https://wokwi.com/projects/322577683855704658 - humidade
https://wokwi.com/projects/322577683855704658 - temperatura

---

Este documento descreve detalhadamente os requisitos do projeto, as tecnologias utilizadas e o funcionamento do sistema.
