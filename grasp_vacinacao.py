"""
GRASP - Distribuição de Recursos para Vacinação em Massa
=========================================================
Problema: Alocar postos de vacinação e demanda para minimizar custo total.

Custos considerados:
  - Abertura de posto
  - Distância (deslocamento da população)
  - Não atendimento (demanda não coberta)

Entrada: arquivo JSON (ver exemplo em instancia_exemplo.json)
"""

import json
import random
import math
import sys
import copy
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────
# Estruturas de dados
# ─────────────────────────────────────────────

@dataclass
class Posto:
    id: int
    nome: str
    capacidade: int       # máximo de pessoas que pode atender
    custo_abertura: float # custo fixo para abrir o posto
    x: float              # coordenada x (para calcular distância)
    y: float              # coordenada y


@dataclass
class PontoDemanda:
    id: int
    nome: str
    populacao: int        # pessoas que precisam ser vacinadas
    x: float
    y: float


@dataclass
class Solucao:
    postos_abertos: list[int]                    # IDs dos postos abertos
    alocacao: dict[int, int]                     # demanda_id -> posto_id
    nao_atendidos: dict[int, int]                # demanda_id -> qtd não atendida
    custo_total: float = 0.0
    custo_abertura: float = 0.0
    custo_distancia: float = 0.0
    custo_nao_atendimento: float = 0.0

    def copia(self):
        return copy.deepcopy(self)


# ─────────────────────────────────────────────
# Leitura da instância
# ─────────────────────────────────────────────

def carregar_instancia(caminho: str) -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    postos = [Posto(**p) for p in dados["postos"]]
    demandas = [PontoDemanda(**d) for d in dados["demandas"]]
    params = dados["parametros"]

    return {
        "postos": postos,
        "demandas": demandas,
        "custo_por_km": params["custo_por_km"],
        "custo_nao_atendimento": params["custo_nao_atendimento"],
    }


# ─────────────────────────────────────────────
# Funções auxiliares
# ─────────────────────────────────────────────

def distancia(a_x, a_y, b_x, b_y) -> float:
    return math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)


def calcular_custo(solucao: Solucao, postos: list[Posto],
                   demandas: list[PontoDemanda],
                   custo_por_km: float,
                   custo_nao_atend: float) -> Solucao:
    """Recalcula todos os custos de uma solução."""

    postos_dict = {p.id: p for p in postos}
    demandas_dict = {d.id: d for d in demandas}

    solucao.custo_abertura = sum(
        postos_dict[pid].custo_abertura for pid in solucao.postos_abertos
    )

    solucao.custo_distancia = 0.0
    for dem_id, posto_id in solucao.alocacao.items():
        dem = demandas_dict[dem_id]
        posto = postos_dict[posto_id]
        dist = distancia(dem.x, dem.y, posto.x, posto.y)
        solucao.custo_distancia += dist * custo_por_km * dem.populacao

    solucao.custo_nao_atendimento = sum(
        qtd * custo_nao_atend for qtd in solucao.nao_atendidos.values()
    )

    solucao.custo_total = (
        solucao.custo_abertura
        + solucao.custo_distancia
        + solucao.custo_nao_atendimento
    )
    return solucao


def alocar_demanda(postos_abertos_ids: list[int],
                   postos: list[Posto],
                   demandas: list[PontoDemanda],
                   custo_por_km: float,
                   custo_nao_atend: float) -> Solucao:
    """
    Para um conjunto de postos abertos, aloca cada ponto de demanda
    ao posto mais próximo com capacidade disponível.
    """
    postos_abertos = [p for p in postos if p.id in postos_abertos_ids]
    capacidade_restante = {p.id: p.capacidade for p in postos_abertos}

    alocacao = {}
    nao_atendidos = {}

    for dem in demandas:
        # Ordena postos abertos por distância à demanda
        candidatos = sorted(
            postos_abertos,
            key=lambda p: distancia(dem.x, dem.y, p.x, p.y)
        )

        populacao_restante = dem.populacao
        for posto in candidatos:
            if populacao_restante <= 0:
                break
            if capacidade_restante[posto.id] > 0:
                atendido = min(populacao_restante, capacidade_restante[posto.id])
                populacao_restante -= atendido
                capacidade_restante[posto.id] -= atendido
                # Registra o posto principal (primeiro que atendeu)
                if dem.id not in alocacao:
                    alocacao[dem.id] = posto.id

        if populacao_restante > 0:
            nao_atendidos[dem.id] = populacao_restante
            if dem.id not in alocacao and postos_abertos:
                # Aloca ao mais próximo mesmo sem capacidade (para ter referência)
                alocacao[dem.id] = candidatos[0].id

    solucao = Solucao(
        postos_abertos=list(postos_abertos_ids),
        alocacao=alocacao,
        nao_atendidos=nao_atendidos,
    )
    return calcular_custo(solucao, postos, demandas, custo_por_km, custo_nao_atend)


