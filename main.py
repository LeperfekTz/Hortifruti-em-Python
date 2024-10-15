# flet run main.py

import flet as ft

def main(page: ft.Page):
    page.title = "ERP Hortifruti"
    
    # Funções para exibir diferentes telas
    def mostrar_tela_caixa():
        return ft.Column(
            [
                ft.Text(value="Caixa", size=50),
                ft.ElevatedButton(text="Voltar", on_click=lambda e: trocar_tela(e)),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_cadastro():
        return ft.Column(
            [
                ft.Text("Cadastro de Produtos", size=30, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Nome do Produto",width=300),
                ft.TextField(label="Preço", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Categoria"),
                ft.TextField(label="Quantidade em Estoque", keyboard_type=ft.KeyboardType.NUMBER),
                ft.ElevatedButton("Adicionar Produto"),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_vendas():
        return ft.Column(
            [
                ft.Text("Tela de Vendas", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Aqui você poderá registrar as vendas e visualizar o histórico."),
                # Adicione mais componentes relacionados às vendas
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_relatorios():
        return ft.Column(
            [
                ft.Text("Relatórios", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Aqui você poderá visualizar relatórios de vendas e estoque."),
                # Adicione componentes para exibir gráficos e relatórios
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    # Função para alternar entre telas com base na seleção da NavigationRail
    def trocar_tela(e):
        if rail.selected_index == 0:
            corpo.content = mostrar_tela_cadastro()
        elif rail.selected_index == 1:
            corpo.content = mostrar_tela_vendas()
        elif rail.selected_index == 2:
            corpo.content = mostrar_tela_relatorios()
        elif rail.selected_index == 3:
            corpo.content = mostrar_tela_caixa()
        elif rail.selected_index == 4:  # Index do botão de sair
            page.window_destroy()  # Fecha a aplicação
        page.update()

    # NavigationRail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        leading=ft.FloatingActionButton(icon=ft.icons.EXIT_TO_APP, text="Sair", on_click=lambda e: page.window_destroy()),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.ADD,
                selected_icon=ft.icons.ADD,
                label="Cadastro"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PAYMENT),
                selected_icon_content=ft.Icon(ft.icons.PAYMENT),
                label="Vendas",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.RECEIPT_LONG,
                selected_icon_content=ft.Icon(ft.icons.RECEIPT_LONG),
                label_content=ft.Text("Relatórios"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.APP_REGISTRATION,  # Substitua por um ícone adequado para "Caixa"
                selected_icon_content=ft.Icon(ft.icons.APP_REGISTRATION),
                label_content=ft.Text("Caixa"),
            ),
        ],
        on_change=trocar_tela,
    )

    # Conteúdo inicial do corpo da página
    corpo = ft.Container(content=mostrar_tela_cadastro(), expand=True)

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

ft.app(main)
