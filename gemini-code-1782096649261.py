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
        margin-top: 5px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Engenharia Financeira")
st.subheader("Basis Capital — Estratégia 180 Meses")
st.markdown("---")

# Função auxiliar para formatação de moeda no padrão brasileiro (R$ 1.000,00)
def m(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 1. Entrada de Dados de Alta Interatividade (Slider + Campo de Texto juntos!)
st.markdown("**Selecione ou Digite o Valor do Crédito:**")
credito_nominal = st.slider(
    "Arraste para ajustar rápido (R$):",
    min_value=100000,
    max_value=2000000,
    value=500000,
    step=50000
)
credito_nominal = st.number_input(
    "Ou digite o valor exato aqui (R$):", 
    min_value=0, 
    value=int(credito_nominal), 
    step=10000
)
st.markdown(f'<div class="money-label">Crédito Selecionado: {m(credito_nominal)}</div>', unsafe_allow_html=True)

st.markdown("---")

st.markdown("**Selecione ou Digite o Aporte do Bolso:**")
entrada_bolso = st.slider(
    "Arraste para ajustar a entrada (R$):",
    min_value=0,
    max_value=500000,
    value=0,
    step=10000
)
entrada_bolso = st.number_input(
    "Ou digite a entrada exata aqui (R$):", 
    min_value=0, 
    value=int(entrada_bolso), 
    step=5000
)
st.markdown(f'<div class="money-label">Aporte do Bolso: {m(entrada_bolso)}</div>', unsafe_allow_html=True)

# Chave liga/desliga para o embutido
usar_embutido = st.toggle("Utilizar Lance Embutido (30%)", value=True)

# ====== AJUSTE INTELIGENTE DO FATOR DA TABELA
