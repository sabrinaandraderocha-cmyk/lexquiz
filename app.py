from flask import Flask, render_template, request, redirect, url_for, session, flash
from whitenoise import WhiteNoise
import random
import secrets
import os

# =========================================================
# APP & CONFIGURAÇÕES
# =========================================================
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

# Configuração do WhiteNoise para arquivos estáticos no Render
root_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(root_dir, "static")

# serve /static no Render
if os.path.exists(static_dir):
    app.wsgi_app = WhiteNoise(app.wsgi_app, root=static_dir, prefix="static/")

# Chave secreta (Tenta pegar do ambiente, senão gera uma aleatória)
# Recomendado: definir SECRET_KEY no Render (Settings -> Environment)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(24)

APP_NAME = "LexQuiz"

AREAS = [
    "Direito Civil",
    "Direito Penal",
    "Direito Constitucional",
    "Processo Civil",
    "Processo Penal",
    "Ética"
]

# =========================================================
# BANCO DE QUESTÕES COMPLETO
# =========================================================
QUESTIONS = [
    # -------------------- DIREITO CIVIL --------------------
    {"id": 1, "area": "Direito Civil", "q": "A personalidade civil da pessoa começa, em regra:", "options": ["na concepção", "no nascimento com vida", "aos 18 anos", "no registro civil"], "answer": 1, "explain": "Em regra, a personalidade civil começa com o nascimento com vida."},
    {"id": 2, "area": "Direito Civil", "q": "Capacidade de direito é:", "options": ["aptidão para ser titular de direitos e deveres", "aptidão para praticar atos sozinho", "poder de representar alguém", "condição exclusiva de maiores de idade"], "answer": 0, "explain": "Capacidade de direito é a aptidão genérica para ter direitos e deveres."},
    {"id": 3, "area": "Direito Civil", "q": "Em regra, a maioridade civil ocorre aos:", "options": ["16 anos", "18 anos", "21 anos", "14 anos"], "answer": 1, "explain": "A regra geral é 18 anos para a maioridade civil."},
    {"id": 4, "area": "Direito Civil", "q": "Domicílio da pessoa natural, em regra, é:", "options": ["onde nasceu", "onde trabalha", "onde estabelece residência com ânimo definitivo", "onde tem família"], "answer": 2, "explain": "Domicílio, em regra, é a residência com intenção de permanência."},
    {"id": 5, "area": "Direito Civil", "q": "Pessoa jurídica é:", "options": ["qualquer pessoa maior de idade", "ente criado pela lei, com personalidade própria", "apenas órgão público", "apenas empresa com lucro"], "answer": 1, "explain": "Pessoa jurídica tem personalidade própria, distinta das pessoas que a compõem."},
    {"id": 6, "area": "Direito Civil", "q": "Bens móveis são, em regra:", "options": ["os que não podem ser transportados", "os que podem ser transportados sem alteração substancial", "somente imóveis", "somente dinheiro"], "answer": 1, "explain": "Bens móveis podem ser transportados sem alteração da substância."},
    {"id": 7, "area": "Direito Civil", "q": "Negócio jurídico é, em geral:", "options": ["qualquer conversa", "manifestação de vontade que produz efeitos jurídicos", "qualquer ato ilícito", "somente contrato escrito"], "answer": 1, "explain": "Negócio jurídico é manifestação de vontade com efeitos no mundo jurídico."},
    {"id": 8, "area": "Direito Civil", "q": "Um contrato, em regra, exige:", "options": ["acordo de vontades", "apenas assinatura em cartório", "sempre duas testemunhas", "sempre forma pública"], "answer": 0, "explain": "O essencial é o acordo de vontades, respeitada a forma exigida em casos específicos."},
    {"id": 9, "area": "Direito Civil", "q": "A boa-fé objetiva se relaciona a:", "options": ["um sentimento interno", "padrão de conduta leal e cooperativo", "direito penal", "apenas promessa verbal"], "answer": 1, "explain": "Boa-fé objetiva é padrão de conduta esperado nas relações jurídicas."},
    {"id": 10, "area": "Direito Civil", "q": "Responsabilidade civil, em regra, visa:", "options": ["punir com prisão", "reparar dano causado", "anular qualquer contrato", "criar imposto"], "answer": 1, "explain": "A responsabilidade civil tem foco na reparação do dano."},
    {"id": 11, "area": "Direito Civil", "q": "Ato ilícito no civil, em linhas gerais, é:", "options": ["qualquer ato imoral", "conduta que viola direito e causa dano", "qualquer ato sem assinatura", "somente crime"], "answer": 1, "explain": "Ato ilícito viola direito e pode gerar dever de indenizar."},
    {"id": 12, "area": "Direito Civil", "q": "Prescrição se relaciona a:", "options": ["perda do direito de ação pelo tempo", "perda do direito de propriedade automaticamente", "prisão do devedor", "regras eleitorais"], "answer": 0, "explain": "Prescrição é a perda da pretensão pelo decurso do tempo."},
    {"id": 13, "area": "Direito Civil", "q": "Decadência se relaciona a:", "options": ["perda de um direito potestativo pelo tempo", "pagamento de dívida", "prisão", "mudança de domicílio"], "answer": 0, "explain": "Decadência é a extinção de um direito pelo tempo, em regra direito potestativo."},
    {"id": 14, "area": "Direito Civil", "q": "Posse é:", "options": ["sempre propriedade", "poder de fato sobre a coisa", "apenas aluguel", "sempre registrada em cartório"], "answer": 1, "explain": "Posse é exercício, de fato, de poderes inerentes à propriedade."},
    {"id": 15, "area": "Direito Civil", "q": "Propriedade é, em geral:", "options": ["poder pleno sobre a coisa, com limitações legais", "apenas morar no imóvel", "apenas ter recibo", "igual a posse sempre"], "answer": 0, "explain": "Propriedade envolve usar, gozar, dispor e reaver, dentro dos limites da lei."},
    {"id": 16, "area": "Direito Civil", "q": "Obrigação é relação jurídica entre:", "options": ["Estado e juiz", "credor e devedor", "réu e promotor", "apenas empresas"], "answer": 1, "explain": "Obrigação liga credor e devedor, tendo por objeto uma prestação."},
    {"id": 17, "area": "Direito Civil", "q": "Adimplemento é:", "options": ["descumprimento da obrigação", "cumprimento da obrigação", "anulação do contrato", "crime"], "answer": 1, "explain": "Adimplemento é o cumprimento da prestação devida."},
    {"id": 18, "area": "Direito Civil", "q": "Inadimplemento é:", "options": ["cumprimento parcial com quitação", "descumprimento da obrigação", "transferência de propriedade", "mudança de domicílio"], "answer": 1, "explain": "Inadimplemento é o descumprimento, total ou parcial, da obrigação."},
    {"id": 19, "area": "Direito Civil", "q": "Contrato de compra e venda envolve, em regra:", "options": ["troca de favores", "transferência de bem mediante preço", "doação sem encargo", "prisão do vendedor"], "answer": 1, "explain": "Compra e venda: bem é transferido mediante pagamento de preço."},
    {"id": 20, "area": "Direito Civil", "q": "Doação é, em regra:", "options": ["transferência gratuita de bem", "compra parcelada", "contrato de trabalho", "pena alternativa"], "answer": 0, "explain": "Doação é transferência gratuita de patrimônio."},
    {"id": 101, "area": "Direito Civil", "q": "Na sucessão legítima, o cônjuge sobrevivente concorre com os descendentes, salvo se casado no regime de:", "options": ["Comunhão parcial (com bens particulares)", "Separação convencional", "Comunhão universal", "Participação final nos aquestos"], "answer": 2, "explain": "Na comunhão universal, o cônjuge já é meeiro de tudo, não herdeiro (salvo exceções complexas)."},
    {"id": 102, "area": "Direito Civil", "q": "O prazo para anular casamento por coação é de:", "options": ["2 anos", "4 anos", "180 dias", "3 anos"], "answer": 1, "explain": "O Código Civil (art. 1.560) estipula 4 anos para anulação por coação."},
    {"id": 103, "area": "Direito Civil", "q": "A usucapião extraordinária de bem imóvel exige posse ininterrupta por:", "options": ["5 anos", "10 anos", "15 anos", "20 anos"], "answer": 2, "explain": "A regra geral da extraordinária é 15 anos, independente de título e boa-fé."},
    {"id": 104, "area": "Direito Civil", "q": "Alimentos avoengos (pagos pelos avós) têm natureza:", "options": ["Solidária", "Subsidiária e complementar", "Principal", "Indenizatória"], "answer": 1, "explain": "Os avós só pagam se os pais não tiverem condições (subsidiária) ou para completar (complementar)."},
    {"id": 151, "area": "Direito Civil", "difficulty": "Média", "q": "Nas obrigações solidárias passivas, o pagamento parcial feito por um dos devedores e a remissão por ele obtida:", "options": ["Extinguem a dívida para todos", "Não aproveitam aos outros devedores", "Aproveitam aos outros até a concorrência da quantia paga ou relevada", "Tornam a obrigação indivisível"], "answer": 2, "explain": "Art. 277, CC: O pagamento parcial ou a remissão aproveitam aos outros devedores apenas até o montante pago ou perdoado."},
    {"id": 152, "area": "Direito Civil", "difficulty": "Fácil", "q": "A cláusula penal (multa contratual) não pode exceder:", "options": ["10% do valor do contrato", "O valor da obrigação principal", "O dobro da obrigação principal", "50 salários mínimos"], "answer": 1, "explain": "Art. 412, CC: O valor da cominação imposta na cláusula penal não pode exceder o da obrigação principal."},
    {"id": 153, "area": "Direito Civil", "difficulty": "Difícil", "q": "Na cessão de crédito onerosa, salvo disposição em contrário, o cedente responde:", "options": ["Pela solvência do devedor", "Pela existência do crédito ao tempo da cessão", "Solidariamente com o devedor", "Por nada"], "answer": 1, "explain": "Art. 295, CC: O cedente garante a existência do crédito (pro soluto), mas não a solvência do devedor (pro solvendo), salvo estipulação."},
    {"id": 154, "area": "Direito Civil", "difficulty": "Média", "q": "Ocorrendo a mora do credor (mora accipiendi), este:", "options": ["Não sofre consequências", "Sujeita o devedor a juros maiores", "Subtrai do devedor a responsabilidade pela conservação da coisa (salvo dolo)", "Pode exigir perdas e danos"], "answer": 2, "explain": "Art. 400, CC: A mora do credor isenta o devedor da responsabilidade pela conservação da coisa (salvo dolo) e o credor deve ressarcir despesas."},
    {"id": 155, "area": "Direito Civil", "difficulty": "Difícil", "q": "A Teoria do Adimplemento Substancial visa:", "options": ["Permitir o calote", "Impedir a resolução do contrato se o descumprimento for mínimo, restando apenas cobrança", "Anular o contrato", "Aumentar os juros"], "answer": 1, "explain": "Evita a resolução extrema do contrato quando a parte já cumpriu parcela muito expressiva da obrigação (Boa-fé objetiva)."},
    {"id": 156, "area": "Direito Civil", "difficulty": "Média", "q": "Na obrigação de dar coisa certa, se a coisa se perder sem culpa do devedor, antes da tradição:", "options": ["A obrigação se resolve para ambas as partes", "O devedor responde pelo equivalente", "O devedor paga perdas e danos", "O credor pode exigir outra coisa"], "answer": 0, "explain": "Art. 234, CC: Se a coisa se perder sem culpa do devedor, antes da tradição, fica resolvida a obrigação (volta-se ao status quo ante)."},
    {"id": 157, "area": "Direito Civil", "difficulty": "Média", "q": "A novação tem por efeito imediato:", "options": ["A confirmação da dívida antiga", "A extinção da dívida antiga e criação de uma nova", "A suspensão da prescrição", "O parcelamento da dívida"], "answer": 1, "explain": "Novação é a criação de uma obrigação nova para extinguir e substituir a anterior."},
    {"id": 158, "area": "Direito Civil", "difficulty": "Fácil", "q": "As arras (sinal) penitenciais servem para:", "options": ["Confirmar o negócio apenas", "Garantir o direito de arrependimento, servindo como indenização pré-fixada", "Pagar o advogado", "Impedir o arrependimento"], "answer": 1, "explain": "Se houver cláusula de arrependimento, as arras valem como indenização. Quem as deu perde; quem recebeu devolve em dobro."},
    {"id": 159, "area": "Direito Civil", "difficulty": "Fácil", "q": "Para que ocorra a compensação legal, as dívidas devem ser:", "options": ["Líquidas, vencidas e de coisas fungíveis", "Iliquidas e vincendas", "De qualquer natureza", "Apenas em dinheiro"], "answer": 0, "explain": "Art. 369, CC: Exige-se reciprocidade, liquidez, exigibilidade (vencidas) e fungibilidade."},
    {"id": 160, "area": "Direito Civil", "difficulty": "Média", "q": "Nas obrigações de resultado, o devedor:", "options": ["Só se obriga a ser prudente", "Obriga-se a alcançar determinado fim", "Não responde por culpa", "Sempre responde por caso fortuito"], "answer": 1, "explain": "Diferente da obrigação de meio (onde basta a diligência), na de resultado o fim deve ser atingido (ex: transporte, cirurgia plástica estética)."},

    # -------------------- DIREITO PENAL --------------------
    {"id": 21, "area": "Direito Penal", "q": "No conceito analítico, crime é:", "options": ["qualquer ilegalidade", "conduta típica, ilícita e culpável", "qualquer ato imoral", "somente o que dá prisão"], "answer": 1, "explain": "No conceito analítico, consideram-se tipicidade, ilicitude e culpabilidade."},
    {"id": 22, "area": "Direito Penal", "q": "Dolo ocorre quando o agente:", "options": ["age com negligência", "quer o resultado ou assume o risco", "não prevê o resultado", "age sem conduta"], "answer": 1, "explain": "Dolo: vontade dirigida ao resultado ou assunção do risco."},
    {"id": 23, "area": "Direito Penal", "q": "Culpa ocorre, em geral, por:", "options": ["imprudência, negligência ou imperícia", "planejamento", "vingança", "obediência à lei"], "answer": 0, "explain": "Culpa envolve violação do dever de cuidado."},
    {"id": 24, "area": "Direito Penal", "q": "Princípio da legalidade penal significa:", "options": ["não há crime sem lei anterior", "todo fato é crime", "o juiz cria crimes", "a vítima define a pena"], "answer": 0, "explain": "Exige lei anterior definindo crime e pena."},
    {"id": 25, "area": "Direito Penal", "q": "Tipo penal é, em geral:", "options": ["a sentença", "a descrição legal de uma conduta criminosa", "o inquérito", "o recurso"], "answer": 1, "explain": "Tipo penal descreve a conduta proibida e seus elementos."},
    {"id": 26, "area": "Direito Penal", "q": "Ilicitude, em geral, significa:", "options": ["conduta permitida", "contrariedade ao direito", "somente erro", "somente culpa"], "answer": 1, "explain": "Ilicitude é a contrariedade ao ordenamento, salvo causas de justificação."},
    {"id": 27, "area": "Direito Penal", "q": "Culpabilidade, em linhas gerais, relaciona-se a:", "options": ["capacidade de reprovação pessoal pela conduta", "apenas ao resultado", "apenas à vítima", "ao valor do bem"], "answer": 0, "explain": "Culpabilidade é juízo de reprovação pessoal, conforme pressupostos do sistema."},
    {"id": 28, "area": "Direito Penal", "q": "Crime consumado ocorre quando:", "options": ["o agente desistiu", "se reúnem todos os elementos do tipo", "o inquérito termina", "a denúncia é recebida"], "answer": 1, "explain": "Consumação: quando todos os elementos do tipo se realizam."},
    {"id": 29, "area": "Direito Penal", "q": "Tentativa ocorre quando:", "options": ["o agente inicia execução e não consuma por circunstâncias alheias", "o agente só pensa no crime", "a polícia investiga", "há confissão"], "answer": 0, "explain": "Tentativa: início de execução sem consumação por circunstâncias alheias."},
    {"id": 30, "area": "Direito Penal", "q": "Pena tem, em geral, finalidade:", "options": ["somente vingança", "reprovação e prevenção", "apenas indenizar", "apenas educar a vítima"], "answer": 1, "explain": "A pena é associada a reprovação e prevenção, entre outras funções discutidas."},
    {"id": 31, "area": "Direito Penal", "q": "Erro de tipo, em geral, afeta:", "options": ["a tipicidade subjetiva (dolo)", "a competência do juiz", "o inquérito", "a prescrição civil"], "answer": 0, "explain": "Erro de tipo costuma afastar o dolo e pode ter efeitos na culpa."},
    {"id": 32, "area": "Direito Penal", "q": "Crime doloso é aquele em que:", "options": ["há imprudência", "há intenção ou assunção de risco", "não há conduta", "sempre há culpa"], "answer": 1, "explain": "Doloso: vontade ou assunção de risco."},
    {"id": 33, "area": "Direito Penal", "q": "Crime culposo é aquele em que:", "options": ["há intenção", "há violação do dever de cuidado", "há legítima defesa sempre", "há confissão obrigatória"], "answer": 1, "explain": "Culposo: dever de cuidado violado, sem intenção."},
    {"id": 34, "area": "Direito Penal", "q": "Legítima defesa é causa de:", "options": ["aumento de pena", "exclusão da ilicitude", "exclusão do dolo", "competência do júri"], "answer": 1, "explain": "Legítima defesa é uma causa que, em regra, exclui a ilicitude."},
    {"id": 35, "area": "Direito Penal", "q": "Estado de necessidade é, em geral:", "options": ["causa de exclusão da ilicitude", "causa de prescrição", "crime mais grave", "recurso penal"], "answer": 0, "explain": "Estado de necessidade pode excluir a ilicitude, conforme requisitos."},
    {"id": 36, "area": "Direito Penal", "q": "A punibilidade se relaciona a:", "options": ["possibilidade de aplicar pena", "propriedade do bem", "processo civil", "registro civil"], "answer": 0, "explain": "Punibilidade: possibilidade de impor sanção penal ao caso."},
    {"id": 37, "area": "Direito Penal", "q": "O princípio da anterioridade penal exige:", "options": ["lei posterior ao fato", "lei anterior ao fato", "decisão do delegado", "aprovação da vítima"], "answer": 1, "explain": "A lei deve ser anterior ao fato para definir crime e pena."},
    {"id": 38, "area": "Direito Penal", "q": "O princípio da intervenção mínima indica que:", "options": ["o penal deve ser usado como última ratio", "qualquer problema vira crime", "penas sempre máximas", "prisão sempre"], "answer": 0, "explain": "O Direito Penal deve ser aplicado de forma subsidiária e fragmentária."},
    {"id": 39, "area": "Direito Penal", "q": "Concurso de pessoas, em geral, envolve:", "options": ["um agente sozinho", "pluralidade de agentes e vínculo para o fato", "somente vítima", "apenas juiz e promotor"], "answer": 1, "explain": "Envolve mais de um agente contribuindo para o fato, com vínculo."},
    {"id": 40, "area": "Direito Penal", "q": "Pena privativa de liberdade é:", "options": ["multa", "restrição de direitos", "prisão (regimes)", "indenização civil"], "answer": 2, "explain": "Privativa de liberdade envolve cumprimento em regime prisional."},
    {"id": 106, "area": "Direito Penal", "q": "O feminicídio é qualificadora do homicídio de natureza:", "options": ["Subjetiva", "Objetiva", "Mista", "Culposa"], "answer": 1, "explain": "É objetiva, pois incide sobre o fato de ser mulher (gênero), não sobre a motivação íntima do agente."},
    {"id": 107, "area": "Direito Penal", "q": "No crime de roubo, o emprego de arma de fogo de uso restrito ou proibido aplica-se:", "options": ["Aumento de 1/3", "Aumento de metade", "Dobro da pena", "Triplo da pena"], "answer": 2, "explain": "A Lei Anticrime alterou o CP: arma de uso restrito/proibido dobra a pena."},
    {"id": 108, "area": "Direito Penal", "q": "Apropriar-se de coisa alheia móvel, de que tem a posse ou a detenção, configura:", "options": ["Furto mediante fraude", "Estelionato", "Apropriação indébita", "Roubo"], "answer": 2, "explain": "O dolo surge depois de já ter a posse lícita da coisa."},
    {"id": 109, "area": "Direito Penal", "q": "Não se pune o aborto praticado por médico se:", "options": ["A gravidez resulta de estupro (com consentimento)", "A gestante é menor de 21 anos", "O pai da criança não quer", "A gestante está desempregada"], "answer": 0, "explain": "Aborto sentimental/humanitário (caso de estupro) e necessário (risco de vida) são permitidos."},
    {"id": 110, "area": "Direito Penal", "q": "A corrupção passiva é crime praticado por:", "options": ["Particular contra administração", "Funcionário público", "Juiz apenas", "Advogado"], "answer": 1, "explain": "Corrupção passiva é crime funcional (praticado por funcionário público)."},
    {"id": 136, "area": "Direito Penal", "difficulty": "Fácil", "q": "A ação penal pública é promovida pelo Ministério Público e, salvo disposição em contrário, é:", "options": ["Condicionada à requisição", "Privada", "Incondicionada", "Subsidiária"], "answer": 2, "explain": "Art. 100, CP: A ação penal é pública, salvo quando a lei declara privativa do ofendido. A regra é ser incondicionada."},
    {"id": 137, "area": "Direito Penal", "difficulty": "Média", "q": "O direito de queixa ou de representação decai se não exercido no prazo de:", "options": ["3 meses", "6 meses", "1 ano", "2 anos"], "answer": 1, "explain": "Art. 103, CP: O prazo decadencial é de 6 meses, contados do dia em que veio a saber quem é o autor do crime."},
    {"id": 138, "area": "Direito Penal", "difficulty": "Média", "q": "Na ação penal privada, o perdão do ofendido:", "options": ["Independe de aceitação do querelado", "Aproveita a todos os querelados, se concedido a um", "Não obsta o prosseguimento da ação", "Só pode ser expresso"], "answer": 1, "explain": "Art. 106, I, CP: O perdão concedido a um dos querelados aproveita a todos (princípio da indivisibilidade)."},
    {"id": 139, "area": "Direito Penal", "difficulty": "Difícil", "q": "O perdão do ofendido, para extinguir a punibilidade, exige:", "options": ["Sentença transitada em julgado", "Aceitação do querelado (réu)", "Pagamento de custas", "Concordância do Ministério Público"], "answer": 1, "explain": "Art. 105, CP: O perdão é ato bilateral; só produz efeito se o querelado o aceitar."},
    {"id": 140, "area": "Direito Penal", "difficulty": "Fácil", "q": "Dentre as causas de extinção da punibilidade (Art. 107), NÃO se inclui:", "options": ["Morte do agente", "Anistia, graça ou indulto", "Prisão preventiva", "Prescrição, decadência ou perempção"], "answer": 2, "explain": "Prisão preventiva é medida cautelar processual, não extingue a punibilidade do crime."},
    {"id": 141, "area": "Direito Penal", "difficulty": "Média", "q": "A prescrição, antes de transitar em julgado a sentença final, regula-se:", "options": ["Pelo máximo da pena privativa de liberdade cominada ao crime", "Pela pena mínima", "Pela média das penas", "Pela pena aplicada na sentença provisória"], "answer": 0, "explain": "Art. 109, CP: Antes da sentença final, regula-se pelo máximo da pena em abstrato prevista na lei."},
    {"id": 142, "area": "Direito Penal", "difficulty": "Difícil", "q": "São reduzidos de metade os prazos de prescrição quando o criminoso era, ao tempo do crime:", "options": ["Menor de 18 anos", "Menor de 21 anos", "Maior de 60 anos", "Réu primário"], "answer": 1, "explain": "Art. 115, CP: Reduz-se pela metade se menor de 21 anos (na data do fato) ou maior de 70 (na data da sentença)."},
    {"id": 143, "area": "Direito Penal", "difficulty": "Média", "q": "A renúncia ao direito de queixa em relação a um dos autores do crime:", "options": ["A todos se estende", "Só vale para aquele que foi perdoado", "Extingue a ação penal pública", "Depende de aceitação"], "answer": 0, "explain": "Art. 104, CP: A renúncia é ato unilateral e, pelo princípio da indivisibilidade, estende-se a todos os autores."},
    {"id": 144, "area": "Direito Penal", "difficulty": "Média", "q": "O curso da prescrição interrompe-se:", "options": ["Pelo oferecimento da denúncia", "Pelo recebimento da denúncia ou queixa", "Pela citação do réu", "Pelo inquérito policial"], "answer": 1, "explain": "Art. 117, I, CP: O marco interruptivo é o RECEBIMENTO da denúncia, não o oferecimento ou a citação."},
    {"id": 145, "area": "Direito Penal", "difficulty": "Difícil", "q": "No caso de evasão do condenado ou de revogação do livramento condicional, a prescrição regula-se:", "options": ["Pela pena total da sentença", "Pelo tempo que resta da pena", "Pela pena máxima em abstrato", "Não há prescrição"], "answer": 1, "explain": "Art. 113, CP: Regula-se pelo tempo que RESTA da pena a cumprir."},
    {"id": 146, "area": "Direito Penal", "difficulty": "Fácil", "q": "A morte do agente (Art. 107, I) gera:", "options": ["Suspensão do processo", "Absolvição sumária", "Extinção da punibilidade", "Nulidade do processo"], "answer": 2, "explain": "Mors omnia solvit. A morte do agente extingue o poder de punir do Estado imediatamente."},
    {"id": 147, "area": "Direito Penal", "difficulty": "Média", "q": "O perdão judicial (Art. 107, IX) somente pode ser concedido:", "options": ["Em qualquer crime", "Nos casos previstos em lei", "A pedido do MP", "Se o réu for primário"], "answer": 1, "explain": "O perdão judicial não é genérico; só se aplica nas hipóteses expressamente previstas em lei (ex: homicídio culposo)."},
    {"id": 148, "area": "Direito Penal", "difficulty": "Difícil", "q": "A 'abolitio criminis' (lei posterior que deixa de considerar o fato crime):", "options": ["Não retroage", "Cessa a execução e os efeitos penais da condenação", "Mantém a reincidência", "Só extingue a pena de multa"], "answer": 1, "explain": "Art. 107, III, CP: A abolitio criminis apaga tudo (efeitos penais), inclusive a reincidência. Só permanecem efeitos civis."},
    {"id": 149, "area": "Direito Penal", "difficulty": "Média", "q": "A perempção (Art. 107, IV) é causa de extinção da punibilidade que ocorre apenas:", "options": ["Na ação penal pública", "Na ação penal privada", "Nos crimes hediondos", "No tribunal do júri"], "answer": 1, "explain": "A perempção é sanção à inércia ou negligência do querelante exclusivamente na ação penal privada."},
    {"id": 150, "area": "Direito Penal", "difficulty": "Fácil", "q": "Se a pena máxima privativa de liberdade é superior a 12 anos, a prescrição ocorre em:", "options": ["10 anos", "15 anos", "20 anos", "30 anos"], "answer": 2, "explain": "Art. 109, I, CP: Prescreve em 20 anos se o máximo da pena é superior a 12."},

    # -------------------- DIREITO CONSTITUCIONAL --------------------
    {"id": 41, "area": "Direito Constitucional", "q": "A Constituição Federal de 1988 é considerada:", "options": ["flexível", "rígida", "costumeira", "não escrita"], "answer": 1, "explain": "É rígida porque tem procedimento mais difícil para alteração."},
    {"id": 42, "area": "Direito Constitucional", "q": "Fundamento da República Federativa do Brasil:", "options": ["ampla defesa", "dignidade da pessoa humana", "coisa julgada", "competência"], "answer": 1, "explain": "Dignidade da pessoa humana é fundamento (art. 1º, CF)."},
    {"id": 43, "area": "Direito Constitucional", "q": "Separação dos Poderes envolve:", "options": ["Legislativo, Executivo e Judiciário", "MP, Defensoria e OAB", "União, Estados e Municípios", "Congresso, STF e Polícia"], "answer": 0, "explain": "A separação clássica envolve Legislativo, Executivo e Judiciário."},
    {"id": 44, "area": "Direito Constitucional", "q": "Direitos e garantias fundamentais estão principalmente no:", "options": ["preâmbulo", "art. 1º", "art. 5º", "ADCT"], "answer": 2, "explain": "O art. 5º é o núcleo de direitos e garantias fundamentais."},
    {"id": 45, "area": "Direito Constitucional", "q": "O Brasil é um Estado:", "options": ["unitário", "federativo", "confederado", "absolutista"], "answer": 1, "explain": "O Brasil é uma federação."},
    {"id": 46, "area": "Direito Constitucional", "q": "Cláusulas pétreas, em geral, são:", "options": ["temas proibidos de emenda", "leis ordinárias", "decretos", "portarias"], "answer": 0, "explain": "Cláusulas pétreas são limites materiais à reforma constitucional."},
    {"id": 47, "area": "Direito Constitucional", "q": "A nacionalidade é tema de:", "options": ["Direito Civil", "Constitucional", "Penal", "Processo Penal"], "answer": 1, "explain": "A CF trata de nacionalidade."},
    {"id": 48, "area": "Direito Constitucional", "q": "Direitos sociais incluem, por exemplo:", "options": ["saúde e educação", "prisão preventiva", "impostos", "habeas data apenas"], "answer": 0, "explain": "Direitos sociais incluem saúde, educação, trabalho, moradia etc."},
    {"id": 49, "area": "Direito Constitucional", "q": "Controle de constitucionalidade serve para:", "options": ["julgar crimes", "verificar compatibilidade de normas com a Constituição", "registrar contratos", "fazer inquérito"], "answer": 1, "explain": "É o exame de compatibilidade das normas com a CF."},
    {"id": 50, "area": "Direito Constitucional", "q": "O voto no Brasil, em regra, é:", "options": ["secreto e direto", "público e indireto", "apenas simbólico", "facultativo para todos"], "answer": 0, "explain": "A regra geral é voto direto e secreto, com variações por idade."},
    {"id": 51, "area": "Direito Constitucional", "q": "O princípio da legalidade (administração) indica que:", "options": ["a administração só faz o que a lei permite", "a administração faz o que quiser", "a lei é opcional", "o juiz cria a lei"], "answer": 0, "explain": "Na administração pública, legalidade é atuação vinculada à lei."},
    {"id": 52, "area": "Direito Constitucional", "q": "O princípio da publicidade se relaciona a:", "options": ["sigilo total", "transparência dos atos públicos", "prisão automática", "privacidade do Estado"], "answer": 1, "explain": "Publicidade garante transparência, com exceções legais."},
    {"id": 53, "area": "Direito Constitucional", "q": "Habeas corpus protege:", "options": ["direito de ir e vir", "direito de propriedade", "direito ao voto", "direito autoral"], "answer": 0, "explain": "Habeas corpus protege liberdade de locomoção."},
    {"id": 54, "area": "Direito Constitucional", "q": "Mandado de segurança, em geral, protege:", "options": ["liberdade de locomoção", "direito líquido e certo", "direitos difusos ambientais", "herança"], "answer": 1, "explain": "MS protege direito líquido e certo contra ilegalidade/abuso."},
    {"id": 55, "area": "Direito Constitucional", "q": "A forma de Estado do Brasil é:", "options": ["república", "monarquia", "federativa", "parlamentarista"], "answer": 2, "explain": "Forma de Estado é federativa."},
    {"id": 56, "area": "Direito Constitucional", "q": "A forma de governo do Brasil é:", "options": ["república", "monarquia", "confederação", "anarquia"], "answer": 0, "explain": "Forma de governo é República."},
    {"id": 57, "area": "Direito Constitucional", "q": "Soberania é:", "options": ["poder supremo do Estado", "poder do município", "poder do juiz", "poder de empresa privada"], "answer": 0, "explain": "Soberania é atributo do Estado perante si e externamente."},
    {"id": 58, "area": "Direito Constitucional", "q": "Cidadania é, em geral:", "options": ["apenas nacionalidade", "participação política e direitos do cidadão", "apenas ter CPF", "apenas morar no Brasil"], "answer": 1, "explain": "Cidadania relaciona-se a participação e direitos políticos."},
    {"id": 59, "area": "Direito Constitucional", "q": "Dignidade da pessoa humana é:", "options": ["fundamento constitucional", "regra de trânsito", "pena criminal", "recurso processual"], "answer": 0, "explain": "É fundamento da República."},
    {"id": 60, "area": "Direito Constitucional", "q": "O devido processo legal significa, em geral:", "options": ["processo sem regras", "garantias de procedimento justo", "decisão sem defesa", "prisão automática"], "answer": 1, "explain": "Devido processo legal exige procedimento adequado e garantias."},
    {"id": 111, "area": "Direito Constitucional", "q": "Compete privativamente ao Senado Federal:", "options": ["Iniciar lei de orçamento", "Aprovar escolha de Ministros do STF", "Julgar contas do Presidente", "Criar CPI mista"], "answer": 1, "explain": "A sabatina e aprovação de autoridades é competência do Senado."},
    {"id": 112, "area": "Direito Constitucional", "q": "A ADI (Ação Direta de Inconstitucionalidade) é julgada pelo:", "options": ["STJ", "STF", "Congresso Nacional", "Senado"], "answer": 1, "explain": "Controle concentrado de constitucionalidade federal é competência do STF."},
    {"id": 113, "area": "Direito Constitucional", "q": "São legitimados para propor ADI, EXCETO:", "options": ["Presidente da República", "OAB (Conselho Federal)", "Juiz de 1º grau", "Partido Político com representação no Congresso"], "answer": 2, "explain": "Juízes singulares realizam controle difuso, não podem propor ADI (controle concentrado)."},
    {"id": 114, "area": "Direito Constitucional", "q": "É cláusula pétrea (não pode ser abolida):", "options": ["O voto obrigatório", "O voto secreto", "A reeleição", "O número de deputados"], "answer": 1, "explain": "O voto direto, secreto, universal e periódico é cláusula pétrea. A obrigatoriedade não é."},
    {"id": 115, "area": "Direito Constitucional", "q": "Medida Provisória tem força de lei e vigência inicial de:", "options": ["30 dias", "45 dias", "60 dias", "90 dias"], "answer": 2, "explain": "60 dias, prorrogáveis por mais 60 (total 120 dias)."},
    {"id": 161, "area": "Direito Constitucional", "difficulty": "Fácil", "q": "Compete privativamente à União legislar sobre:", "options": ["Direito Civil, Penal e Processual", "Saúde e Meio Ambiente", "Junta Comercial", "Gás Canalizado"], "answer": 0, "explain": "Art. 22, CF: Legislar sobre direito civil, comercial, penal, processual, eleitoral, agrário, marítimo, aeronáutico, espacial e do trabalho é competência privativa da União."},
    {"id": 162, "area": "Direito Constitucional", "difficulty": "Fácil", "q": "Cuidar da saúde e assistência pública, da proteção e garantia das pessoas portadoras de deficiência é competência:", "options": ["Privativa da União", "Exclusiva dos Estados", "Comum da União, Estados, DF e Municípios", "Apenas dos Municípios"], "answer": 2, "explain": "Art. 23, CF: Competência material comum (todos os entes devem atuar)."},
    {"id": 163, "area": "Direito Constitucional", "difficulty": "Média", "q": "Legislar sobre previdência social, proteção e defesa da saúde é competência:", "options": ["Privativa da União", "Concorrente da União, Estados e DF", "Exclusiva da União", "Apenas dos Municípios"], "answer": 1, "explain": "Art. 24, CF: Competência legislativa concorrente. A União faz normas gerais e os Estados suplementam."},
    {"id": 164, "area": "Direito Constitucional", "difficulty": "Fácil", "q": "Compete aos Municípios legislar sobre:", "options": ["Assuntos de interesse local", "Trânsito e transporte", "Direito do Trabalho", "Energia"], "answer": 0, "explain": "Art. 30, CF: Compete aos Municípios legislar sobre assuntos de interesse local e suplementar a legislação federal/estadual no que couber."},
    {"id": 165, "area": "Direito Constitucional", "difficulty": "Média", "q": "A criação de novos Municípios depende de:", "options": ["Lei Federal", "Lei Estadual, após plebiscito", "Decreto do Governador", "Decisão do STF"], "answer": 1, "explain": "Art. 18, § 4º: Far-se-á por lei estadual, dentro do período determinado por Lei Complementar Federal, e dependerá de consulta prévia, mediante plebiscito."},
    {"id": 166, "area": "Direito Constitucional", "difficulty": "Média", "q": "São bens da União:", "options": ["As águas superficiais ou subterrâneas", "Os recursos minerais, inclusive os do subsolo", "As ilhas fluviais em zonas não fronteiriças", "As terras devolutas estaduais"], "answer": 1, "explain": "Art. 20, IX: Os recursos minerais, inclusive os do subsolo, são bens da União."},
    {"id": 167, "area": "Direito Constitucional", "difficulty": "Difícil", "q": "Legislar sobre populações indígenas é competência:", "options": ["Privativa da União", "Concorrente", "Dos Estados onde houver tribos", "Comum"], "answer": 0, "explain": "Art. 22, XIV: Competência privativa da União."},
    {"id": 168, "area": "Direito Constitucional", "difficulty": "Difícil", "q": "A competência dos Estados é caracterizada como:", "options": ["Taxativa", "Residual (ou remanescente)", "Implícita", "Absoluta"], "answer": 1, "explain": "Art. 25, § 1º: São reservadas aos Estados as competências que não lhes sejam vedadas por esta Constituição (competência residual)."},
    {"id": 169, "area": "Direito Constitucional", "difficulty": "Fácil", "q": "Ao Distrito Federal são atribuídas as competências legislativas:", "options": ["Apenas dos Estados", "Apenas dos Municípios", "Reservadas aos Estados e aos Municípios", "Apenas da União"], "answer": 2, "explain": "Art. 32, § 1º: Ao DF são atribuídas as competências legislativas reservadas aos Estados e Municípios (natureza híbrida)."},
    {"id": 170, "area": "Direito Constitucional", "difficulty": "Média", "q": "Legislar sobre trânsito e transporte é competência:", "options": ["Dos Municípios", "Dos Estados", "Privativa da União", "Concorrente"], "answer": 2, "explain": "Art. 22, XI: Privativa da União. O Município legisla apenas sobre o 'trânsito local' (estacionamento, circulação, sentido de via), mas as normas gerais (CTB) são federais."},

    # -------------------- PROCESSO CIVIL --------------------
    {"id": 61, "area": "Processo Civil", "q": "O processo civil busca, em geral:", "options": ["punir com prisão", "tutelar direitos e resolver conflitos", "eleger representantes", "aplicar multas administrativas sempre"], "answer": 1, "explain": "Processo civil tutela direitos em conflitos, com garantias processuais."},
    {"id": 62, "area": "Processo Civil", "q": "Citação é o ato de:", "options": ["punir o réu", "chamar o réu ao processo e dar ciência da demanda", "encerrar o processo", "criar lei"], "answer": 1, "explain": "Citação chama o réu e inicia a relação processual de forma válida."},
    {"id": 63, "area": "Processo Civil", "q": "O contraditório envolve, em geral:", "options": ["silêncio das partes", "participação e possibilidade de influenciar a decisão", "decisão surpresa", "apenas falar por último"], "answer": 1, "explain": "Contraditório é participação efetiva, não só formal."},
    {"id": 64, "area": "Processo Civil", "q": "Ampla defesa significa:", "options": ["defesa limitada", "uso dos meios de defesa admitidos", "defesa só por escrito", "defesa só por advogado público"], "answer": 1, "explain": "Ampla defesa permite meios e recursos adequados, conforme lei."},
    {"id": 65, "area": "Processo Civil", "q": "Competência absoluta pode ser reconhecida:", "options": ["apenas se a parte pedir", "de ofício pelo juiz", "só na sentença", "nunca"], "answer": 1, "explain": "Competência absoluta pode ser conhecida de ofício."},
    {"id": 66, "area": "Processo Civil", "q": "Petição inicial serve para:", "options": ["apresentar o pedido e fundamentos", "apresentar sentença", "fazer recurso", "fazer investigação penal"], "answer": 0, "explain": "A inicial traz pedido, causa de pedir e requisitos."},
    {"id": 67, "area": "Processo Civil", "q": "Sentença é, em geral:", "options": ["decisão que encerra fase de conhecimento em 1º grau", "qualquer despacho", "apenas prova", "apenas recurso"], "answer": 0, "explain": "Sentença normalmente encerra a fase de conhecimento ou extingue execução."},
    {"id": 68, "area": "Processo Civil", "q": "Recurso é usado para:", "options": ["criar lei", "impugnar decisão judicial", "citar o réu", "registrar imóvel"], "answer": 1, "explain": "Recurso visa reexaminar decisões, conforme hipóteses legais."},
    {"id": 69, "area": "Processo Civil", "q": "Prova testemunhal é:", "options": ["prova por documento", "depoimento de pessoas sobre fatos", "perícia", "confissão por escrito sempre"], "answer": 1, "explain": "Testemunhas relatam fatos relevantes ao processo."},
    {"id": 70, "area": "Processo Civil", "q": "Perícia é, em geral:", "options": ["análise técnica por especialista", "apenas depoimento", "decisão do juiz", "um tipo de citação"], "answer": 0, "explain": "Perícia produz prova técnica quando o juiz precisa de conhecimento especializado."},
    {"id": 71, "area": "Processo Civil", "q": "Tutela provisória serve para:", "options": ["resolver tudo no final", "proteger direito com urgência ou evidência", "prender réu", "punir advogado"], "answer": 1, "explain": "Tutela provisória antecipa ou assegura proteção antes do final."},
    {"id": 72, "area": "Processo Civil", "q": "Coisa julgada é:", "options": ["decisão provisória", "imutabilidade da decisão após trânsito em julgado", "um despacho", "um contrato"], "answer": 1, "explain": "Coisa julgada torna a decisão estável após o trânsito em julgado."},
    {"id": 73, "area": "Processo Civil", "q": "Ônus da prova, em geral, é:", "options": ["dever de pagar custas", "responsabilidade de provar alegações", "dever de prender", "direito do juiz"], "answer": 1, "explain": "Cada parte, em regra, prova o que alega, conforme distribuição legal."},
    {"id": 74, "area": "Processo Civil", "q": "Audiência de conciliação tem objetivo de:", "options": ["prender o réu", "buscar acordo entre as partes", "julgar recurso", "fazer perícia"], "answer": 1, "explain": "Visa estimular autocomposição, quando cabível."},
    {"id": 75, "area": "Processo Civil", "q": "Despacho é, em geral:", "options": ["decisão de mérito", "ato de impulso processual", "sentença penal", "acórdão"], "answer": 1, "explain": "Despacho normalmente impulsiona o processo, sem decidir mérito."},
    {"id": 76, "area": "Processo Civil", "q": "Decisão interlocutória é, em geral:", "options": ["sentença final", "decisão no curso do processo sobre questão incidental", "apenas despacho", "apenas acordo"], "answer": 1, "explain": "Interlocutória decide questões durante o processo."},
    {"id": 77, "area": "Processo Civil", "q": "A competência territorial, em regra, é:", "options": ["absoluta sempre", "relativa", "inexistente", "penal"], "answer": 1, "explain": "Em regra, competência territorial é relativa."},
    {"id": 78, "area": "Processo Civil", "q": "Mediação e conciliação são formas de:", "options": ["autocomposição", "pena alternativa", "investigação", "prova pericial"], "answer": 0, "explain": "São métodos consensuais para solução de conflitos."},
    {"id": 79, "area": "Processo Civil", "q": "O autor é, em geral, quem:", "options": ["apresenta a demanda", "julga", "defende o réu", "investiga crime"], "answer": 0, "explain": "Autor propõe a ação."},
    {"id": 80, "area": "Processo Civil", "q": "O réu é, em geral, quem:", "options": ["propõe a ação", "é demandado", "julga", "faz a lei"], "answer": 1, "explain": "Réu é quem sofre a demanda (demandado)."},
    {"id": 116, "area": "Processo Civil", "q": "O prazo geral para interposição de recursos no CPC/2015 é de:", "options": ["10 dias", "5 dias", "15 dias", "20 dias"], "answer": 2, "explain": "Regra geral: 15 dias úteis. Exceção: Embargos (5 dias)."},
    {"id": 117, "area": "Processo Civil", "q": "Contra decisão interlocutória que versa sobre tutelas provisórias cabe:", "options": ["Apelação", "Agravo de Instrumento", "Recurso Inominado", "Embargos Infringentes"], "answer": 1, "explain": "Decisões interlocutórias do rol do art. 1.015 (como tutelas) desafiam Agravo de Instrumento."},
    {"id": 118, "area": "Processo Civil", "q": "A contagem dos prazos processuais no CPC se dá em:", "options": ["Dias corridos", "Dias úteis", "Semanas", "Meses"], "answer": 1, "explain": "O CPC/15 inovou ao estabelecer a contagem apenas em dias úteis."},
    {"id": 119, "area": "Processo Civil", "q": "Não havendo bens penhoráveis, a execução será:", "options": ["Extinta imediatamente", "Suspensa", "Transformada em prisão", "Transferida para a União"], "answer": 1, "explain": "O juiz suspende a execução (prescrição intercorrente pode começar a correr)."},
    {"id": 120, "area": "Processo Civil", "q": "O juízo de admissibilidade da Apelação é feito:", "options": ["Pelo juiz de 1º grau", "Apenas pelo Tribunal (2º grau)", "Pelo escrivão", "Pelo MP"], "answer": 1, "explain": "No CPC/15, o juiz de 1º grau não faz admissibilidade; remete direto ao Tribunal."},

    # -------------------- PROCESSO PENAL --------------------
    {"id": 81, "area": "Processo Penal", "q": "Presunção de inocência significa:", "options": ["culpado desde a denúncia", "ninguém é considerado culpado até trânsito em julgado", "culpado no flagrante sempre", "só vale para réu primário"], "answer": 1, "explain": "A regra é não considerar culpado até o trânsito em julgado."},
    {"id": 82, "area": "Processo Penal", "q": "Inquérito policial é, em geral:", "options": ["fase do julgamento", "procedimento investigativo", "sentença", "recurso"], "answer": 1, "explain": "O inquérito é procedimento para apurar autoria e materialidade."},
    {"id": 83, "area": "Processo Penal", "q": "A ação penal pública, em regra, é proposta pelo:", "options": ["juiz", "delegado", "Ministério Público", "advogado da vítima"], "answer": 2, "explain": "Em regra, o MP é o titular da ação penal pública."},
    {"id": 84, "area": "Processo Penal", "q": "Finalidade do processo penal é:", "options": ["resolver contrato", "apurar infração penal e aplicar a lei com garantias", "registrar imóvel", "criar leis"], "answer": 1, "explain": "Busca apuração e julgamento, respeitando garantias."},
    {"id": 85, "area": "Processo Penal", "q": "Denúncia é, em geral:", "options": ["peça inicial do MP", "sentença", "recurso", "prova pericial"], "answer": 0, "explain": "Denúncia é a peça inicial da ação penal pública."},
    {"id": 86, "area": "Processo Penal", "q": "Queixa-crime é, em geral:", "options": ["peça do particular", "sentença", "inquérito", "prisão"], "answer": 0, "explain": "Na ação penal privada, o particular propõe a queixa-crime."},
    {"id": 87, "area": "Processo Penal", "q": "Contraditório no processo penal significa:", "options": ["decisão sem ouvir defesa", "direito de se manifestar e participar", "apenas falar no final", "somente acusação fala"], "answer": 1, "explain": "Contraditório implica participação e ciência dos atos."},
    {"id": 88, "area": "Processo Penal", "q": "Ampla defesa inclui:", "options": ["apenas defesa técnica", "defesa técnica e autodefesa, quando cabível", "apenas silêncio", "apenas recursos"], "answer": 1, "explain": "Abrange defesa por advogado e participação do acusado, conforme regras."},
    {"id": 89, "area": "Processo Penal", "q": "Prova no processo penal deve ser, em geral:", "options": ["ilícita sempre", "lícita e produzida com garantias", "secreta sempre", "dispensável"], "answer": 1, "explain": "Provas devem respeitar legalidade e garantias."},
    {"id": 90, "area": "Processo Penal", "q": "Juiz imparcial significa:", "options": ["juiz ajuda acusação", "juiz decide sem favoritismo", "juiz decide por amizade", "juiz sempre condena"], "answer": 1, "explain": "Imparcialidade é condição de validade e justiça do julgamento."},
    {"id": 91, "area": "Processo Penal", "q": "Prisão em flagrante ocorre quando:", "options": ["após trânsito em julgado", "alguém é surpreendido cometendo crime ou logo após", "antes do fato", "apenas com sentença"], "answer": 1, "explain": "Flagrante tem hipóteses relacionadas ao momento do fato."},
    {"id": 92, "area": "Processo Penal", "q": "Prisão preventiva é, em geral:", "options": ["pena definitiva", "medida cautelar antes do fim do processo", "multa", "perdão judicial"], "answer": 1, "explain": "É cautelar, não é pena, e depende de requisitos legais."},
    {"id": 93, "area": "Processo Penal", "q": "Audiência de instrução serve para:", "options": ["produzir provas (oitivas etc.)", "registrar imóveis", "eleger representantes", "aplicar multa tributária"], "answer": 0, "explain": "Na instrução, em geral, colhem-se provas e depoimentos."},
    {"id": 94, "area": "Processo Penal", "q": "Sentença penal condenatória, em geral, ocorre quando:", "options": ["não há prova", "há prova suficiente e tipicidade, ilicitude e culpabilidade", "sempre automaticamente", "a vítima pede"], "answer": 1, "explain": "A condenação pressupõe provas e requisitos do delito, além de regras processuais."},
    {"id": 95, "area": "Processo Penal", "q": "Recurso no processo penal serve para:", "options": ["investigar", "impugnar decisão judicial", "citar", "fazer perícia"], "answer": 1, "explain": "Recurso pede reexame de decisões, conforme previsão legal."},
    {"id": 96, "area": "Processo Penal", "q": "O Ministério Público, em regra, atua como:", "options": ["juiz", "defesa", "acusação na ação penal pública", "perito"], "answer": 2, "explain": "Em regra, o MP é o titular da ação penal pública e atua na acusação."},
    {"id": 97, "area": "Processo Penal", "q": "A defesa técnica é feita por:", "options": ["delegado", "advogado/defensor", "perito", "testemunha"], "answer": 1, "explain": "Defesa técnica é exercida por advogado ou defensor."},
    {"id": 98, "area": "Processo Penal", "q": "O juiz, no sistema acusatório, deve:", "options": ["investigar e acusar", "manter imparcialidade e julgar", "ser parte", "decidir sem ouvir ninguém"], "answer": 1, "explain": "O juiz julga com imparcialidade, sem assumir papel de acusação."},
    {"id": 99, "area": "Processo Penal", "q": "A vítima, em regra, é:", "options": ["titular da ação penal pública", "sempre quem acusa", "ofendido pelo delito", "juiz do caso"], "answer": 2, "explain": "Vítima é o ofendido, com direitos e participação conforme lei."},
    {"id": 100, "area": "Processo Penal", "q": "O princípio do in dubio pro reo indica que:", "options": ["na dúvida, condena", "na dúvida, absolve", "na dúvida, multa", "na dúvida, arquiva sempre"], "answer": 1, "explain": "Dúvida razoável favorece o acusado, conforme lógica garantista."},
    {"id": 121, "area": "Processo Penal", "q": "No Tribunal do Júri, a primeira fase encerra-se com a:", "options": ["Condenação", "Pronúncia (ou impronúncia/absolvição/desclassificação)", "Sentença de mérito", "Pena"], "answer": 1, "explain": "A pronúncia admite a acusação e envia o réu para o Plenário (2ª fase)."},
    {"id": 122, "area": "Processo Penal", "q": "Não se admite prisão preventiva:", "options": ["Para garantia da ordem pública", "Para assegurar a lei penal", "Como antecipação de pena", "Por conveniência da instrução"], "answer": 2, "explain": "A prisão preventiva é cautelar. É inconstitucional usá-la como cumprimento antecipado de pena."},
    {"id": 123, "area": "Processo Penal", "q": "O inquérito policial nos crimes de ação penal pública é:", "options": ["Indispensável", "Dispensável", "Obrigatório para o juiz", "Vinculante"], "answer": 1, "explain": "É dispensável se o MP já tiver elementos suficientes para oferecer a denúncia."},
    {"id": 124, "area": "Processo Penal", "q": "A competência para julgar crimes dolosos contra a vida é do:", "options": ["Juiz Singular", "Tribunal do Júri", "Justiça Federal sempre", "Juizado Especial"], "answer": 1, "explain": "Competência constitucional do Tribunal do Júri."},
    {"id": 125, "area": "Processo Penal", "q": "Em relação à cadeia de custódia da prova, é correto afirmar:", "options": ["É mera burocracia", "Visa garantir a idoneidade e rastreabilidade da prova", "Só se aplica a documentos", "Foi revogada"], "answer": 1, "explain": "Fundamental para assegurar que a prova não foi alterada desde a coleta até o processo."},

    # -------------------- ÉTICA (OAB) --------------------
    {"id": 126, "area": "Ética", "q": "O advogado pode fazer publicidade de seus serviços?", "options": ["Não, nunca", "Sim, com discrição e sobriedade, vedada a mercantilização", "Sim, em rádio e TV", "Sim, panfletagem é permitida"], "answer": 1, "explain": "A publicidade é permitida, mas deve ser informativa, discreta e sóbria."},
    {"id": 127, "area": "Ética", "q": "A incompatibilidade com a advocacia gera:", "options": ["Impedimento parcial", "Proibição total de exercer a advocacia", "Apenas multa", "Suspensão temporária"], "answer": 1, "explain": "Incompatibilidade (ex: Juiz, Policial) gera proibição total. Impedimento gera proibição parcial."},
    {"id": 128, "area": "Ética", "q": "O sigilo profissional do advogado é:", "options": ["Absoluto, salvo grave ameaça à vida ou honra, ou defesa própria", "Relativo sempre", "Dispensável se o cliente autorizar", "Inexistente"], "answer": 0, "explain": "É dever e direito, cedendo apenas em circunstâncias excepcionalíssimas."},
    {"id": 129, "area": "Ética", "q": "A sociedade de advogados adquire personalidade jurídica com:", "options": ["Registro na Receita Federal", "Registro no Cartório Civil", "Registro no Conselho Seccional da OAB", "Abertura de conta bancária"], "answer": 2, "explain": "O registro é exclusivo na OAB, não em cartório."},
    {"id": 130, "area": "Ética", "q": "Advogado substabelecido com reserva de poderes:", "options": ["Pode cobrar honorários diretamente do cliente", "Não pode cobrar honorários do cliente sem intervenção do substabelecente", "Vira dono do processo", "Não pode atuar"], "answer": 1, "explain": "O contrato principal segue com o advogado original; o substabelecido ajusta com ele."},
    {"id": 131, "area": "Ética", "q": "É direito da advogada gestante:", "options": ["Entrada em tribunais sem passar por raio-X", "Suspensão de prazos em qualquer caso", "Imunidade penal", "Isenção de anuidade"], "answer": 0, "explain": "Estatuto da OAB garante entrada sem raio-X e vaga preferencial."},
    {"id": 132, "area": "Ética", "q": "O advogado empregado, em regra, tem jornada de:", "options": ["8 horas diárias", "4 horas diárias ou 20 semanais", "6 horas diárias", "12 horas diárias"], "answer": 1, "explain": "Salvo dedicação exclusiva, a jornada é de 4 horas diárias."},
    {"id": 133, "area": "Ética", "q": "A pena de exclusão da OAB aplica-se a quem:", "options": ["Deixa de pagar anuidade", "Faz publicidade irregular", "Torna-se moralmente inidôneo para a advocacia", "Abandona a causa"], "answer": 2, "explain": "Inidoneidade moral, crime infamante e falsa prova de requisitos geram exclusão."},
    {"id": 134, "area": "Ética", "q": "Os honorários de sucumbência pertencem:", "options": ["Ao cliente", "Ao advogado", "Ao Estado", "Ao juiz"], "answer": 1, "explain": "O Estatuto define que os honorários de sucumbência são direito do advogado."},
    {"id": 135, "area": "Ética", "q": "O mandato judicial (procuração) extingue-se por:", "options": ["Mero decurso de tempo", "Revogação pelo cliente ou renúncia pelo advogado", "Fim do ano forense", "Vontade do juiz"], "answer": 1, "explain": "A revogação ou renúncia encerram o mandato, devendo ser notificadas."},
]

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def norm_area(s: str) -> str:
    """Normaliza texto de área para evitar mismatch por espaços invisíveis."""
    return (s or "").strip()

