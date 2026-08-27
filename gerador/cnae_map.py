# -*- coding: utf-8 -*-
"""CNAE (subclasse 2.3) -> (setor, descricao curta) para os mapas da BDGD.
Setores usam a mesma taxonomia do mapa de Imperatriz, com 'Imobiliario' e 'Sem CNAE' a mais.
Fonte das descricoes: CNAE 2.3 (IBGE/CONCLA), redigidas em forma curta.
"""
SET = {
 "V":"Varejo","A":"Atacado","I":"Indústria","S":"Serviços profissionais/empresariais",
 "T":"Telecom/Mídia/TI","SE":"Saúde/Educação","AL":"Alimentação (bares/restaurantes)",
 "C":"Cultura/Esporte/Lazer","TR":"Transporte/Logística","VE":"Veículos","AG":"Agropecuária",
 "F":"Financeiro","CO":"Construção","SP":"Serviços pessoais/associações","EN":"Energia",
 "H":"Hotelaria","IM":"Imobiliário","O":"Outros","X":"Sem CNAE",
}
_RAW = """
(vazio)|X|Sem CNAE informado
0111-3/99|AG|Cultivo de outros cereais n.e.
0115-6/00|AG|Cultivo de soja
0119-9/01|AG|Cultivo de abacaxi
0119-9/99|AG|Cultivo de lavoura temporária n.e.
0122-9/00|AG|Cultivo de flores e plantas ornamentais
0151-2/01|AG|Criação de bovinos para corte
0151-2/02|AG|Criação de bovinos para leite
0153-9/01|AG|Criação de caprinos
0159-8/01|AG|Criação de coelhos
1011-2/01|I|Frigorífico - abate de bovinos
1031-7/00|I|Fab. de conservas de frutas
1053-8/00|I|Fab. de sorvetes
1066-0/00|I|Fab. de alimentos para animais
1091-1/00|I|Fab. de produtos de panificação
1091-1/01|I|Fab. de produtos de panificação industrial
1091-1/02|I|Fab. de padaria/confeitaria (própria)
1099-6/01|I|Fab. de vinagres
1113-5/01|I|Fab. de cervejas e chopes
1359-6/00|I|Fab. de outros produtos têxteis n.e.
1413-4/01|I|Confecção de roupas profissionais
1610-2/03|I|Serraria - desdobramento de madeira em bruto
1621-8/00|I|Fab. de madeira laminada e chapas de compensado
1622-6/00|I|Fab. de estruturas de madeira e carpintaria
1622-6/02|I|Fab. de esquadrias/peças de madeira
1629-3/00|I|Fab. de artefatos de madeira n.e.
1629-3/01|I|Fab. de artefatos diversos de madeira
1710-9/00|I|Fab. de celulose/pastas para papel
1741-9/02|I|Fab. de produtos de papel/papelão
1813-0/01|I|Impressão de material publicitário
2071-1/00|I|Fab. de tintas, vernizes, esmaltes e lacas
2212-9/00|I|Reforma de pneumáticos usados
2221-8/00|I|Fab. de laminados de material plástico
2222-6/00|I|Fab. de embalagens de material plástico
2229-3/01|I|Fab. de artefatos de plástico p/ uso pessoal/doméstico
2229-3/03|I|Fab. de artefatos de plástico p/ construção
2330-3/01|I|Fab. de estruturas pré-moldadas de concreto
2330-3/99|I|Fab. de outros artefatos de cimento/gesso n.e.
2342-7/01|I|Fab. de azulejos e pisos
2342-7/02|I|Fab. de artefatos de cerâmica p/ construção
2399-1/00|I|Fab. de produtos de minerais não metálicos n.e.
2399-1/01|I|Decoração/gravação em cerâmica, louça, vidro e cristal
2449-1/03|I|Fab. de ânodos para galvanoplastia
2512-8/00|I|Fab. de esquadrias de metal
2710-4/01|I|Fab. de geradores de corrente contínua e alternada
2710-4/02|I|Fab. de transformadores, indutores e conversores
2852-6/00|I|Fab. de máquinas p/ extração mineral e construção
2944-1/00|I|Fab. de peças p/ sistema motor de veículos
3102-1/00|I|Fab. de móveis com predominância de metal
3511-5/01|EN|Geração de energia elétrica
3512-3/00|EN|Transmissão de energia elétrica
3514-0/00|EN|Distribuição de energia elétrica
3832-7/00|O|Recuperação de materiais plásticos
4110-7/00|CO|Incorporação de empreendimentos imobiliários
4120-4/00|CO|Construção de edifícios
4221-9/01|CO|Construção de barragens e represas p/ geração de energia
4222-7/02|CO|Construção de redes de água/esgoto
4292-8/02|CO|Obras de montagem industrial
4299-5/99|CO|Outras obras de engenharia civil n.e.
4511-1/01|VE|Varejo de automóveis novos
4511-1/02|VE|Varejo de automóveis usados
4520-0/01|VE|Manutenção/reparação mecânica de veículos
4520-0/05|VE|Lavagem/lubrificação de veículos (lava-jato)
4530-7/00|VE|Comércio de peças e acessórios para veículos
4530-7/01|VE|Atacado de peças/acessórios novos para veículos
4530-7/02|VE|Atacado de pneumáticos e câmaras de ar
4530-7/03|VE|Varejo de peças/acessórios para veículos
4541-2/03|VE|Varejo de motocicletas novas
4611-7/00|A|Repres. de matérias-primas agrícolas/animais
4617-6/00|A|Repres. de produtos alimentícios/bebidas/fumo
4618-4/99|A|Representantes comerciais n.e.
4623-1/06|A|Atacado de sementes, flores, plantas e gramas
4623-1/08|A|Atacado de matérias-primas agrícolas c/ fracionamento
4631-1/00|A|Atacado de leite e laticínios
4633-8/01|A|Atacado de frutas, verduras e hortaliças
4633-8/03|A|Atacado de pequenos animais vivos p/ alimentação
4634-6/01|A|Atacado de carnes bovinas/suínas
4634-6/02|A|Atacado de aves abatidas e derivados
4634-6/03|A|Atacado de pescados e frutos do mar
4635-4/02|A|Atacado de cerveja, chope e refrigerante
4637-1/04|A|Atacado de pães, bolos, biscoitos
4637-1/06|A|Atacado de sorvetes
4637-1/99|A|Atacado especializado em outros alimentos n.e.
4639-7/01|A|Atacado de produtos alimentícios em geral
4639-7/02|A|Atacado de alimentos em geral c/ fracionamento
4641-9/01|A|Atacado de tecidos
4644-3/01|A|Atacado de medicamentos de uso humano
4644-3/02|A|Atacado de medicamentos de uso veterinário
4645-1/01|A|Atacado de materiais médicos/hospitalares
4646-0/01|A|Atacado de cosméticos e perfumaria
4646-0/02|A|Atacado de produtos de higiene pessoal
4647-8/01|A|Atacado de artigos de escritório e papelaria
4649-4/99|A|Atacado de outros artigos de uso pessoal/doméstico n.e.
4651-6/01|A|Atacado de equipamentos de informática
4651-6/02|A|Atacado de suprimentos para informática
4661-3/00|A|Atacado de máquinas/equip. agropecuário
4662-1/00|A|Atacado de máquinas p/ terraplenagem e construção
4663-0/00|A|Atacado de máquinas/equip. industrial
4669-9/01|A|Atacado de bombas e compressores
4669-9/99|A|Atacado de outras máquinas/equipamentos n.e.
4672-9/00|A|Atacado de ferragens e ferramentas
4679-6/01|A|Atacado de tintas, vernizes e similares
4679-6/04|A|Atacado de materiais de construção n.e.
4679-6/99|A|Atacado de materiais de construção em geral
4681-8/01|A|Atacado de combustíveis (gasolina, álcool, derivados)
4683-4/00|A|Atacado de defensivos, adubos e fertilizantes
4684-2/99|A|Atacado de outros produtos químicos n.e.
4686-9/02|A|Atacado de embalagens
4687-7/02|A|Atacado de resíduos e sucatas metálicos
4691-5/00|A|Atacado de mercadorias em geral (alimentício)
4711-3/01|V|Hipermercados
4711-3/02|V|Supermercados
4712-1/00|V|Minimercados, mercearias e armazéns
4713-0/02|V|Lojas de variedades (exceto departamentos/magazines)
4713-0/04|V|Lojas de departamentos ou magazines
4713-0/05|V|Lojas francas (duty free)
4721-1/02|V|Padaria/confeitaria (revenda)
4721-1/03|V|Varejo de laticínios e frios
4722-9/01|V|Açougues
4722-9/02|V|Peixaria
4723-7/00|V|Varejo de bebidas
4724-5/00|V|Varejo de hortifrutigranjeiros
4729-6/01|V|Tabacaria
4729-6/02|V|Lojas de conveniência
4729-6/99|V|Varejo de produtos alimentícios n.e.
4731-8/00|V|Posto de combustível
4741-5/00|V|Varejo de tintas e materiais para pintura
4742-3/00|V|Varejo de material elétrico
4743-1/00|V|Varejo de vidros
4744-0/01|V|Varejo de ferragens e ferramentas
4744-0/05|V|Varejo de materiais de construção n.e.
4744-0/99|V|Varejo de materiais de construção em geral
4751-2/01|V|Varejo de equipamentos e suprimentos de informática
4752-1/00|V|Varejo de equip. de telefonia/comunicação
4753-9/00|V|Varejo de eletrodomésticos/áudio e vídeo
4754-7/01|V|Varejo de móveis
4754-7/03|V|Varejo de artigos de iluminação
4755-5/01|V|Varejo de tecidos
4759-8/99|V|Varejo de outros artigos de uso doméstico n.e.
4761-0/01|V|Varejo de livros
4763-6/02|V|Varejo de artigos esportivos
4771-7/00|V|Farmácias e drogarias
4771-7/01|V|Farmácia sem manipulação
4771-7/04|V|Varejo de medicamentos veterinários
4772-5/00|V|Varejo de cosméticos e higiene pessoal
4773-3/00|V|Varejo de artigos médicos e ortopédicos
4774-1/00|V|Varejo de artigos de óptica
4781-4/00|V|Varejo de vestuário e acessórios
4782-2/01|V|Varejo de calçados
4789-0/01|V|Varejo de suvenires, bijuterias e artesanatos
4789-0/99|V|Varejo de outros produtos n.e.
4790-3/00|V|Comércio ambulante e outros tipos de varejo
4921-3/01|TR|Transporte coletivo de passageiros municipal
4922-1/01|TR|Transporte coletivo de passageiros intermunicipal
4922-1/02|TR|Transporte coletivo de passageiros interestadual
4929-9/00|TR|Transporte rodoviário coletivo (fretamento/turismo)
4930-2/00|TR|Transporte rodoviário de carga
4930-2/01|TR|Transporte rodoviário de carga municipal
4930-2/02|TR|Transporte rodoviário de carga inter/estadual
4930-2/04|TR|Transporte rodoviário de mudanças
5111-1/00|TR|Transporte aéreo de passageiros regular
5112-9/01|TR|Táxi aéreo/locação de aeronaves
5211-7/01|TR|Armazéns gerais - emissão de warrant
5212-5/00|TR|Carga e descarga
5221-4/00|TR|Concessionárias de rodovias, pontes e túneis
5222-2/00|TR|Terminais rodoviários e ferroviários
5223-1/00|TR|Estacionamento de veículos
5229-0/02|TR|Serviços de reboque de veículos
5229-0/99|TR|Outras atividades auxiliares dos transportes terrestres
5250-8/04|TR|Organização logística do transporte de carga
5310-5/01|TR|Atividades do Correio Nacional
5320-2/02|TR|Serviços de entrega rápida
5510-8/01|H|Hotéis
5510-8/03|H|Motéis
5590-6/00|H|Outros tipos de alojamento
5590-6/99|H|Outros alojamentos n.e.
5611-2/01|AL|Restaurantes e similares
5611-2/03|AL|Lanchonetes e similares
5611-2/04|AL|Bares e bebidas, sem entretenimento
5611-2/05|AL|Bares e bebidas, com entretenimento
5612-1/00|AL|Serviços ambulantes de alimentação
5620-1/01|AL|Fornecimento de alimentos preparados para empresas
5620-1/04|AL|Fornecimento de alimentos p/ consumo domiciliar
5822-1/01|T|Edição integrada à impressão de jornais
5920-1/00|T|Gravação de som/edição de música
6010-1/00|T|Atividades de rádio
6021-7/00|T|Televisão aberta
6110-8/01|T|Telefonia fixa comutada (STFC)
6110-8/03|T|Comunicação multimídia - SCM (telecom)
6120-5/01|T|Telefonia móvel celular
6120-5/99|T|Telecomunicações sem fio
6190-6/01|T|Provedores de acesso às redes de comunicações
6190-6/99|T|Outras atividades de telecomunicações n.e.
6201-5/01|T|Desenvolvimento de software sob encomenda
6202-3/00|T|Desenvolvimento/licenciamento de software customizável
6421-2/00|F|Bancos comerciais
6422-1/00|F|Bancos múltiplos, com carteira comercial
6423-9/00|F|Caixas econômicas
6424-7/02|F|Cooperativas centrais de crédito
6424-7/03|F|Cooperativas de crédito mútuo
6424-7/04|F|Cooperativas de crédito rural
6434-4/00|F|Agências de fomento
6463-8/00|F|Outras sociedades de participação (exceto holdings)
6499-9/00|F|Outras atividades de serviços financeiros n.e.
6550-2/00|F|Planos de saúde
6613-4/00|F|Administração de cartões de crédito
6810-2/00|IM|Atividades imobiliárias de imóveis próprios
6810-2/01|IM|Compra e venda de imóveis próprios
6810-2/02|IM|Aluguel de imóveis próprios
6821-8/01|IM|Corretagem na compra/venda e avaliação de imóveis
6822-6/00|IM|Gestão e administração da propriedade imobiliária
6911-7/01|S|Serviços advocatícios
6912-5/00|S|Cartórios
6920-6/01|S|Atividades de contabilidade
7020-4/00|S|Consultoria em gestão empresarial
7112-0/00|S|Serviços de engenharia
7119-7/01|S|Serviços de cartografia, topografia e geodésia
7311-4/00|S|Agências de publicidade
7420-0/01|S|Produção de fotografias
7490-1/01|S|Serviços de tradução e interpretação
7490-1/99|S|Outras atividades profissionais/técnicas n.e.
7500-1/00|SE|Atividades veterinárias
7711-0/00|S|Locação de automóveis sem condutor
7721-7/00|S|Aluguel de equipamentos recreativos e esportivos
7739-0/99|S|Aluguel de outras máquinas/equip. comerciais n.e.
7740-3/00|S|Gestão de ativos intangíveis não financeiros
7911-2/00|S|Agências de viagens
8012-9/00|S|Transporte de valores
8111-7/00|S|Apoio a edifícios (exceto condomínios)
8112-5/00|S|Condomínios prediais
8129-0/00|S|Atividades de limpeza n.e.
8211-3/00|S|Serviços de escritório/apoio administrativo
8230-0/01|S|Organização de feiras, congressos e exposições
8230-0/02|S|Casas de festas e eventos
8291-1/00|S|Cobrança e informações cadastrais
8299-7/01|S|Medição de consumo de energia, gás e água
8299-7/99|S|Serviços prestados às empresas n.e.
8511-2/00|SE|Educação infantil - creche
8512-1/00|SE|Educação infantil - pré-escola
8513-9/00|SE|Ensino fundamental
8520-1/00|SE|Ensino médio
8531-7/00|SE|Educação superior - graduação
8541-4/00|SE|Educação profissional de nível técnico
8599-6/04|SE|Treinamento profissional e gerencial
8599-6/05|SE|Cursos preparatórios para concursos
8599-6/99|SE|Outras atividades de ensino n.e.
8610-1/01|SE|Atendimento hospitalar
8630-5/01|SE|Atividade médica ambulatorial com procedimentos cirúrgicos
8630-5/03|SE|Atividade médica ambulatorial restrita a consultas
8630-5/04|SE|Atividade odontológica
8630-5/99|SE|Atenção ambulatorial n.e.
8640-2/01|SE|Laboratórios de anatomia patológica e citológica
8640-2/02|SE|Laboratórios clínicos
8640-2/06|SE|Serviços de ressonância magnética
8640-2/07|SE|Serviços de tomografia
8640-2/08|SE|Diagnóstico por imagem com radiação ionizante
8640-2/10|SE|Serviços de quimioterapia
8640-2/99|SE|Complementação diagnóstica e terapêutica n.e.
8690-9/99|SE|Outras atividades de atenção à saúde n.e.
8730-1/99|SP|Assistência social em residências coletivas n.e.
8800-6/00|SP|Serviços de assistência social sem alojamento
9001-9/00|C|Artes cênicas e espetáculos
9001-9/01|C|Produção teatral
9312-3/00|C|Clubes sociais e esportivos
9313-1/00|C|Academia (condicionamento físico)
9321-2/00|C|Parques de diversão/temáticos
9329-8/01|C|Discotecas, danceterias e similares
9411-1/00|SP|Organizações patronais e empresariais
9412-0/99|SP|Outras atividades associativas profissionais
9420-1/00|SP|Organizações sindicais
9430-8/00|SP|Associações de defesa de direitos sociais
9491-0/00|SP|Organizações religiosas/filosóficas
9499-5/00|SP|Atividades associativas n.e.
9521-5/00|SP|Reparação de eletroeletrônicos pessoais/domésticos
9601-7/01|SP|Lavanderias
9602-5/01|SP|Cabeleireiros, manicure e pedicure
9602-5/02|SP|Estética e cuidados com a beleza
9603-3/01|SP|Gestão e manutenção de cemitérios
9603-3/04|SP|Serviços de funerárias
9609-2/02|SP|Agências matrimoniais
9609-2/99|SP|Outras atividades de serviços pessoais n.e.
"""
CNAE = {}
for _l in _RAW.strip().splitlines():
    _c, _s, _d = _l.split("|")
    CNAE[_c.strip()] = (SET[_s.strip()], _d.strip())