# ─────────────────────────────────────────────
# GRASP – Fase de Construção
# ─────────────────────────────────────────────

def construcao_grasp(postos: list[Posto],
                     demandas: list[PontoDemanda],
                     alpha: float,
                     custo_por_km: float,
                     custo_nao_atend: float) -> Solucao:
    """
    Constrói uma solução gulosa-aleatória (semi-gulosa).

    Critério guloso: custo marginal de adicionar um posto à solução atual.
    LRC: postos com custo entre [melhor, melhor + α*(pior - melhor)]
    """
    postos_disponiveis = list(postos)
    postos_escolhidos = []

    # Garante ao menos um posto na solução inicial
    while postos_disponiveis:
        # Avalia custo marginal de cada posto candidato
        custos_marginais = []
        for posto in postos_disponiveis:
            sol_teste = alocar_demanda(
                postos_escolhidos + [posto.id],
                postos, demandas, custo_por_km, custo_nao_atend
            )
            custos_marginais.append((posto, sol_teste.custo_total))

        custos_marginais.sort(key=lambda x: x[1])

        c_melhor = custos_marginais[0][1]   # e1: melhor candidato
        c_pior = custos_marginais[-1][1]    # e2: pior candidato

        # Limiar da LRC (versão minimização)
        limiar = c_melhor + alpha * (c_pior - c_melhor)

        # LRC: candidatos com custo <= limiar
        lrc = [posto for posto, custo in custos_marginais if custo <= limiar]

        # Escolhe aleatoriamente da LRC
        escolhido = random.choice(lrc)
        postos_escolhidos.append(escolhido.id)
        postos_disponiveis.remove(escolhido)

        # Critério de parada: solução viável (toda demanda atendida ou
        # adicionar mais postos não melhora)
        sol_atual = alocar_demanda(
            postos_escolhidos, postos, demandas, custo_por_km, custo_nao_atend
        )

        # Verifica se toda demanda foi atendida
        if not sol_atual.nao_atendidos:
            return sol_atual

        # Verifica se vale abrir mais postos: compara custo com e sem o próximo
        # (simplificação: para quando o custo marginal esperado é negativo)
        if len(postos_disponiveis) > 0:
            melhor_prox = min(
                alocar_demanda(postos_escolhidos + [p.id], postos, demandas,
                               custo_por_km, custo_nao_atend).custo_total
                for p in postos_disponiveis
            )
            if melhor_prox >= sol_atual.custo_total:
                return sol_atual  # adicionar mais postos só piora

    return alocar_demanda(postos_escolhidos, postos, demandas,
                          custo_por_km, custo_nao_atend)


# ─────────────────────────────────────────────
# GRASP – Busca Local
# ─────────────────────────────────────────────

def busca_local(solucao: Solucao,
                postos: list[Posto],
                demandas: list[PontoDemanda],
                custo_por_km: float,
                custo_nao_atend: float) -> Solucao:
    """
    Busca local por troca: tenta substituir cada posto aberto por um fechado,
    ou fechar um posto sem substituto. Aceita qualquer melhora (first-improvement).
    """
    todos_ids = {p.id for p in postos}
    melhor = solucao.copia()
    melhorou = True

    while melhorou:
        melhorou = False
        abertos = set(melhor.postos_abertos)
        fechados = todos_ids - abertos

        # Movimento 1: fechar um posto aberto
        for pid in list(abertos):
            if len(abertos) <= 1:
                break
            novos_abertos = [p for p in melhor.postos_abertos if p != pid]
            nova_sol = alocar_demanda(novos_abertos, postos, demandas,
                                      custo_por_km, custo_nao_atend)
            if nova_sol.custo_total < melhor.custo_total:
                melhor = nova_sol
                melhorou = True
                break

        # Movimento 2: trocar um posto aberto por um fechado
        for pid_aberto in list(melhor.postos_abertos):
            for pid_fechado in fechados:
                novos_abertos = [p for p in melhor.postos_abertos
                                 if p != pid_aberto] + [pid_fechado]
                nova_sol = alocar_demanda(novos_abertos, postos, demandas,
                                          custo_por_km, custo_nao_atend)
                if nova_sol.custo_total < melhor.custo_total:
                    melhor = nova_sol
                    melhorou = True
                    break
            if melhorou:
                break

        # Movimento 3: abrir um posto fechado
        for pid_fechado in fechados:
            novos_abertos = melhor.postos_abertos + [pid_fechado]
            nova_sol = alocar_demanda(novos_abertos, postos, demandas,
                                      custo_por_km, custo_nao_atend)
            if nova_sol.custo_total < melhor.custo_total:
                melhor = nova_sol
                melhorou = True
                break

    return melhor