def get_questions_by_area(area: str):
    area = norm_area(area)
    return [q for q in QUESTIONS if norm_area(q.get("area")) == area]

def q_by_id(qid: int):
    for q in QUESTIONS:
        if q.get("id") == qid:
            return q
    return None

def build_quiz(area: str, mode: str, n: int):
    pool = get_questions_by_area(area)

    # protege: não pede mais do que existe
    n = min(n, len(pool))

    # seleciona SEM repetição
    selected = random.sample(pool, k=n) if n > 0 else []

    return {
        "area": area,
        "mode": mode,
        "n": n,
        "items": [q["id"] for q in selected],
        "pos": 0,
        "score": 0,
        "answers": [],
    }

# =========================================================
# ROTAS
# =========================================================
@app.get("/")
def index():
    counts = {a: 0 for a in AREAS}
    for q in QUESTIONS:
        a = norm_area(q.get("area"))
        if a in counts:
            counts[a] += 1

    return render_template(
        "index.html",
        app_name=APP_NAME,
        areas=AREAS,
        total_questions=len(QUESTIONS),
        counts=counts
    )

@app.post("/start")
def start():
    area = norm_area(request.form.get("area"))
    mode = (request.form.get("mode") or "treino").strip()
    n_raw = (request.form.get("n") or "10").strip()

    areas_norm = [norm_area(a) for a in AREAS]
    if area not in areas_norm:
        flash("Escolha uma área válida.")
        return redirect(url_for("index"))

    try:
        n = int(n_raw)
        n = max(5, min(20, n))
    except ValueError:
        n = 10

    quiz = build_quiz(area, mode, n)

    if not quiz["items"]:
        flash(f"Ainda não há perguntas cadastradas para {area}.")
        return redirect(url_for("index"))

    session["quiz"] = quiz
    session.pop("last_feedback", None)
    return redirect(url_for("question"))

