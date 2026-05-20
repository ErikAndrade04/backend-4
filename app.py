from flask import Flask, render_template, request, redirect, url_for, flash
 
app = Flask(__name__)
app.secret_key = 'delivery_secret_key_2024'
lanches = [
    {
         'id': 1,
        'nome': 'Hambúrguer Artesanal',
        'descricao': 'Hambúrguer com queijo e bacon',
        'categoria': 'Hambúrguer',
        'preco': 29.90,
        'destaque': True
    }
    ,
    {
        'id': 2,
        'nome': 'Pizza Calabresa',
        'descricao': 'Pizza tradicional de calabresa',
        'categoria': 'Pizza',
        'preco': 45.00,
        'destaque': True
    },
    {
        'id': 3,
        'nome': 'Refrigerante',
        'descricao': 'Lata 350ml',
        'categoria': 'Bebida',
        'preco': 6.50,
        'destaque': False
    }
]

@app.route('/')
def index():
    destaques = [l for l in lanches if l['destaque']]
    total_pedidos = len(pedidos)
    total_clientes = len(clientes)
    return render_template('index.html',
                           destaques=destaques,
                           total_pedidos=total_pedidos,
                           total_clientes=total_clientes)
clientes = [
    {
        'id': 1,
        'nome': 'João',
        'email': 'joao@email.com'
    },
    {
        'id': 2,
        'nome': 'Maria',
        'email': 'maria@email.com'
    }
]

pedidos = [
    {
        'id': 1,
        'cliente_id': 1,
        'status': 'Em preparo'
    },
    {
        'id': 2,
        'cliente_id': 2,
        'status': 'Entregue'
    }
]
 
@app.route('/cardapio')
def cardapio():
    categorias = sorted(set(l['categoria'] for l in lanches))
    categoria_filtro = request.args.get('categoria', '')
    if categoria_filtro:
        lista = [l for l in lanches if l['categoria'] == categoria_filtro]
    else:
        lista = lanches
    return render_template('cardapio.html',
                           lanches=lista,
                           categorias=categorias,
                           categoria_filtro=categoria_filtro)
 
@app.route('/pedidos')
def pedidos_lista():
    status_filtro = request.args.get('status', '')
    if status_filtro:
        lista = [p for p in pedidos if p['status'] == status_filtro]
    else:
        lista = pedidos
    status_opcoes = sorted(set(p['status'] for p in pedidos))
    return render_template('pedidos.html',
                           pedidos=lista,
                           status_opcoes=status_opcoes,
                           status_filtro=status_filtro)
 
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome    = request.form.get('nome', '').strip()
        email   = request.form.get('email', '').strip()
        assunto = request.form.get('assunto', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        if nome and email and mensagem:
            flash(f'Mensagem enviada com sucesso, {nome}! Retornaremos em breve.', 'success')
        else:
            flash('Preencha todos os campos obrigatórios.', 'danger')
        return redirect(url_for('contato'))
    return render_template('contato.html')
 
@app.route('/cliente/<int:cliente_id>')
def cliente_detalhe(cliente_id):
    cliente = next((c for c in clientes if c['id'] == cliente_id), None)
    if cliente is None:
        return render_template('404.html', mensagem=f'Cliente #{cliente_id} não encontrado.'), 404
    pedidos_cliente = [p for p in pedidos if p['cliente_id'] == cliente_id]
    return render_template('cliente_detalhe.html',
                           cliente=cliente,
                           pedidos=pedidos_cliente)
 
 
@app.route('/lanche/<int:lanche_id>')
def lanche_detalhe(lanche_id):
    lanche = next((l for l in lanches if l['id'] == lanche_id), None)
    if lanche is None:
        return render_template('404.html', mensagem=f'Lanche #{lanche_id} não encontrado.'), 404
    similares = [l for l in lanches if l['categoria'] == lanche['categoria'] and l['id'] != lanche_id][:3]
    return render_template('lanche_detalhe.html',
                           lanche=lanche,
                           similares=similares)
 
 
@app.route('/clientes')
def clientes_lista():
    return render_template('clientes.html', clientes=clientes)
if __name__ == '__main__':
    app.run(debug=True)