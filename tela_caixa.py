import flet as ft

def mostrar_tela_caixa(page):
    def on_change_valor(e):
        # Filtra para permitir apenas números
        e.control.value = ''.join(filter(str.isdigit, e.control.value))
        e.control.update()

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
                on_click=lambda e: None,  # Adicione a função que você quiser aqui
                width=130,
                color="#62ff00",
                bgcolor=ft.colors.GREEN,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
            ft.ElevatedButton(
                text="Fechar caixa",
                on_click=lambda e: None,  # Adicione a função que você quiser aqui
                width=130,
                color=ft.colors.BLACK,
                bgcolor=ft.colors.RED_400,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
