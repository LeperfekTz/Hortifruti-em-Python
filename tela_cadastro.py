import flet as ft

def mostrar_tela_cadastro(page):
    def on_change_preco(e):
        try:
            # Tenta converter o valor para float
            float(e.control.value)
            e.control.error_text = None  # Remove a mensagem de erro se for um valor válido
        except ValueError:
            e.control.error_text = "Insira um valor numérico válido."
        e.control.update()

    def on_change_valor(e):
        # Filtra para permitir apenas números
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
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
                bgcolor=ft.colors.GREEN,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
