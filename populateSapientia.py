from rdflib import Graph, Namespace, RDF, OWL, Literal, URIRef
import json


g = Graph()
g.parse("sapientia_base.ttl")
n = Namespace("http://rpcw/ontologies/2025/sapientia_base/")


#migração dos conceitos
with open("conceitos.json", "r",encoding="utf-8") as f:
    data = json.load(f)

conceitosList = []
periodoHistList = []
aplicacoesList = []
disciplinasList = []
tConhecimentoList = []
mestresList = []
obrasList = []
aprendizesList = []

for conceito in data["conceitos"]:

    nome = conceito["nome"] #str
    aplicacoes = conceito["aplicações"] #list
    periodoHist = conceito["períodoHistórico"] #str
    conceitosRel = conceito["conceitosRelacionados"] #list

    conceitoURI = URIRef(f"{n}{nome.replace(' ', '_')}")

    if nome not in conceitosList:
        g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
        g.add((conceitoURI, RDF.type, n.Conceito))
        g.add((conceitoURI, n.nome, Literal(nome)))
        conceitosList.append(nome)

    periodoURI = URIRef(f"{n}{periodoHist.replace(' ', '_')}")
    if periodoHist not in periodoHistList:
        g.add((periodoURI, RDF.type, OWL.NamedIndividual))
        g.add((periodoURI, RDF.type, n.PeriodoHistorico))
        g.add((periodoURI, n.periodo, Literal(periodoHist)))

        periodoHistList.append(periodoHist)
        
    g.add((conceitoURI,n.surgeEm,periodoURI))
    
    for conceitoRel in conceitosRel:
        conceitoRelURI = URIRef(f"{n}{conceitoRel.replace(' ', '_')}")
        if conceitoRel not in conceitosList:
            g.add((conceitoRelURI, RDF.type, OWL.NamedIndividual))
            g.add((conceitoRelURI, RDF.type, n.Conceito))
            g.add((conceitoRelURI, n.nome, Literal(conceitoRel)))
            conceitosList.append(conceitoRel)
        g.add((conceitoURI,n.estáRelacionadoCom,conceitoRelURI))
    
    for aplicacao in aplicacoes:
        aplicacaoURI = URIRef(f"{n}{aplicacao.replace(' ', '_')}")
        if aplicacao not in aplicacoesList:
            g.add((aplicacaoURI, RDF.type, OWL.NamedIndividual))
            g.add((aplicacaoURI, RDF.type, n.Aplicacao))
            g.add((aplicacaoURI, n.nome, Literal(aplicacao)))
            aplicacoesList.append(aplicacao)
        g.add((conceitoURI,n.temAplicaçãoEm,aplicacaoURI))

#migração das disciplinas
with open("disciplinas.json", "r",encoding="utf-8") as f:
    data = json.load(f)


for disciplina in data["disciplinas"]:

    nome = disciplina["nome"] #str
    tConhecimento = disciplina["tiposDeConhecimento"]
    if "conceitos" in disciplina.keys():
        conceitos = disciplina["conceitos"]
    else:
        conceitos = []
    disciplinaURI = URIRef(f"{n}{nome.replace(' ', '_')}")

    if nome not in disciplinasList:
        g.add((disciplinaURI, RDF.type, OWL.NamedIndividual))
        g.add((disciplinaURI, RDF.type, n.Disciplina))
        g.add((disciplinaURI, n.nome, Literal(nome)))
        disciplinasList.append(nome)
    
    for t in tConhecimento:
        tURI = URIRef(f"{n}{t.replace(' ', '_')}")
        if t not in tConhecimentoList:
            g.add((tURI, RDF.type, OWL.NamedIndividual))
            g.add((tURI, RDF.type, n.TipoDeConhecimento))
            g.add((tURI, n.nome, Literal(t)))
            tConhecimentoList.append(t)
        g.add((disciplinaURI,n.pertenceA,tURI))

    for con in conceitos:
        conURI = URIRef(f"{n}{con.replace(' ', '_')}")
        if con not in conceitosList:
            g.add((conURI, RDF.type, OWL.NamedIndividual))
            g.add((conURI, RDF.type, n.Conceito))
            g.add((conURI, n.nome, Literal(con)))
            conceitosList.append(con)
        g.add((conURI,n.éEstudadoEm,disciplinaURI))

