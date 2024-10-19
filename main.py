import flet as ft
from tela_caixa import mostrar_tela_caixa
from tela_cadastro import mostrar_tela_cadastro
from tela_vendas import mostrar_tela_vendas
from tela_relatorios import mostrar_tela_relatorios
from navigation import criar_navigation_rail
from flet import *

def main(page: ft.Page):
    page.title = "ERP Hortifruti"
    page.bgcolor = "#f2f2f2"  # Cor de fundo do app

    # Função para alternar entre telas com base na seleção da NavigationRail
    def trocar_tela(e):
        if rail.selected_index == 0:
            corpo.content = mostrar_tela_cadastro(page)
        elif rail.selected_index == 1:
            corpo.content = mostrar_tela_vendas(page)
        elif rail.selected_index == 2:
            corpo.content = mostrar_tela_relatorios(page)
        elif rail.selected_index == 3:
            corpo.content = mostrar_tela_caixa(page)
        elif rail.selected_index == 4:  # Index do botão de sair
            page.window.destroy()  # Fecha a aplicação
        page.update()

    # NavigationRail
    rail = criar_navigation_rail(trocar_tela)

    # Conteúdo inicial do corpo da página
    corpo = ft.Container(content=mostrar_tela_cadastro(page), expand=True)

    # Layout da página
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                corpo,
            ],
            expand=True,
        )
    )

# Inicia a aplicação Flet
ft.app(main)
