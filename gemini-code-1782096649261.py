import streamlit as st

# Configuração de página para mobile
st.set_page_config(
    page_title="Simulador Basis Capital", 
    page_icon="📊", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização visual dos blocos de resposta (Cards)
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0066cc;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 14px;
        color: #6c757d;
        font-weight: bold;
    }
    .metric-value {
        font-size: 22px;
        color: #212529;
        font-weight: bold;
    }
    .money-label {
        font-size: 16px;
        color: #0066cc;
        font-weight: bold;
        margin-top: -10px;
        margin-bottom: 15px;
    }
    .explanation-box {
        background-color: #f1f8ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Engenharia Financeira")
st.subheader("Basis Capital — Estratégia 180 Meses")
st.markdown("---")

# Função auxiliar para formatação de moeda no padrão brasileiro (R$ 1.000,00)
def m(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. Entrada de Dados (Apenas digitação direta)
credito_nominal = st.number_input(
    "Valor NOMINAL do Consórcio (R$):", 
    min_value=0, 
    value=500000, 
    step=10000
)
st.markdown(f'<div class="money-label">Crédito Selecionado: {m(credito_nominal)}</div>', unsafe_allow_html=True)

entrada_bolso = st.number_input(
    "Aporte / Entrada do Bolso (R$):", 
    min_value=0, 
    value=0, 
    step=5000
)
st.markdown(f'<div class="money-label">Aporte do Bolso: {m(entrada_bolso)}</div>', unsafe_allow_html=True)

# Chave liga/desliga para o embutido
usar_embutido = st.toggle("Utilizar Lance Embutido (30%)", value=True)

# ====== AJUSTE INTELIGENTE DO FATOR DA TABELA REAL =====
if credito_nominal >= 300000:
    FATOR_TABELA = 0.005590  # Cravado: 500k -> Parcela Cheia R$ 2.795,00 / Meia R$ 1.397,50
else:
    FATOR_TABELA = 0.006830  # Cravado: 100k -> Meia Parcela R$ 341,50

# 2. Execução dos Cálculos Matemáticos Reais
parcela_integral_original = credito_nominal * FATOR_TABELA
meia_parcela = parcela_integral_original * 0.50

if usar_embutido:
    lance_embutido = credito_nominal * 0.30
    credito_liquido = credito_nominal - lance_embutido
    proporcao_abatimento_embutido = 0.70
else:
    lance_embutido = 0.0
    credito_liquido = credito_nominal
    proporcao_abatimento_embutido = 1.0

lance_total = lance_embutido + entrada_bolso

# Recálculo do Saldo Devedor e Nova Parcela pós-contemplação
saldo_total_com_taxas = parcela_integral_original * 180
saldo_devedor_pos_embutido = saldo_total_com_taxas * proporcao_abatimento_embutido
saldo_devedor_final = max(0.0, saldo_devedor_pos_embutido - entrada_bolso)
nova_parcela_integral = saldo_devedor_final / 180

# Projeções de Rentabilidade
aluguel_estimado = credito_liquido * 0.007
sobra_imovel = aluguel_estimado - nova_parcela_integral

rendimento_rf = credito_liquido * 0.0095
sobra_rf = rendimento_rf - nova_parcela_integral

# 3. Interface Visual dos Resultados
st.markdown("---")
st.markdown("### 📉 Pré-Contemplação")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">MEIA PARCELA (ESPERA)</div><div class="metric-value">{m(meia_parcela)}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">PARCELA INTEGRAL</div><div class="metric-value">{m(parcela_integral_original)}</div></div>', unsafe_allow_html=True)

st.markdown("### 🔑 Na Contemplação")
st.info(f"🎯 **CRÉDITO LÍQUIDO DISPONÍVEL:** {m(credito_liquido)}")

col3, col4 = st.columns(2)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">LANCE TOTAL</div><div class="metric-value">{m(lance_total)}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">PERCENTUAL LANCE</div><div class="metric-value">{((lance_total/credito_nominal)*100):.1f}%</div></div>', unsafe_allow_html=True)

st.markdown("### 🏢 Pós-Contemplação")
st.warning(f"💡 **Nova Parcela Recalculada:** {m(nova_parcela_integral)} / mês")

# Abas interativas para os cenários comerciais
tab1, tab2 = st.tabs(["💼 Cenário A: Imóvel", "📈 Cenário B: Renda Fixa Inteligente"])

with tab1:
    st.markdown(f"**Aluguel Estimado (0.7%):** {m(aluguel_estimado)} / mês")
    if sobra_imovel >= 0:
        st.success(f"🎉 **SOBRA NO BOLSO:** + {m(sobra_imovel)} / mês")
    else:
        st.error(f"📉 **ESFORÇO LÍQUIDO:** - {m(abs(sobra_imovel))} / mês")

with tab2:
    st.markdown("### 🔍 Estratégia de Alavancagem em Renda Fixa")
    st.markdown(
        f"""
        <div class="explanation-box">
            <strong>Como funciona esta operação?</strong><br>
            Ao invés de comprar um patrimônio físico, o capital líquido liberado de 
            <strong>{m(credito_liquido)}</strong> é integralmente aplicado em uma estrutura de ativos de 
            Renda Fixa/LCI/FIIs estruturados, gerando uma taxa média estimada de <strong>0,95% ao mês</strong> de forma isenta ou líquida.
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Detalhamento dos valores para o cliente
    st.write(f"📈 **Rendimento Bruto da Aplicação:** {m(rendimento_rf)} / mês")
    st.write(f"📉 **Custo de Manutenção (Nova Parcela):** {m(nova_parcela_integral)} / mês")
    st.markdown("---")
    
    if sobra_rf >= 0:
        st.success(f"🎉 **RESULTADO POSITIVO (Venda de Renda):** O rendimento do próprio capital aplicado paga a parcela do consórcio e ainda sobra **{m(sobra_rf)} por mês** líquidos no bolso do seu cliente!")
    else:
        st.error(f"📉 **DIFERENÇA DE APORTE:** O rendimento cobre a maior parte da estrutura, restando apenas um esforço complementar de **{m(abs(sobra_rf))} por mês** para carregar o patrimônio alavancado.")

st.markdown("---")
st.caption("Uso exclusivo de prospecção — Basis Capital.")
