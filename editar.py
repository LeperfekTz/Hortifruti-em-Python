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

# Função que inicializa a interface
def main(page: ft.Page):
    page.title = "Editar Produtos"
    page.scroll = ft.ScrollMode.AUTO  # Permite rolagem na página
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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

    # Cabeçalhos da tabela com cor de fundo e alinhamento centralizado
    table_header = ft.Row(
        [
            ft.Text("ID", width=50, text_align="center"),
            ft.Text("Nome", width=140, text_align="center"),
            ft.Text("Preço", width=100, text_align="center"),
            ft.Text("Categoria", width=200, text_align="center"),
            ft.Text("Quantidade", width=100, text_align="center"),
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
            'id': product_id,
            'name': ft.TextField(value=name, width=140, height=40),
            'price': ft.TextField(value=str(price), width=100, height=40),
            'category': ft.TextField(value=category, width=200, height=40),
            'quantity': ft.TextField(value=str(quantity), width=100, height=40)
        }
        product_rows.append(row)
        product_list.controls.append(
            ft.Row(
                [
                    ft.Text(str(product_id), width=50, text_align="center"),
                    row['name'],
                    row['price'],
                    row['category'],
                    row['quantity']
                ],
                alignment="start",
                spacing=5,
            )
        )

    # Botão para salvar
    save_button = ft.ElevatedButton(text="Salvar Alterações", on_click=save_changes)

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