# ─────────────────────────────────────────────
# GRASP – Loop Principal
# ─────────────────────────────────────────────

def grasp(postos: list[Posto],
          demandas: list[PontoDemanda],
          custo_por_km: float,
          custo_nao_atend: float,
          alpha: float = 0.3,
          max_iteracoes: int = 50,
          semente: Optional[int] = None) -> tuple[Solucao, list[float]]:
    """
    GRASP completo.

    Parâmetros:
        alpha           : grau de aleatoriedade (0 = guloso puro, 1 = aleatório puro)
        max_iteracoes   : número de iterações do GRASP
        semente         : semente para reprodutibilidade (None = aleatório)

    Retorna:
        melhor_solucao  : melhor solução encontrada
        historico       : custo da melhor solução a cada iteração
    """
    if semente is not None:
        random.seed(semente)

    melhor_global: Optional[Solucao] = None
    historico = []

    print(f"\n{'='*55}")
    print(f"  GRASP – Vacinação em Massa")
    print(f"  α={alpha}  |  iterações={max_iteracoes}")
    print(f"{'='*55}")

    for it in range(1, max_iteracoes + 1):
        # 1. Construção
        sol_construida = construcao_grasp(
            postos, demandas, alpha, custo_por_km, custo_nao_atend
        )

        # 2. Busca Local
        sol_melhorada = busca_local(
            sol_construida, postos, demandas, custo_por_km, custo_nao_atend
        )

        # 3. Atualiza melhor global
        if melhor_global is None or sol_melhorada.custo_total < melhor_global.custo_total:
            melhor_global = sol_melhorada.copia()
            flag = " ◀ novo melhor"
        else:
            flag = ""

        historico.append(melhor_global.custo_total)
        print(f"  iter {it:3d} | construção: {sol_construida.custo_total:10.2f}"
              f" | após BL: {sol_melhorada.custo_total:10.2f}"
              f" | melhor: {melhor_global.custo_total:10.2f}{flag}")

    return melhor_global, historico


# ─────────────────────────────────────────────
# Relatório final
# ─────────────────────────────────────────────

def imprimir_resultado(solucao: Solucao,
                       postos: list[Posto],
                       demandas: list[PontoDemanda]):
    postos_dict = {p.id: p for p in postos}
    demandas_dict = {d.id: d for d in demandas}

    print(f"\n{'='*55}")
    print("  MELHOR SOLUÇÃO ENCONTRADA")
    print(f"{'='*55}")
    print(f"  Custo total          : {solucao.custo_total:,.2f}")
    print(f"  └ Abertura           : {solucao.custo_abertura:,.2f}")
    print(f"  └ Distância          : {solucao.custo_distancia:,.2f}")
    print(f"  └ Não atendimento    : {solucao.custo_nao_atendimento:,.2f}")
    print(f"\n  Postos abertos ({len(solucao.postos_abertos)}):")
    for pid in sorted(solucao.postos_abertos):
        p = postos_dict[pid]
        print(f"    • [{pid}] {p.nome}  (cap={p.capacidade}, abertura={p.custo_abertura})")

    print(f"\n  Alocação de demanda:")
    for did, pid in sorted(solucao.alocacao.items()):
        dem = demandas_dict[did]
        posto = postos_dict[pid]
        nao_at = solucao.nao_atendidos.get(did, 0)
        status = f"  ⚠ {nao_at} não atendidos" if nao_at else ""
        print(f"    • {dem.nome} (pop={dem.populacao}) → {posto.nome}{status}")

    total_nao_at = sum(solucao.nao_atendidos.values())
    total_pop = sum(d.populacao for d in demandas)
    cobertura = 100 * (1 - total_nao_at / total_pop) if total_pop > 0 else 100
    print(f"\n  Cobertura            : {cobertura:.1f}%")
    print(f"  Não atendidos        : {total_nao_at} / {total_pop}")
    print(f"{'='*55}\n")


# ─────────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python grasp_vacinacao.py <instancia.json> [alpha] [iteracoes] [semente]")
        print("Exemplo: python grasp_vacinacao.py instancia_exemplo.json 0.3 50 42")
        sys.exit(1)

    caminho = sys.argv[1]
    alpha = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
    max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    semente = int(sys.argv[4]) if len(sys.argv) > 4 else None

    dados = carregar_instancia(caminho)

    melhor, historico = grasp(
        postos=dados["postos"],
        demandas=dados["demandas"],
        custo_por_km=dados["custo_por_km"],
        custo_nao_atend=dados["custo_nao_atendimento"],
        alpha=alpha,
        max_iteracoes=max_iter,
        semente=semente,
    )

    imprimir_resultado(melhor, dados["postos"], dados["demandas"])


if __name__ == "__main__":
    main()
