import random

def _mk(qid, area, q, options, answer, explain, difficulty="basico", tags=None):
    return {
        "id": qid,
        "area": area,
        "q": q,
        "options": options,
        "answer": answer,
        "explain": explain,
        "difficulty": difficulty,
        "tags": tags or []
    }

def _shuffle_options(item):
    """Embaralha alternativas mantendo o gabarito correto."""
    opts = list(item["options"])
    correct_text = opts[item["answer"]]
    random.shuffle(opts)
    item["answer"] = opts.index(correct_text)
    item["options"] = opts
    return item

def generate_extra_questions(start_id: int, target_total: int):
    """
    Gera questões extras por templates até chegar em target_total.
    """
    qid = start_id
    out = []

    # ========= TEMPLATES (exemplos) =========
    # Você vai adicionar mais templates com o tempo.
    penal_templates = [
        ("Direito Penal",
         "A representação da vítima, nos crimes de ação pública condicionada, em regra, deve ocorrer em:",
         ["3 meses", "6 meses", "1 ano", "2 anos"], 1,
         "Regra geral: prazo decadencial de 6 meses a contar do conhecimento da autoria.",
         "basico", ["ação penal", "representação"]),

        ("Direito Penal",
         "O recebimento da denúncia ou queixa é marco que, em regra:",
         ["reduz a pena", "interrompe a prescrição", "extingue o processo", "anula o inquérito"], 1,
         "Em geral, o recebimento da inicial acusatória é marco interruptivo da prescrição (CP).",
         "basico", ["prescrição", "marcos"]),

        ("Direito Penal",
         "A decadência, quando aplicável, tem como efeito principal:",
         ["reduzir a pena", "extinguir a punibilidade", "aumentar a pena", "suspender o processo"], 1,
         "Decadência do direito de queixa/representação extingue a punibilidade.",
         "basico", ["extinção da punibilidade", "decadência"]),
    ]

    civil_obrigacoes_templates = [
        ("Direito Civil",
         "Em obrigações solidárias passivas, o credor pode exigir:",
         ["apenas parte da dívida", "apenas do devedor mais rico", "a totalidade de qualquer devedor", "somente após sentença"], 2,
         "Na solidariedade passiva, o credor pode cobrar integralmente de qualquer devedor.",
         "basico", ["obrigações", "solidariedade"]),

        ("Direito Civil",
         "A mora do devedor ocorre, em regra, quando:",
         ["o credor perdoa a dívida", "não paga no tempo, lugar e forma devidos", "há contrato verbal", "existe fiador"], 1,
         "Mora é atraso culposo no cumprimento: tempo, lugar e forma convencionados.",
         "basico", ["mora", "inadimplemento"]),
    ]

    proc_civil_templates = [
        ("Processo Civil",
         "O princípio da cooperação no CPC impõe que:",
         ["apenas o juiz coopere", "todos atuem para decisão justa e efetiva", "o réu sempre confesse", "não haja contraditório"], 1,
         "CPC/2015 reforça cooperação entre sujeitos do processo para decisão justa.",
         "basico", ["princípios", "cooperação"]),

        ("Processo Civil",
         "O Incidente de Desconsideração da Personalidade Jurídica (IDPJ) assegura:",
         ["prisão civil", "contraditório e ampla defesa", "execução automática", "revelia do sócio"], 1,
         "Arts. 133–137 do CPC: IDPJ garante contraditório e ampla defesa.",
         "basico", ["IDPJ", "art. 133-137"]),
    ]

    constitucional_templates = [
        ("Direito Constitucional",
         "Direitos fundamentais possuem, em regra, aplicabilidade:",
         ["somente após lei", "imediata", "somente em estados", "apenas programática"], 1,
         "Art. 5º, §1º: normas definidoras têm aplicação imediata.",
         "basico", ["direitos fundamentais"]),

        ("Direito Constitucional",
         "O controle difuso de constitucionalidade pode ser realizado por:",
         ["apenas STF", "qualquer juiz ou tribunal", "apenas Senado", "apenas Presidente"], 1,
         "No controle difuso, qualquer órgão do Judiciário pode reconhecer inconstitucionalidade no caso concreto.",
         "basico", ["controle de constitucionalidade"]),
    ]

    etica_templates = [
        ("Ética",
         "No exercício profissional, é eticamente adequado:",
         ["prometer resultado ao cliente", "guardar sigilo sobre informações sensíveis", "divulgar dados sem consentimento", "aceitar causa com conflito de interesse sem informar"], 1,
         "Sigilo e proteção de informações são pilares éticos em diversas profissões e na prática jurídica/atendimento.",
         "basico", ["sigilo", "conduta profissional"]),

        ("Ética",
         "Conflito de interesses ocorre quando:",
         ["há mais de um cliente", "há interesse pessoal que compromete imparcialidade", "o processo é complexo", "o juiz é competente"], 1,
         "Conflito de interesses surge quando interesses pessoais ou de terceiros podem comprometer a atuação profissional.",
         "basico", ["conflito de interesses"]),
    ]

    all_templates = (
        penal_templates
        + civil_obrigacoes_templates
        + proc_civil_templates
        + constitucional_templates
        + etica_templates
    )

    # ========= GERAÇÃO COM VARIAÇÕES =========
    # A lógica aqui multiplica com pequenas variações de texto/ordem.
    prefixes = ["(Nível Básico) ", "(Revisão) ", "(Fixação) ", ""]
    suffixes = ["", " (marque a correta)", " (assinale a alternativa correta)"]

    while (len(out) + start_id - 1) < target_total:
        base = random.choice(all_templates)
        area, q_text, options, answer, explain, difficulty, tags = base

        q2 = random.choice(prefixes) + q_text + random.choice(suffixes)

        item = _mk(qid, area, q2, list(options), answer, explain, difficulty=difficulty, tags=list(tags))
        item = _shuffle_options(item)

        out.append(item)
        qid += 1

        # Evita loop infinito se target_total for pequeno
        if qid > start_id + 100000:
            break

    return out