def lookup(cod):
    """Devolve (setor, descricao). Faz fallback pela classe (4 digitos) e pela divisao."""
    if cod is None or str(cod).strip() == "":
        return CNAE["(vazio)"]
    c = str(cod).strip()
    if c in CNAE:
        return CNAE[c]
    # fallback: mesma classe (mesmos 6 primeiros caracteres, ex. '4711-3')
    pref = c[:6]
    for k, v in CNAE.items():
        if k.startswith(pref):
            return (v[0], v[1] + " (subclasse próxima)")
    # fallback: divisao (2 digitos)
    div = c[:2]
    DIV = {"01":"AG","02":"AG","03":"AG","05":"I","07":"I","08":"I","09":"I",
           "10":"I","11":"I","12":"I","13":"I","14":"I","15":"I","16":"I","17":"I","18":"I",
           "19":"I","20":"I","21":"I","22":"I","23":"I","24":"I","25":"I","26":"I","27":"I",
           "28":"I","29":"I","30":"I","31":"I","32":"I","33":"I","35":"EN","38":"O","39":"O",
           "41":"CO","42":"CO","43":"CO","45":"VE","46":"A","47":"V","49":"TR","50":"TR",
           "51":"TR","52":"TR","53":"TR","55":"H","56":"AL","58":"T","59":"T","60":"T","61":"T",
           "62":"T","63":"T","64":"F","65":"F","66":"F","68":"IM","69":"S","70":"S","71":"S",
           "72":"S","73":"S","74":"S","75":"SE","77":"S","78":"S","79":"S","80":"S","81":"S",
           "82":"S","85":"SE","86":"SE","87":"SP","88":"SP","90":"C","91":"C","92":"C","93":"C",
           "94":"SP","95":"SP","96":"SP","97":"SP","99":"O"}
    return (SET.get(DIV.get(div, "O"), "Outros"), "CNAE " + c)