#migração dos mestres
with open("mestres.json", "r",encoding="utf-8") as f:
    data = json.load(f)


for mestre in data["mestres"]:

    nome = mestre["nome"] #str
    periodoHist = mestre["períodoHistórico"]
    disciplinas = mestre["disciplinas"]

    mestreURI = URIRef(f"{n}{nome.replace(' ', '_')}")

    if nome not in mestresList:
        g.add((mestreURI, RDF.type, OWL.NamedIndividual))
        g.add((mestreURI, RDF.type, n.Mestre))
        g.add((mestreURI, n.nome, Literal(nome)))
        mestresList.append(nome)
    
    periodoURI = URIRef(f"{n}{periodoHist.replace(' ', '_')}")
    if periodoHist not in periodoHistList:
        g.add((periodoURI, RDF.type, OWL.NamedIndividual))
        g.add((periodoURI, RDF.type, n.PeriodoHistorico))
        g.add((periodoURI, n.periodo, Literal(periodoHist)))
        periodoHistList.append(periodoHist)
    g.add((mestreURI,n.surgeEm,periodoURI))

    for dis in disciplinas:
        disURI = URIRef(f"{n}{dis.replace(' ', '_')}")
        if dis not in disciplinasList:
            g.add((disURI, RDF.type, OWL.NamedIndividual))
            g.add((disURI, RDF.type, n.Disciplina))
            g.add((disURI, n.nome, Literal(dis)))
            disciplinasList.append(dis)
        g.add((mestreURI,n.ensina,disURI))
    
#migração das obras
with open("obras.json", "r",encoding="utf-8") as f:
    data = json.load(f)


for obra in data["obras"]:

    nome = obra["titulo"] #str
    autor = obra["autor"]
    conceitos = obra["conceitos"]
    obraURI = URIRef(f"{n}{nome.replace(' ', '_')}")

    if nome not in obrasList:
        g.add((obraURI, RDF.type, OWL.NamedIndividual))
        g.add((obraURI, RDF.type, n.Obra))
        g.add((obraURI, n.titulo, Literal(nome)))
        obrasList.append(nome)
    
    autorURI = URIRef(f"{n}{autor.replace(' ', '_')}")
    if autor not in mestresList:
        g.add((autorURI, RDF.type, OWL.NamedIndividual))
        g.add((autorURI, RDF.type, n.Mestre))
        g.add((autorURI, n.nome, Literal(autor)))
        mestresList.append(autor)
    g.add((obraURI,n.foiEscritoPor,autorURI))

    for con in conceitos:
        conURI = URIRef(f"{n}{con.replace(' ', '_')}")
        if con not in conceitosList:
            g.add((conURI, RDF.type, OWL.NamedIndividual))
            g.add((conURI, RDF.type, n.Conceito))
            g.add((conURI, n.nome, Literal(con)))
            conceitosList.append(con)
        g.add((obraURI,n.explica,conURI))


#migração dos aprendizes
with open("pg56006.json", "r",encoding="utf-8") as f:
    data = json.load(f)

for aprendiz in data:

    nome = aprendiz["nome"] #str
    idade = aprendiz["idade"]
    disciplinas = aprendiz["disciplinas"]
    aprendizURI = URIRef(f"{n}{nome.replace(' ', '_')}")

    if nome not in aprendizesList:
        g.add((aprendizURI, RDF.type, OWL.NamedIndividual))
        g.add((aprendizURI, RDF.type, n.Aprendiz))
        g.add((aprendizURI, n.nome, Literal(nome)))
    g.add((aprendizURI, n.idade, Literal(idade)))

    for dis in disciplinas:
        disURI = URIRef(f"{n}{dis.replace(' ', '_')}")
        if dis not in disciplinasList:
            g.add((disURI, RDF.type, OWL.NamedIndividual))
            g.add((disURI, RDF.type, n.Disciplina))
            g.add((disURI, n.nome, Literal(dis)))
            disciplinasList.append(dis)
        g.add((aprendizURI,n.aprende,disURI))

print(g.serialize("sapientia_ind.ttl", format="turtle"))
