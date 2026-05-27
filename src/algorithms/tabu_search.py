"""
Busca Tabu (Tabu Search).
Responsabilidade única: otimizar solução através de restrições em histórico de movimentos.
"""

from typing import List, Tuple, Dict
from src.domain import Solucao, Posto, PontoDemanda, ParametrosInstancia
from src.algorithms.construcao import ConstrutorGrasp
from src.services.alocacao import AlocadorDemanda

class BuscaTabu:
    """
    Implementa Busca Tabu para encontrar o melhor conjunto de postos.
    Usa movimentos: Drop (fechar), Add (abrir), e Swap (trocar).
    """

    def __init__(self, construtor: ConstrutorGrasp, alocador: AlocadorDemanda):
        self.construtor = construtor
        self.alocador = alocador

    def executar(
        self,
        postos: List[Posto],
        demandas: List[PontoDemanda],
        params: ParametrosInstancia,
        max_iteracoes: int = 50,
        tabu_tenure: int = 5,
        verbose: bool = True
    ) -> Tuple[Solucao, List[float]]:
        """
        Executa Busca Tabu completa.
        
        Args:
            postos: Lista de postos
            demandas: Lista de pontos de demanda
            params: Parâmetros da instância
            max_iteracoes: Quantidade de vizinhanças que serão investigadas
            tabu_tenure: Tempo (iterações) que um movimento reverso fica proibido
            
        Returns:
            Tupla (melhor_solucao, historico_custos)
        """
        # 1. Gera solução inicial (Gulosa, alpha = 0.0)
        solucao_atual = self.construtor.construir(
            postos, demandas, 0.0,
            params.custo_por_km,
            params.custo_nao_atendimento
        )
        
        melhor_global = solucao_atual.copia()
        historico = [melhor_global.custo_total]

        # Dicionário guardando a iter de expiração do movimento reverso
        tabu_list = {}
        todos_ids = {p.id for p in postos}

        if verbose:
            print(f"\n{'='*55}")
            print(f"  BUSCA TABU – Vacinação em Massa")
            print(f"  iterações={max_iteracoes}  |  tabu_tenure={tabu_tenure}")
            print(f"{'='*55}")
            print(f"  Solução inicial gulosa: {solucao_atual.custo_total:10.2f}")

        for it in range(1, max_iteracoes + 1):
            abertos = set(solucao_atual.postos_abertos)
            fechados = todos_ids - abertos

            melhor_vizinho = None
            melhor_custo_vizinho = float('inf')
            melhor_movimento = None

            # ----------------------------------------------------
            # EXPLORAR VIZINHANÇA
            # ----------------------------------------------------

            # Movimento A: Fechar um posto (Drop)
            if len(abertos) > 1:
                for pid in abertos:
                    # Se fechou X, o reverso é Adicionar X = ('add', pid)
                    is_tabu = tabu_list.get(('drop', pid), 0) >= it
                    
                    novos_abertos = [p for p in solucao_atual.postos_abertos if p != pid]
                    nova_sol = self.alocador.alocar(
                        novos_abertos, postos, demandas,
                        params.custo_por_km, params.custo_nao_atendimento
                    )
                    
                    # Critério de Aspiração: se é melhor global, esquece ser tabu
                    if is_tabu and nova_sol.custo_total >= melhor_global.custo_total:
                        continue
                        
                    if nova_sol.custo_total < melhor_custo_vizinho:
                        melhor_vizinho = nova_sol
                        melhor_custo_vizinho = nova_sol.custo_total
                        melhor_movimento = ('drop', pid)

            # Movimento B: Abrir um posto (Add)
            for pid in fechados:
                is_tabu = tabu_list.get(('add', pid), 0) >= it
                
                novos_abertos = solucao_atual.postos_abertos + [pid]
                nova_sol = self.alocador.alocar(
                    novos_abertos, postos, demandas,
                    params.custo_por_km, params.custo_nao_atendimento
                )
                
                if is_tabu and nova_sol.custo_total >= melhor_global.custo_total:
                    continue
                    
                if nova_sol.custo_total < melhor_custo_vizinho:
                    melhor_vizinho = nova_sol
                    melhor_custo_vizinho = nova_sol.custo_total
                    melhor_movimento = ('add', pid)

            # Movimento C: Trocar (Swap) - Fecha um e abre outro
            for pid_sai in abertos:
                for pid_entra in fechados:
                    is_tabu = (tabu_list.get(('drop', pid_sai), 0) >= it) or \
                              (tabu_list.get(('add', pid_entra), 0) >= it)
                    
                    novos_abertos = [p for p in solucao_atual.postos_abertos if p != pid_sai] + [pid_entra]
                    nova_sol = self.alocador.alocar(
                        novos_abertos, postos, demandas,
                        params.custo_por_km, params.custo_nao_atendimento
                    )
                    
                    if is_tabu and nova_sol.custo_total >= melhor_global.custo_total:
                        continue
                        
                    if nova_sol.custo_total < melhor_custo_vizinho:
                        melhor_vizinho = nova_sol
                        melhor_custo_vizinho = nova_sol.custo_total
                        melhor_movimento = ('swap', pid_sai, pid_entra)

            if melhor_vizinho is None:
                if verbose:
                    print("Nenhum vizinho disponível, convergência atingida.")
                break

            # ----------------------------------------------------
            # ATUALIZAR STATUS
            # ----------------------------------------------------
            solucao_atual = melhor_vizinho
            
            # Bloqueia os movimentos reversos na Lista Tabu
            if melhor_movimento[0] == 'drop':
                pid = melhor_movimento[1]
                tabu_list[('add', pid)] = it + tabu_tenure
            elif melhor_movimento[0] == 'add':
                pid = melhor_movimento[1]
                tabu_list[('drop', pid)] = it + tabu_tenure
            elif melhor_movimento[0] == 'swap':
                _, pid_sai, pid_entra = melhor_movimento
                tabu_list[('add', pid_sai)] = it + tabu_tenure
                tabu_list[('drop', pid_entra)] = it + tabu_tenure

            flag = ""
            if solucao_atual.custo_total < melhor_global.custo_total:
                melhor_global = solucao_atual.copia()
                flag = " ◀ novo melhor global"

            historico.append(melhor_global.custo_total)

            if verbose:
                msg_mov = melhor_movimento[0]
                if msg_mov == 'drop':
                    msg_mov = f"drop {melhor_movimento[1]}"
                elif msg_mov == 'add':
                    msg_mov = f"add {melhor_movimento[1]}"
                else:
                    msg_mov = f"swap {melhor_movimento[1]}->{melhor_movimento[2]}"
                    
                print(f"  iter {it:3d} | vz_custo: {solucao_atual.custo_total:10.2f} "
                      f"| mov: {msg_mov:12} | global: {melhor_global.custo_total:10.2f}{flag}")

        if verbose:
            print(f"{'='*55}\n")

        return melhor_global, historico
