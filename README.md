# Entidades

| Entidades  | Propriedades |
| ------------- | ------------- |
| Loja  |  Deve ter a unidade da loja e coordenadas de geolocalização |
| Representante  |  Deve ter viculo á unidade da empresa, cargo (sendo os únicos: Financeiro, Administrador, Operador), nome e CPF |
| Produto |  Deve ter imagem, nome, quantia em estoque, valor, código de barras ([EAN-13](https://pt.wikipedia.org/wiki/EAN-13), salvando uma identidade única), unidade da loja cadastrada |
| Venda | Deve possuir o valor total da venda, número de N-FE, data e hora da venda |
| Auditoria | Apenas registrar quando foi uma venda, estorno e baixa de funcionário |

# Features
- Ao cadastrar um funcionário, deve ter como dar baixa (retirar o acesso mas sem excluir da base de dados) e editar o CPF (somente com permissão de administrador), como funcionário deve ter acesso somente para editar o nome;
- Ao cadastrar um produto, deve ter como consultar por código de barras com a permissão de operador, editar o valor com a permissão de financeiro, visualizar as vendas e fazer estorno com permissão de financeiro e informações totais do produto como administrador;

# Atenção
* Ao consultar um produto de forma geral, tentar da melhor forma possível não deixar duplicar os resultados por conta da unidade da loja.
* Ao registrar uma venda, deve ser possível marcar se foi uma venda remota (onde pega o estoque de uma outra unidade) e caso for uma venda remota, deve ser possível a quebra de contrato para efetuar o reembolso dentro de 7 dias independente da razão do consumidor.
* Para informações sensíveis como o CPF, deve ser aplicado uma máscara antes de salvar no banco de dados.

# Fluxo

O **usuário** vai a qualquer unidade da loja e após escolher um produto, deve ter como consultar o valor através de um scanner ou chamando um funcionário (casa haja dúvidas), caso não tenha em estoque na unidade onde o usuário se encontra, deve ser possível buscar o mesmo produto em outras unidades da loja e possibilitando a compra e escolhendo se vai retirar no local ou entrega.

A **empresa** deve ter a possibilidade de cadastrar produtos, efetuar vendas, estornos, gerenciamento de funcionários e visualização de auditoria.
