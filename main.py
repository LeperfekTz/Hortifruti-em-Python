import flet as ft

def main(page: ft.Page):
    page.title = "ERP Hortifruti"
    page.bgcolor = "#f2f2f2"  # Cor de fundo do app

    def on_change_valor(e):
        # Filtra para permitir apenas números
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
        e.control.update()

    # Funções para exibir diferentes telas
    def mostrar_tela_caixa():
        return ft.Column(
            [                   
                ft.Text(value="Caixa", size=50, color="black"),
                ft.TextField(
                    label="Valor de abertura",
                    width=305,
                    keyboard_type=ft.KeyboardType.NUMBER,
                    on_change=on_change_valor
                ),  # Campo para valor de abertura
                ft.ElevatedButton(
                    text="Abrir caixa",
                    on_click=lambda e: trocar_tela(e),
                    color="#62ff00",
                    bgcolor="#000",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                ),
                ft.ElevatedButton(
                    text="Fechar caixa",
                    on_click=lambda e: trocar_tela(e),
                    color="#ff0000",
                    bgcolor="#000",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
    
    def mostrar_tela_cadastro():
        def on_change_preco(e):
            try:
                # Tenta converter o valor para float
                float(e.control.value)
                e.control.error_text = None  # Remove a mensagem de erro se for um valor válido
            except ValueError:
                e.control.error_text = "Insira um valor numérico válido."
            e.control.update()

        return ft.Column(
            [
                ft.Text("Cadastro de Produtos", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.TextField(label="Nome do Produto", width=300),
                ft.TextField(label="Preço", width=300, keyboard_type=ft.KeyboardType.NUMBER, color="black", on_change=on_change_preco, hint_text="Digite o valor"),
                ft.Row(
                    [
                        ft.Dropdown(
                            label="Categoria",
                            width=270,
                            bgcolor="#f2f2f2",
                            border_color="#000001",
                            border_width=1,
                            color="black",
                            options=[
                                ft.dropdown.Option("Frutas"),
                                ft.dropdown.Option("Verduras"),
                                ft.dropdown.Option("Legumes"),
                                ft.dropdown.Option("Grãos"),
                                ft.dropdown.Option("Laticínios"),
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.TextField(label="Quantidade em Estoque", width=300, keyboard_type=ft.KeyboardType.NUMBER, color="black", on_change=on_change_valor, hint_text="Digite a quantidade"),
                ft.ElevatedButton(
                    "Adicionar Produto",
                    color="#62ff00",
                    bgcolor="#000",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_vendas():
        return ft.Column(
            [
                ft.Text("Tela de Vendas", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Aqui você poderá registrar as vendas e visualizar o histórico.", color="black"),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_relatorios():
        return ft.Column(
            [
                ft.Text("Relatórios", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text("Aqui você poderá visualizar relatórios de vendas e estoque.", color="black"),
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
        bgcolor=ft.colors.GREEN,
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
                icon=ft.icons.POINT_OF_SALE,
                selected_icon_content=ft.Icon(ft.icons.POINT_OF_SALE),
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

# Inicia a aplicação Flet
ft.app(main)
