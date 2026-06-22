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
    </style>
""", unsafe_allow_html=True)

st.title("📊 Engenharia Financeira")
st.subheader("Basis Capital — Estratégia 180 Meses")
st.markdown("---")

# 1. Campos de Entrada com formatação corrigida para evitar o erro do Streamlit
credito_nominal = st.number_input(
    "Valor NOMINAL do Consórcio (R$):", 
    min_value=0.0, 
    value=500000.0, 
    step=10000.0,
    format="%.2f"
)

entrada_bolso = st.number_input(
    "Aporte / Entrada do Bolso (R$):", 
    min_value=0.0, 
    value=0.0, 
    step=5000.0,
    format="%.2f"
)

# Chave liga/desliga para o embutido
usar_embutido = st.toggle("Utilizar Lance Embutido (30%)", value=True)

# ====== AJUSTE INTELIGENTE DO FATOR DA TABELA REAL =====
if credito_nominal >= 300000.0:
    FATOR_TABELA = 0.005590  # Cravado: 500k -> Parcela Cheia R$ 2.795,00 / Meia R$ 1.397,50
else:
    FATOR_TABELA = 0.006830  # Cravado: 100k -> Meia Parcela R$ 341,50

# 2. Execução dos Cálculos Matemáticos
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

# 3. Interface Visual do Aplicativo
st.markdown("### 📉 Pré-Contemplação")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">MEIA PARCELA (ESPERA)</div><div class="metric-value">R$ {meia_parcela:,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">PARCELA INTEGRAL</div><div class="metric-value">R$ {parcela_integral_original:,.2f}</div></div>', unsafe_allow_html=True)

st.markdown("### 🔑 Na Contemplação")
st.info(f"🎯 **CRÉDITO LÍQUIDO DISPONÍVEL:** R$ {credito_liquido:,.2f}")

col3, col4 = st.columns(2)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">LANCE TOTAL</div><div class="metric-value">R$ {lance_total:,.2f}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">PERCENTUAL LANCE</div><div class="metric-value">{((lance_total/credito_nominal)*100):.1f}%</div></div>', unsafe_allow_html=True)

st.markdown("### 🏢 Pós-Contemplação")
st.warning(f"💡 **Nova Parcela Recalculada:** R$ {nova_parcela_integral:,.2f} / mês")

# Abas interativas para os cenários comerciais
tab1, tab2 = st.tabs(["💼 Cenário A: Imóvel", "📈 Cenário B: Renda Fixa"])

with tab1:
    st.markdown(f"**Aluguel Estimado (0.7%):** R$ {aluguel_estimado:,.2f} / mês")
    if sobra_imovel >= 0:
        st.success(f"🎉 **SOBRA NO BOLSO:** + R$ {sobra_imovel:,.2f} / mês")
    else:
        st.error(
