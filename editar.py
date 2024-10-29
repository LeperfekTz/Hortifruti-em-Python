import sqlite3
import flet as ft

# Função para carregar produtos do banco de dados
def load_products():
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    products = cursor.fetchall()
    conn.close()
    return products

# Função para atualizar um produto no banco de dados
def update_product(product_id, name, price, category, quantity):
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos
        SET nome = ?, preco = ?, categoria = ?, quantidade = ?
        WHERE id = ?
    """, (name, price, category, quantity, product_id))
    conn.commit()
    conn.close()

# Função para excluir um produto no banco de dados
def delete_product(product_id):
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Função que inicializa a interface
def main(page: ft.Page):
    page.title = "Editar Produtos"
    page.scroll = ft.ScrollMode.AUTO  # Permite rolagem na página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 800
    page.window.height = 500
    page.window_maximizable = False
    page.bgcolor = "#f2f2f2"

    # Carregar produtos da DB
    products = load_products()

    # Função para salvar mudanças
    def save_changes(e):
        for row in product_rows:
            product_id = row['id']
            name = row['name'].value
            price = float(row['price'].value)
            category = row['category'].value
            quantity = int(row['quantity'].value)
            update_product(product_id, name, price, category, quantity)

        # Exibir notificação de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"))
        page.snack_bar.open = True
        page.update()

    # Função para excluir um produto
    def delete_product_row(e, product_id):
        delete_product(product_id)
        for row in product_rows:
            if row['id'] == product_id:
                product_list.controls.remove(row['row'])  # Remover da lista de produtos
                product_rows.remove(row)  # Remover do controle
                break
        page.update()  # Atualizar a interface

    # Cabeçalhos da tabela com cor de fundo e alinhamento centralizado
    table_header = ft.Row(
        [
            ft.Text("ID", width=30, color="black", text_align="START"),
            ft.Text("Nome", width=140, color="black", text_align="center"),
            ft.Text("Preço", width=100, color="black", text_align="center"),
            ft.Text("Categoria", width=200, color="black", text_align="center"),
            ft.Text("Quantidade", width=100, color="black", text_align="center"),
            ft.Text("Ação", width=70, color="black", text_align="center"),  # Coluna de ação
        ],
        alignment="start",
        spacing=5,
    )

    # Container para os produtos com rolagem
    product_rows = []
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO)

    # Gerar linhas para cada produto
    for product in products:
        product_id, name, price, category, quantity = product
        row = {
            'id': product_id,  # Armazenar o ID diretamente
            'row': ft.Row(  # Contêiner da linha do produto
                [
                    ft.Text(value=product_id, color="black", width=50, size=15),
                    ft.TextField(value=name, color="black", bgcolor=ft.colors.GREEN_400, width=140, height=40),
                    ft.TextField(value=str(price), color="black", bgcolor=ft.colors.GREEN_400, width=100, height=40),
                    ft.TextField(value=category, color="black", bgcolor=ft.colors.GREEN_400, width=200, height=40),
                    ft.TextField(value=str(quantity), color="black", bgcolor=ft.colors.GREEN_400, width=100, height=40),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.RED,
                        tooltip="Excluir Produto",
                        on_click=lambda e, product_id=product_id: delete_product_row(e, product_id),  # Passar o ID do produto
                    )
                ],
                alignment="start",
                spacing=5,
            )
        }
        product_rows.append(row)
        product_list.controls.append(row['row'])  # Adicionar a linha ao contêiner de produtos

    # Botão para salvar
    save_button = ft.ElevatedButton(
        text="Salvar Alterações",
        icon_color=ft.colors.GREEN,
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        color="WHITE",
        on_click=save_changes
    )

    # Adicionar cabeçalhos, lista de produtos e botão de salvar à página
    page.add(
        ft.Column(
            [
                table_header,
                ft.Container(content=product_list, height=400, width=650),
                save_button
            ],
            alignment="center",
            spacing=10
        )
    )

# Executa a aplicação
ft.app(target=main)