@app.get("/q")
def question():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("index"))

    pos = quiz["pos"]
    if pos >= quiz["n"]:
        return redirect(url_for("result"))

    qid = quiz["items"][pos]
    q = q_by_id(qid)
    if not q:
        flash("Erro ao carregar pergunta.")
        return redirect(url_for("index"))

    time_limit = 20 if quiz["mode"] == "prova" else None

    return render_template(
        "quiz.html",
        app_name=APP_NAME,
        quiz=quiz,
        q=q,
        pos=pos,
        time_limit=time_limit
    )

@app.post("/answer")
def answer():
    quiz = session.get("quiz")
    if not quiz:
        flash("Sessão expirada. Inicie novo quiz.")
        return redirect(url_for("index"))

    pos = quiz["pos"]
    if pos >= quiz["n"]:
        return redirect(url_for("result"))

    qid = quiz["items"][pos]
    q = q_by_id(qid)
    if not q:
        flash("Pergunta inválida.")
        return redirect(url_for("index"))

    chosen_raw = request.form.get("choice", "")
    try:
        chosen = int(chosen_raw)
    except ValueError:
        chosen = -1

    correct = q["answer"]
    is_correct = (chosen == correct)

    if is_correct:
        quiz["score"] += 1

    quiz["answers"].append({
        "id": qid,
        "chosen": chosen,
        "correct": correct,
        "is_correct": is_correct
    })

    quiz["pos"] += 1
    session["quiz"] = quiz

    if quiz["mode"] == "treino":
        session["last_feedback"] = {
            "qid": qid,
            "is_correct": is_correct,
            "explain": q.get("explain", "")
        }
    else:
        session.pop("last_feedback", None)

    return redirect(url_for("question"))

