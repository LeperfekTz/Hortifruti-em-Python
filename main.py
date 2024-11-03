import flet as ft
import sqlite3
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




# Função para carregar produtos do banco de dados
def load_products():
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    products = cursor.fetchall()
    conn.close()
    return products

# Função para deletar um produto
def delete_product(product_id):
    conn = sqlite3.connect("database_hortifruti-py.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

# Função para abrir a janela de edição
def abrir_janela_edicao(page):
    products = load_products()
    product_rows = []
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    page.update()

    def product_exists(product_id):
        conn = sqlite3.connect("database_hortifruti-py.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def update_product(product_id, name, price, category, quantity):
        try:
            conn = sqlite3.connect("database_hortifruti-py.db")
            cursor = conn.cursor()
            cursor.execute(""" 
                UPDATE produtos 
                SET nome = ?, preco = ?, categoria = ?, quantidade = ? 
                WHERE id = ? 
            """, (name, price, category, quantity, product_id))
            
            affected_rows = cursor.rowcount  # Número de linhas afetadas
            conn.commit()
            logging.info(f"Atualização: {affected_rows} linha(s) afetada(s).")  # Usando logging para depuração
        except Exception as e:
            logging.error(f"Ocorreu um erro ao atualizar o produto: {e}")
        finally:
            conn.close()

    def save_changes(e):
        for row in product_rows:
            product_id = row['id']
            name = row['name'].value
            price = float(row['price'].value)
            category = row['category'].value
            quantity = int(row['quantity'].value)

            # Verifica se o produto existe antes de tentar atualizar
            if product_exists(product_id):
                update_product(product_id, name, price, category, quantity)
            else:
                logging.warning(f"Produto com ID {product_id} não encontrado.")  # Mensagem de erro para depuração

        # Recarrega a lista de produtos após a atualização
        product_rows.clear()  # Limpa a lista atual
        products.clear()
        products.extend(load_products())  # Recarrega os produtos

        page.snack_bar = ft.SnackBar(ft.Text("Alterações salvas com sucesso!"), bgcolor="green") 
        page.snack_bar.open = True
        page.update()

    def delete_product_row(e, product_id):
        # Verifica se o produto realmente existe antes de tentar deletá-lo
        if product_exists(product_id):
            try:
                delete_product(product_id)  # Remove o produto do banco de dados
                for row in product_rows:
                    if row['id'] == product_id:
                        product_list.controls.remove(row['row'])  # Remove a linha da lista
                        product_rows.remove(row)  # Remove da lista de produtos
                        break
            except Exception as ex:
                logging.error(f"Erro ao tentar deletar o produto: {ex}")
                page.snack_bar = ft.SnackBar(ft.Text("Erro ao excluir o produto!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
            else:
                # Atualiza a página após a remoção
                page.update()
        else:
            logging.warning(f"Produto com ID {product_id} não encontrado para exclusão.")

    def filter_products(e):
        search_term = search_field.value.lower()
        product_list.controls.clear()
        for product in products:
            product_id, name, price, category, quantity = product
            if (search_term in name.lower() or
                search_term in category.lower() or
                search_term in str(price)):
                # Campos de edição do produto
                name_field = ft.TextField(value=name, width=510,color="black",bgcolor=ft.colors.GREEN_100)
                price_field = ft.TextField(value=str(price), width=510,color="black",bgcolor=ft.colors.GREEN_100)
                category_field = ft.TextField(value=category, width=510,color="black",bgcolor=ft.colors.GREEN_100)
                quantity_field = ft.TextField(value=str(quantity), width=510,color="black",bgcolor=ft.colors.GREEN_100)

                category = str(category) if category else ""
                

                categoria_dropdown = ft.Dropdown(
                    label=category,
                    width=270,
                    bgcolor=ft.colors.GREEN_100,
                    border_color="green", 
                    border_width=1,
                    color="black", 
                    
                    label_style=ft.TextStyle(color="black"),
                    options=[
                        ft.dropdown.Option("Frutas"),
                        ft.dropdown.Option("Verduras"),
                        ft.dropdown.Option("Legumes"),
                        ft.dropdown.Option("Grãos"),
                        ft.dropdown.Option("Laticínios"),
                    ],
                    
                )

                category_field.value = category

                # Linha de produto
                row = {
                    'id': product_id,
                    'name': name_field,
                    'price': price_field,
                    'category': category_field,
                    'quantity': quantity_field,
                    'row': ft.Row(
                        [  
                            ft.Text(value=product_id,color="black", width=50, text_align="center"),
                            ft.Column(
                                [
                                    ft.Text("Nome:",color="black", weight="bold"),
                                    name_field
                                ],
                                alignment="start",
                                spacing=2,
                                width=220,
                                
                            ),
                            ft.Column(
                                [
                                    ft.Text("Preço:",color="black", weight="bold"),
                                    price_field
                                ],
                                alignment="start", 
                                spacing=2,
                                width=100
                            ),
                            ft.Column(
                                [
                                    ft.Text("Categoria:",color="black", weight="bold"),
                                    categoria_dropdown
                                ],
                                alignment="start",
                                spacing=2,
                                width=150
                            ),
                            ft.Column(
                                [
                                    ft.Text("Qtd:",color="black", weight="bold"),
                                    quantity_field
                                ], 
                                alignment="start",
                                spacing=2,
                                width=60,
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Excluir Produto",
                                on_click=lambda e, product_id=product_id: delete_product_row(e, product_id),  # Cor de fundo do botão
                                icon_color=ft.colors.RED,   # Cor do ícone
                            )
                        ],
                        alignment="center", 
                        spacing=10,
                    )
                }

                product_rows.append(row)
                product_list.controls.append(row['row'])
        page.update()

    search_field = ft.TextField(
        label="Pesquisar produtos",
        bgcolor="#f2f2f2",
        width=500,
        color=ft.colors.BLACK,
        border_color="green",
        label_style=ft.TextStyle(color=ft.colors.BLACK),
        on_change=filter_products,
        icon=ft.icons.SEARCH
    )


    save_button = ft.ElevatedButton(
        text="Salvar Alterações",
        color="green",
        icon_color="white",
        icon=ft.icons.SAVE,
        on_click=save_changes,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.all(10))
    )

    back_button = ft.ElevatedButton(
        text="Voltar",
        icon=ft.icons.ARROW_BACK,
        color="green",
        icon_color="white", 
        on_click=lambda e: close_dialog(),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.all(10))
    )

    def close_dialog():
        page.window_fullscreen = True  # Retornar ao modo normal, se necessário
        page.dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Editar Produtos", color=ft.colors.BLACK, size=20, weight="bold"),
        bgcolor="#f2f2f2",
        content=ft.Column(
            [
                search_field,
                ft.Container(content=product_list, width=900, expand=True),  
                save_button,   
                back_button,
                
            ], 
            spacing=10,
            
        ),
        on_dismiss=lambda e: page.update(),
        modal=True,
        open=True
    )

    page.dialog = dialog
    page.update()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pesquisa_input = ft.Ref[ft.TextField]()


def main(page: ft.Page):
    page.title = "ERP Hortifruti"
    page.bgcolor = "#f2f2f2" # Cor de fundo do app
    page.window_maximized = True # Maximiza a janela da aplicação

    

    def conectar_db():
        try:
            conn = sqlite3.connect('database_hortifruti-py.db')
            logging.info("Conexão ao banco de dados estabelecida com sucesso.")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None  # Retorna None em caso de erro

    def obter_produtos(pesquisa=None, id_produto=None):
        conn = conectar_db()  # Conecta ao banco de dados
        if conn is None:
            return []  # Retorna uma lista vazia se a conexão falhar

        cursor = conn.cursor()  # Cria o cursor a partir da conexão

        if id_produto is not None:
            query = "SELECT * FROM produtos WHERE id = ?"
            parametros = (id_produto,)  # Busca pelo ID específico

        elif pesquisa:
            query = "SELECT * FROM produtos WHERE nome LIKE ?"
            parametros = (f"%{pesquisa}%",)  # Wildcards para busca pelo nome
        
        else:
            query = "SELECT * FROM produtos"
            parametros = ()
        
        try:
            cursor.execute(query, parametros)  # Execute a consulta
            produtos = cursor.fetchall()  # Obtenha todos os resultados
        except sqlite3.Error as e:
            logging.error(f"Erro ao obter produtos: {e}")
            produtos = []  # Retorna uma lista vazia em caso de erro
        finally:
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão com o banco de dados
        
        return produtos  # Retorna os produtos encontrados

    # Função para listar produtos na tabela
    def listar_produtos(pesquisa=None):
        produtos = obter_produtos(pesquisa)  # Função que busca produtos no banco de dados
        data_rows = []  # Lista para armazenar as linhas da tabela

        for produto in produtos:
            quantidade_input = ft.TextField(
                hint_text="Qtd.",
                label_style=ft.TextStyle(color=ft.colors.BLACK), 
                border_color=ft.colors.GREEN,
                color=ft.colors.BLACK,
                width=80,
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            
            # Captura os valores de 'produto' e 'quantidade_input'
            venda_button = ft.ElevatedButton(
                "Add",
                on_click=lambda e,
                p=produto,
                q=quantidade_input: vender_produto(e, p, q),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                color="black",
                bgcolor="green", 
                icon=ft.icons.ADD,
                icon_color="RED",
            )
            
            # Adiciona uma linha de dados para a tabela
            data_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(produto[0]), color=ft.colors.BLACK)),  # ID do produto
                    ft.DataCell(ft.Text(produto[1], color=ft.colors.BLACK)),  # Nome do produto
                    ft.DataCell(ft.Text(f"R$ {float(produto[2]):.2f}", color=ft.colors.BLACK)),  # Preço do produto
                    ft.DataCell(ft.Text(str(produto[4]), color=ft.colors.BLACK)),  # Quantidade em estoque
                    ft.DataCell(quantidade_input),  # Campo de entrada de quantidade
                    ft.DataCell(venda_button),  # Botão de venda
                ])
            )

        # Atualiza a tabela com as novas linhas
        produtos_table.rows = data_rows
        page.update()

    def listar_historico():
        conn = conectar_db()
        
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historico_vendas") 
        sales = cursor.fetchall()

        # Clear the current lines of the historic
        historic_rows = []

        for sale in sales:
            historic_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(sale[1], color=ft.colors.BLACK)),  # Product
                    ft.DataCell(ft.Text(f"R${float(sale[3]):.2f}", color=ft.colors.BLACK)),  # Total Price
                    ft.DataCell(ft.Text(str(sale[2]), color=ft.colors.BLACK)),  # Quantity
                    ft.DataCell(ft.Text(sale[4], color=ft.colors.BLACK)),  # Date
                ]) 
            )

        # Adiciona um DataRow para o botão de limpar histórico fora da contagem de células
        historic_rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(
                    ft.ElevatedButton(
                        "Limpar Histórico",
                        on_click=lambda e, sale_id=sale[0]: limpar_historico(sale_id),
                        color="black",
                        bgcolor="red",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.all(10)),
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.WHITE,
                    )
                )
            ])
        )

        historico_table.rows = historic_rows
        page.update()
        conn.close()

    def vender_produto(e, produto, quantidade_input):
        try:
            quantidade = int(quantidade_input.value)

            # Verifica se a quantidade é válida
            if quantidade > 0 and quantidade <= produto[4]:
                conn = conectar_db()
                if conn:
                    cursor = conn.cursor()

                    # Atualiza a quantidade do produto na tabela produtos
                    cursor.execute(
                        "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
                        (quantidade, produto[0])  # Usando o ID do produto
                    )

                    # Adiciona a venda na tabela vendas
                    # Atualiza o historico de vendas
                    cursor.execute(
                        "INSERT INTO historico_vendas (produto, quantidade, preco_total, data_venda) VALUES (?, ?, ?, ?)",  # Corrigido de 'produtos' para 'produto'
                        (produto[1], quantidade, quantidade * produto[2], dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    
                    conn.commit()  # Confirma as alterações
                    conn.close()

                    # Mensagem de sucesso
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"{quantidade} unidades de {produto[1]} vendidas!", color=ft.colors.GREEN)
                    )
                    page.snack_bar.open = True
                    page.update()

                    # Atualiza as tabelas de produtos e histórico
                    listar_produtos() 
                    listar_historico()  # Atualiza a listagem
                else:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Erro ao conectar ao banco de dados.", color=ft.colors.RED)
                    )
                    page.snack_bar.open = True
                    page.update()
            else:
                show_popup(
                    "Erro",
                    "Quantidade inválida ou maior que o estoque disponível."
                )
                page.snack_bar.open = True
                page.update()
        except ValueError:
            show_popup(
                "Erro", 
                "Insira um valor numérico válido para a quantidade.",
                color=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()

    # Cria uma tabela para listar produtos
    produtos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Produto", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Preço", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Estoque", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Quantidade", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("")),
        ],
        rows=[],  # Inicialmente vazio
        border_radius=10,
    )

    historico_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Produto", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Preço", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("quantidade", color=ft.colors.BLACK)),
            ft.DataColumn(ft.Text("Data", color=ft.colors.BLACK)),
        ],
        rows=[],  # Inicialmente vazio
        border_radius=10,
    )
    def limpar_historico(sale_id):
        conn = conectar_db()
        
        if conn is None:
            return

        cursor = conn.cursor()
        cursor.execute("DELETE FROM historico_vendas WHERE id = ?", (sale_id,))
        conn.commit()
        conn.close()

        # Atualiza a lista após a remoção
        listar_historico()  # Recarrega o histórico para refletir as mudanças

    def mostrar_tela_vendas():
        listar_produtos()  # Preenche a tabela com produtos
        return ft.Column(
            [
                ft.Text("Tela de Vendas", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.Divider(height=6, thickness=1),
                ft.Row([
                    ft.TextField(label="Pesquisar",bgcolor="#f2f2f2",label_style=ft.TextStyle(color=ft.colors.BLACK),border_color=ft.colors.GREEN, color=ft.colors.BLACK, width=200, ref=pesquisa_input),
                    ft.ElevatedButton("Buscar",color="black",icon=ft.icons.SEARCH,bgcolor="#f2f2f2",on_click=lambda e: listar_produtos(pesquisa_input.current.value)), 
                ]),
                ft.Row(  # Coloca as tabelas lado a lado
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Column(  # Coluna para produtos
                            controls=[
                                ft.Text("Produtos", color='black', weight=ft.FontWeight.W_200, size=30),
                                ft.Container(
                                    content=ft.ListView(
                                        controls=[produtos_table],
                                        width=700,  # Largura ajustada para caber lado acomo lado
                                        height=400,
                                    ),
                                    border=ft.border.all(2, ft.colors.GREEN),
                                    border_radius=10,
                                    bgcolor="#f2f2f2", 
                                ),
                                ft.ElevatedButton(
                                    "Editar produtos",
                                    on_click=lambda _: abrir_janela_edicao(page),
                                    color="black",
                                    bgcolor="green",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.all(10)),
                                    icon=ft.icons.EDIT_NOTE,
                                    icon_color=ft.colors.RED,
                                    ) 
                            ],
                            alignment=ft.MainAxisAlignment.START,  # Alinhamento vertical para a coluna
                        ),
                        ft.Column(  # Coluna para histórico de vendas
                            controls=[
                                ft.Text("Histórico de vendas", color='black', weight=ft.FontWeight.W_200, size=30),
                                ft.Container(
                                    content=ft.ListView( 
                                        controls=[historico_table],
                                        width=700,  # Largura ajustada para caber lado a lado
                                        height=400,
                                    ), 
                                    border=ft.border.all(2, ft.colors.GREEN),
                                    border_radius=10,  
                                    bgcolor="#f2f2f2",
                                    ),
                                ft.ElevatedButton(
                                    "Limpar Histórico",
                                    on_click=limpar_historico,
                                    color="black",
                                    bgcolor="green",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.all(10)),
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED,
                                    )
                                    
                                ],
                                
                                alignment=ft.MainAxisAlignment.START,  # Alinhamento vertical para a coluna
                            ),
                        ]
                    ) 
                ] 
            )


    def fetch_records():
        conn = sqlite3.connect('database_hortifruti-py.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM caixa')
        records = cursor.fetchall()
        conn.close()
        return records

    def mostrar_tela_caixa():
        records = fetch_records()  # Supondo que você tenha uma função que busca os registros

        # Cria as linhas do DataTable a partir dos registros
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(record[0], color='black', weight=ft.FontWeight.W_200)),  # ID
                    ft.DataCell(ft.Text(record[2], color='black', weight=ft.FontWeight.W_200)),  # Produto
                    ft.DataCell(ft.Text(record[4], color='black', weight=ft.FontWeight.W_200)),  # Preço
                    ft.DataCell(ft.Text(record[3], color='black', weight=ft.FontWeight.W_200)),  # Quantidade
                    ft.DataCell(ft.Text(record[1], color='black', weight=ft.FontWeight.W_200)),  # Data
                ]
            )
            for record in records
        ]

        # Cria o DataTable
        historico_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", color=ft.colors.BLACK)),
                ft.DataColumn(ft.Text("Produto", color=ft.colors.BLACK)),
                ft.DataColumn(ft.Text("Preço", color=ft.colors.BLACK)),
                ft.DataColumn(ft.Text("Quantidade", color=ft.colors.BLACK)),
                ft.DataColumn(ft.Text("Data", color=ft.colors.BLACK)),
            ],
            rows=rows,
                border_radius=10,
                border=ft.border.all(2, ft.colors.GREEN),
                bgcolor="#f2f2f2",
        )

        # Cria o ListView para permitir rolagem
        list_view = ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(record[0], width=50, color='black'),  # ID
                        ft.Text(record[2], width=100, color='black'),  # Produto
                        ft.Text(record[4], width=100, color='black'),  # Preço
                        ft.Text(record[3], width=100, color='black'),  # Quantidade
                        ft.Text(record[1], width=110, color='black'),  # Data
                    ]
                )
                for record in records
            ],
            width=700,
            height=400,  # Define a altura do ListView
        )

        # Cria a coluna principal com o cabeçalho fixo e o conteúdo rolável
        main_column = ft.Column(
            controls=[
                ft.Text("Histórico de Vendas", color=ft.colors.BLACK, size=24, weight=ft.FontWeight.BOLD),
                list_view  # O ListView já tem rolagem
            ],
            spacing=10,
        )

        return main_column



    def adicionar_produto(nome, preco, quantidade, categoria):
        conn = conectar_db()  # Usa a função de conexão
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (nome, preco, quantidade, categoria) 
                VALUES (?, ?, ?, ?)
            ''', (nome, preco, quantidade, categoria))
            conn.commit()
            conn.close()
        else:
            logging.error("Não foi possível conectar ao banco de dados.")

    # Função para mostrar a tela de cadastro
    def mostrar_tela_cadastro():
        nome_produto = ft.TextField()
        preco_produto = ft.TextField()
        quantidade_produto = ft.TextField()

        # Dropdown para seleção de categoria
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            width=270,
            bgcolor="#f2f2f2",
            border_color="green",
            border_width=1,
            color="black", 
            label_style=ft.TextStyle(color="black"),
            options=[
                ft.dropdown.Option("Frutas"),
                ft.dropdown.Option("Verduras"),
                ft.dropdown.Option("Legumes"),
                ft.dropdown.Option("Grãos"),
                ft.dropdown.Option("Laticínios"),
            ],
        )

        def on_adicionar_produto(e):
            nome = nome_produto.value
            preco = float(preco_produto.value)  # Converte para float
            quantidade = int(quantidade_produto.value)  # Converte para inteiro
            categoria = categoria_dropdown.value  # Pega o valor selecionado do dropdown
            adicionar_produto(nome, preco, quantidade, categoria)  # Passa a categoria

            # Limpa os campos após adicionar
            nome_produto.value = ""
            preco_produto.value = ""
            quantidade_produto.value = ""
            categoria_dropdown.value = None  # Limpa a seleção do dropdown
            
            # Atualiza a interface
            page.update()

        return ft.Column(
            [
                ft.Text("Cadastro de Produtos", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                nome_produto := ft.TextField(label="Nome do Produto", bgcolor="#f2f2f2", label_style=ft.TextStyle(color=ft.colors.BLACK), border_color=ft.colors.GREEN, hint_text="Insira o nome", color=ft.colors.BLACK, width=300),
                preco_produto := ft.TextField(label="Preço", width=300, bgcolor="#f2f2f2", keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK, hint_text="Digite o valor", label_style=ft.TextStyle(color=ft.colors.BLACK), border_color=ft.colors.GREEN),
                quantidade_produto := ft.TextField(label="Quantidade em Estoque", bgcolor="#f2f2f2", label_style=ft.TextStyle(color=ft.colors.BLACK), border_color=ft.colors.GREEN, width=300, keyboard_type=ft.KeyboardType.NUMBER, color=ft.colors.BLACK, hint_text="Digite a quantidade"),
                ft.Row(
                    [
                        categoria_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.ElevatedButton(
                    "Adicionar Produto",
                    color=ft.colors.BLACK, 
                    bgcolor=ft.colors.GREEN_300,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=on_adicionar_produto  # Adiciona o evento de clique
                ), 
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def mostrar_tela_relatorios():
        return ft.Column(
            [

            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
    def show_popup(title, message, color=ft.colors.RED):
        # Cria o conteúdo do dialog
        dialog = ft.AlertDialog(
            title=ft.Text(title, color=ft.colors.BLACK),  # Título do popup
            content=ft.Text(message, color=ft.colors.WHITE),  # Mensagem do popup
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_popup(dialog)),  # Botão de fechar o popup
            ],
            actions_alignment=ft.MainAxisAlignment.END,  # Alinha o botão à direita
            bgcolor=color,  # Cor de fundo do popup
            shape=ft.RoundedRectangleBorder(radius=10),  # Forma arredondada
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Função para fechar o AlertDialog
    def close_popup(dialog):
        dialog.open = False
        page.update()


    # Função para fechar o SnackBar
    def close_snack_bar():
        page.snack_bar.open = False
        page.update()


    # Função para alternar entre telas com base na seleção da NavigationRail
    def trocar_tela(e):
        if rail.selected_index == 0:
            corpo.content = mostrar_tela_cadastro()
        elif rail.selected_index == 1:
            corpo.content = mostrar_tela_vendas()  # Chama a função que mostra a tela de vendas
        elif rail.selected_index == 2:
            corpo.content = mostrar_tela_relatorios()
        elif rail.selected_index == 3:
            corpo.content = mostrar_tela_caixa()
        page.update()

    # NavigationRail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL, 
        min_width=100, 
        bgcolor=ft.colors.GREEN_100,
        indicator_color='black',
        indicator_shape=ft.RoundedRectangleBorder(radius=10),
        leading=ft.FloatingActionButton(icon=ft.icons.EXIT_TO_APP,width=80,height=50,text="Sair",bgcolor=ft.colors.RED_500,on_click=lambda e: page.window.destroy()),
        group_alignment=-0.9,
        selected_label_text_style=ft.TextStyle(color="black"),  # Estilo do label selecionado
        unselected_label_text_style=ft.TextStyle(color="black"),
        destinations=[
            ft.NavigationRailDestination( 
                icon_content=ft.Icon(ft.icons.ASSIGNMENT_ADD,color="black"),
                selected_icon_content=ft.Icon(ft.icons.ASSIGNMENT_ADD,color="green"),   
                label="Cadastro",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PAYMENT,color="black"),
                selected_icon_content=ft.Icon(ft.icons.PAYMENT,color="green"),
                label="Vendas",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.RECEIPT_LONG,color="black"),
                selected_icon_content=ft.Icon(ft.icons.RECEIPT_LONG,color="green"),
                label="Relatórios",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.POINT_OF_SALE,color="black"),
                selected_icon_content=ft.Icon(ft.icons.POINT_OF_SALE,color="green"),
                label="Caixa", 
            ),
        ],
        on_change=trocar_tela,

    )

    corpo = ft.Container(content=mostrar_tela_cadastro())

    # Corpo da aplicação



    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=5 , color="black"),
                corpo,
            ],
            expand=True,
        )
    ) 

# Executa a aplicação
if __name__ == "__main__":
    ft.app(target=main)  