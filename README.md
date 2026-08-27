# mapas-bdgd — Minum

Mapas interativos de unidades consumidoras de alto consumo, por cidade, a partir da
**BDGD/ANEEL** (Base de Dados Geográfica da Distribuidora, safra 31/12/2024).

Site publicado: **https://SEU-USUARIO.github.io/minum-mapas-bdgd/**
(ajustar depois de configurar o GitHub Pages — ver `COMO-PUBLICAR.md`)

## Estrutura

```
mapas-bdgd/
├── docs/                       ← o site (é daqui que o GitHub Pages serve)
│   ├── index.html                 página inicial, lista as cidades
│   ├── cidades.json               manifesto — alimenta o index
│   ├── <cidade>.html              um mapa por cidade
│   └── planilhas/<cidade>.xlsx    a planilha de campo de cada cidade
├── gerador/
│   ├── gera_mapa.py               gera o mapa + a planilha + atualiza o manifesto
│   ├── gera_index.py              reconstrói o index.html a partir do manifesto
│   ├── cnae_map.py                281 subclasses CNAE 2.3 → setor + descrição
│   └── template_mapa.html         template do mapa
└── README.md
```

A base da BDGD (os `.parquet`) **não fica aqui** — continua em `C:\Users\VictorFranco\Documents\bdgd`.
Este repositório guarda só o gerador e o que é publicado.

## Rodar uma cidade nova

```
cd %USERPROFILE%\Claude\Projects\Minum\OUTPUTS\mapas-bdgd\gerador
python gera_mapa.py --uf GO --cidade "5208707=Goiânia" --titulo "Goiânia — GO" --slug goiania --min 5000
python gera_index.py
```

Cidades coladas entram no mesmo mapa: repita `--cidade`.

```
python gera_mapa.py --uf MT --cidade "5103403=Cuiabá" --cidade "5108402=Várzea Grande" ^
    --titulo "Cuiabá + Várzea Grande — MT" --slug cuiaba-varzea-grande --min 5000
```

Outros parâmetros: `--min` (corte de kWh/mês, padrão 5.000), `--base` (pasta da BDGD),
`--manter-pp` (não excluir poder público / IP / saneamento / consumo próprio).

Dependências: `pip install --user duckdb pandas xlsxwriter`. Roda em ~30 s por cidade.

## Regra de seleção

`UCBT_tab` com `SIT_ATIV='AT'`, município na lista, média dos 12 meses de `ENE_01..12` ≥ corte,
excluindo `CLAS_SUB` em PP%/IP/SP%/CPR e CNAE de divisão 84, 36 e 37.
Coordenada via `PN_CON → PONNOT.Shape`. Medidor via `EQME.UC_UG → UCBT_tab.COD_ID`.

**Régua de média tensão (exclusão dura).** Quando o mesmo `COD_ID` aparece também na `UCMT_tab`, é o
mesmo cliente registrado nas duas tabelas — energia medida na linha de BT, demanda contratada na de
MT. Na prática é cliente do Grupo A, com quem a Minum não pode atuar. Essas UCs são **removidas na
origem**: não entram no mapa, não entram na planilha, e não existe filtro para trazê-las de volta.
O log da execução informa quantas saíram.

> **Confirmar por estado antes de rodar.** Esse padrão é da **Energisa** (MT, provavelmente MS). Em
> Imperatriz (Equatorial MA) o mesmo cruzamento dá **zero** — ou a Equatorial não duplica o registro,
> ou usa outra convenção. Antes de gerar um estado novo, conferir quantas UCs do recorte casam com a
> `UCMT_tab`: se der zero, a régua de MT precisa de outra fonte.

## Ressalvas que valem sempre

- A coordenada é a do **poste**, não da fachada. Prova proximidade, nunca titularidade.
- O consumo é o que passou pelo medidor: quem já tem geração própria aparece com consumo residual.
- `CEG_GD` marca só quem tinha usina própria conectada em 31/12/2024 — não pega quem recebe crédito
  remoto de fazenda solar de terceiro.
- A BDGD **não tem CNPJ nem nome**. A identificação depende de cruzamento externo, ou do código do
  medidor da fatura.