@app.get("/result")
def result():
    quiz = session.get("quiz")
    if not quiz:
        return redirect(url_for("index"))

    details = []
    for a in quiz["answers"]:
        q = q_by_id(a["id"])
        if not q:
            continue

        q_data = {
            "area": q.get("area", ""),
            "q": q.get("q", ""),
            "options": q.get("options", []),
            "chosen": a.get("chosen", -1),
            "correct": a.get("correct", -1),
            "is_correct": a.get("is_correct", False),
            "explain": q.get("explain", ""),
        }
        if "difficulty" in q:
            q_data["difficulty"] = q["difficulty"]

        details.append(q_data)

    wrong_ids = [a["id"] for a in quiz["answers"] if not a.get("is_correct")]
    session["wrong_ids"] = wrong_ids

    per_area = {}
    for d in details:
        area = norm_area(d.get("area"))
        if area not in per_area:
            per_area[area] = {"total": 0, "correct": 0}
        per_area[area]["total"] += 1
        if d.get("is_correct"):
            per_area[area]["correct"] += 1

    session["last_per_area"] = per_area

    return render_template(
        "result.html",
        app_name=APP_NAME,
        quiz=quiz,
        details=details,
        per_area=per_area
    )

@app.get("/review")
def review():
    wrong_ids = session.get("wrong_ids", [])
    if not wrong_ids:
        flash("Você não tem erros para revisar ainda.")
        return redirect(url_for("index"))

    n_review = min(20, len(wrong_ids))

    quiz = {
        "area": "Revisão de Erros",
        "mode": "treino",
        "n": n_review,
        "items": wrong_ids[:n_review],
        "pos": 0,
        "score": 0,
        "answers": [],
    }

    session["quiz"] = quiz
    session.pop("last_feedback", None)
    return redirect(url_for("question"))

# =========================================================
# NOVO: PRÓXIMA QUESTÃO (MODO TREINO)
# =========================================================
@app.get("/next")
def next_question():
    # limpa o feedback e deixa /q renderizar a próxima pergunta
    session.pop("last_feedback", None)
    return redirect(url_for("question"))

@app.get("/reset")
def reset():
    session.pop("quiz", None)
    session.pop("last_feedback", None)
    session.pop("wrong_ids", None)
    session.pop("last_per_area", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
