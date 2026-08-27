# Como publicar no GitHub Pages

O GitHub Pages hospeda páginas HTML de graça, com URL pública e sem servidor. O plano gratuito
só publica de **repositório público** — ver a nota de privacidade no fim.

## Parte 1 — a primeira vez (do zero, ~10 minutos)

**1. Conta.** Se ainda não tem, crie em <https://github.com/signup>. Guarde o nome de usuário —
ele entra na URL final.

**2. Criar o repositório.**
- Clique no `+` no canto superior direito → **New repository**
- **Repository name:** `minum-mapas-bdgd`
- Deixe **Public** marcado
- **Não** marque "Add a README file" (já temos um)
- **Create repository**

**3. Subir os arquivos.** Na tela que aparece, clique em **uploading an existing file**
(ou vá em **Add file → Upload files**).
- Abra o Explorador em `C:\Users\VictorFranco\Claude\Projects\Minum\OUTPUTS\mapas-bdgd`
- Arraste para a página do navegador, de uma vez: a pasta **`docs`**, a pasta **`gerador`**,
  o **`README.md`**, o **`COMO-PUBLICAR.md`** e o **`.gitignore`**
- O navegador preserva a estrutura de pastas
- Em "Commit changes", escreva `primeira publicação` e clique **Commit changes**

**4. Ligar o Pages.**
- No repositório, aba **Settings** (engrenagem, no topo)
- Menu da esquerda: **Pages**
- Em *Build and deployment* → **Source:** `Deploy from a branch`
- **Branch:** `main` &nbsp;·&nbsp; **Folder:** `/docs` → **Save**

**5. Esperar 1–2 minutos.** Recarregue a página de Settings → Pages: aparece
`Your site is live at https://SEU-USUARIO.github.io/minum-mapas-bdgd/`.

Pronto. Essa é a página inicial. Os mapas ficam em:
`https://SEU-USUARIO.github.io/minum-mapas-bdgd/cuiaba-varzea-grande.html`

**6. Atualizar o README.** Abra o `README.md` no GitHub, clique no lápis, troque
`SEU-USUARIO` pelo seu usuário, **Commit changes**.

## Parte 2 — cada cidade nova (~2 minutos)

Não cria repositório novo. É sempre o mesmo.

**1. Gerar, no computador:**
```
cd %USERPROFILE%\Claude\Projects\Minum\OUTPUTS\mapas-bdgd\gerador
python gera_mapa.py --uf PA --cidade "1501402=Belém" --titulo "Belém — PA" --slug belem --min 5000
python gera_index.py
```

**2. Subir:** no repositório → **Add file → Upload files** → arraste a pasta **`docs`** inteira
de novo → *Commit changes*.

O GitHub substitui os arquivos com o mesmo nome (`index.html`, `cidades.json`) e acrescenta os
novos (`belem.html`, `planilhas/UCs_belem.xlsx`). O site se atualiza sozinho em ~1 minuto, e a
cidade nova aparece como mais um cartão na página inicial.

> Se preferir não arrastar a pasta toda, dá para subir só os arquivos que mudaram —
> mas aí é preciso entrar em cada subpasta no GitHub antes de fazer o upload. Arrastar
> `docs` inteira é mais simples e não quebra nada.

## Se quiser algo mais confortável depois

Instale o **GitHub Desktop** (<https://desktop.github.com>) e clone o repositório para
`...\OUTPUTS\mapas-bdgd`. Aí cada atualização vira: rodar os dois scripts → abrir o GitHub Desktop →
**Commit to main** → **Push origin**. Sem arrastar arquivo nenhum.

## Nota de privacidade — vale ler antes

A página fica **pública na internet**, indexável pelo Google. O que ela expõe:

- Os dados em si são públicos (BDGD/ANEEL) e **não têm CNPJ, nome nem titular** — nada de dado
  pessoal vaza.
- Mas ela expõe **a nossa régua de prospecção**: quais cidades estamos trabalhando, qual o corte de
  consumo, quantos leads temos por praça e onde eles estão. Um concorrente que achar a URL ganha
  o mapa de trabalho pronto.

Três caminhos:

| | Custo | Privacidade |
|---|---|---|
| GitHub Pages público (o descrito acima) | grátis | aberto a quem tiver a URL |
| GitHub Pages em repositório privado | precisa GitHub Pro (~US$ 4/mês) | só quem você convidar |
| Cloudflare Pages + Cloudflare Access | grátis | acesso por e-mail autorizado |

Se a ideia é só o time de campo abrir no celular, o segundo ou o terceiro cabe melhor.
Se for para circular livre entre supervisores e SDRs sem fricção, o público resolve.
