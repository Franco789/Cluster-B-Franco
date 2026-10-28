import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURACIÓN Y ESTÉTICA INSTITUCIONAL DE ALTO CONTRASTE (WCAG 2.1)
# ==============================================================================
st.set_page_config(
    page_title="Atlas Neurosemiológico del Clúster B | Ateneo Hospitalario",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<head>
<meta name="google" content="notranslate">
</head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #080C14 !important;
    color: #E2E8F0 !important;
}

.block-container {
    padding-top: 1.6rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 95% !important;
}

h1 {
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: #F8FAFC !important;
    margin-bottom: 0.2rem !important;
}

h2, h3, h4 {
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: #F1F5F9 !important;
}

div[data-testid="stMetric"] {
    background: #0F172A !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
}

div[data-testid="stMetric"] label {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #94A3B8 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important;
    background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding-bottom: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #0D1424 !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 6px !important;
    padding: 8px 18px !important;
    color: #94A3B8 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background: #1E293B !important;
    border-color: #38BDF8 !important;
    color: #38BDF8 !important;
}

section[data-testid="stSidebar"] {
    background-color: #090E18 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.stAlert {
    border-radius: 6px !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
}

textarea {
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace !important;
    font-size: 0.82rem !important;
    background-color: #060911 !important;
    color: #CBD5E1 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 6px !important;
    line-height: 1.45 !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. PANEL LATERAL: VARIABLES SELECCIONADAS
# ==============================================================================
st.sidebar.markdown("### Parámetros Clínicos")
st.sidebar.caption("Modelo Dimensional (HiTOP / DSM-5 III / Neurobiología):")

trastorno_foco = st.sidebar.selectbox(
    "1. Fenotipo Clínico en Evaluación",
    options=[
        "Trastorno Límite de la Personalidad (TLP)",
        "Trastorno Narcisista de la Personalidad (TNP)",
        "Trastorno Antisocial de la Personalidad (TASP)",
        "Trastorno Histriónico de la Personalidad (THP)"
    ],
    index=0
)

estresor_tipo = st.sidebar.selectbox(
    "2. Estresor Relacional en Guardia / Sala",
    options=[
        "Puesta de Límites: Indicación de egreso hospitalario sin internación",
        "Demora Asistencial: Espera prolongada o atención no inmediata",
        "Confrontación Técnica: Señalamiento de inconsistencia en el relato",
        "Distanciamiento Vincular: Conflicto agudo con referente afectivo"
    ],
    index=0
)

severidad_estres = st.sidebar.slider(
    "3. Carga Afectiva Percibida (0 a 100)",
    min_value=0, max_value=100, value=75, step=1,
    help="Graduación cuantitativa del estrés interpersonal. A mayor puntaje, mayor desacoplamiento prefrontal."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Farmacología de Guardia")

farmaco_1 = st.sidebar.selectbox(
    "Molécula Evaluada:",
    options=[
        "Abordaje Verbal y Contención del Encuadre (Sin psicofármacos)",
        "Clonazepam (2 mg Vía Oral)",
        "Lorazepam (2 mg Sublingual)",
        "Haloperidol (5 mg Intramuscular)",
        "Quetiapina (50 mg Vía Oral)",
        "Aripiprazol (5 mg Vía Oral)",
        "Lamotrigina (100 mg Vía Oral - Mantenimiento previo de base)"
    ],
    index=1
)

soporte_red = st.sidebar.radio(
    "Red Vincular Continente:",
    options=["Presente, continente y localizable", "Ausente, expulsiva o francamente disfuncional"],
    index=0
)

# ==============================================================================
# 3. BASE DE DATOS CLINICA, SEMIOLOGICA Y MODELO CUANTITATIVO
# ==============================================================================
perfiles_hitop = {
    "Trastorno Límite de la Personalidad (TLP)": {
        "Afecto Negativo": 95, "Desinhibición": 88, "Antagonismo": 45, "Desapego": 35, "Psicoticismo": 60,
        "color": "#F87171",
        "semiologia_clasica": "Inestabilidad en la vivencia del tiempo interno, discordancia afectiva y angustia básica difusa (Betta / Suárez Richards).",
        "mecanismo_defensa": "Escisión primaria (splitting) e identificación proyectiva masiva (Kernberg).",
        "vivencia_subjetiva": "Terror visceral al aniquilamiento por abandono; el dolor emocional se vive con la intensidad física de una herida tisular.",
        "impacto_equipo": "Inducción de culpa, angustia de rescate en el profesional y posterior sensación de agotamiento o impotencia.",
        "analogia_radar": "El polígono se dispara verticalmente hacia el dolor afectivo y la urgencia motora impulsiva."
    },
    "Trastorno Narcisista de la Personalidad (TNP)": {
        "Afecto Negativo": 50, "Desinhibición": 30, "Antagonismo": 96, "Desapego": 40, "Psicoticismo": 20,
        "color": "#FBBF24",
        "semiologia_clasica": "Estructuración sobre un Yo grandioso compensatorio frente a una extrema vulnerabilidad a la vergüenza y el desprecio (Schneider).",
        "mecanismo_defensa": "Desmentida de la vulnerabilidad, idealización propia y devaluación hostil del profesional.",
        "vivencia_subjetiva": "Humillación catastrófica oculta bajo una máscara de autosuficiencia; necesidad urgente de descalificar al médico.",
        "impacto_equipo": "Sensación de cuestionamiento técnico permanente, empequeñecimiento forzado y fastidio encubierto.",
        "analogia_radar": "El radar polariza de forma casi pura el vértice de antagonismo, manteniendo el autocontrol conductual intacto."
    },
    "Trastorno Antisocial de la Personalidad (TASP)": {
        "Afecto Negativo": 25, "Desinhibición": 92, "Antagonismo": 95, "Desapego": 30, "Psicoticismo": 25,
        "color": "#A78BFA",
        "semiologia_clasica": "Frialdad afectiva, aplanamiento del remordimiento y desprecio sostenido por los derechos ajenos (Schneider / Betta).",
        "mecanismo_defensa": "Paso al acto coactivo compulsivo (acting out) y racionalización instrumental de la agresión.",
        "vivencia_subjetiva": "El entorno asistencial es percibido como un campo de fuerzas a doblegar para obtener un beneficio inmediato.",
        "impacto_equipo": "Alerta somática real de peligro físico, hipervigilancia y tentación contratransferencial de adoptar actitudes punitivas.",
        "analogia_radar": "El polígono se ensancha hacia la transgresión desinhibida y el cálculo frío sin sufrimiento afectivo interno."
    },
    "Trastorno Histriónico de la Personalidad (THP)": {
        "Afecto Negativo": 80, "Desinhibición": 70, "Antagonismo": 55, "Desapego": 10, "Psicoticismo": 30,
        "color": "#22D3EE",
        "semiologia_clasica": "Labilidad afectiva de expresión llamativa pero superficial, sugestionabilidad y vivencia mítica del vínculo (Jaspers).",
        "mecanismo_defensa": "Disociación, somatización conversiva y erotización defensiva de la relación médico-paciente.",
        "vivencia_subjetiva": "Urgencia de cautivar la mirada del otro para confirmar la propia existencia; terror agudo a la indiferencia.",
        "impacto_equipo": "Interés o fascinación inicial en el equipo asistencial, seguida de saturación rápida por demanda afectiva continua.",
        "analogia_radar": "El polígono muestra alta proximidad relacional (bajo desapego) con labilidad pero sin fragmentación psicótica."
    }
}

p_actual = perfiles_hitop[trastorno_foco]

# Fisiopatología cuantitativa de circuitos
acoplamiento_base = 75.0 if "Narcisista" in trastorno_foco else (45.0 if "Límite" in trastorno_foco else 60.0)
factor_caida = (severidad_estres / 100.0) * 0.70
acoplamiento_frontal = float(np.clip(acoplamiento_base * (1.0 - factor_caida), 8.0, 95.0))
actividad_amigdala = float(np.clip((100.0 - acoplamiento_frontal) * (p_actual["Afecto Negativo"] / 100.0) * 1.2, 15.0, 100.0))

# Farmacodinamia cuantitativa
farmaco_datos = {
    "Abordaje Verbal y Contención del Encuadre (Sin psicofármacos)": {"d2": 0, "5ht2a": 0, "gaba": 0, "nav": 0, "riesgo_desin": 0, "riesgo_acatisia": 0, "tipo": "Intervención No Farmacológica"},
    "Clonazepam (2 mg Vía Oral)": {"d2": 0, "5ht2a": 0, "gaba": 88, "nav": 0, "riesgo_desin": 82, "riesgo_acatisia": 0, "tipo": "Benzodiacepina de Alta Potencia"},
    "Lorazepam (2 mg Sublingual)": {"d2": 0, "5ht2a": 0, "gaba": 85, "nav": 0, "riesgo_desin": 78, "riesgo_acatisia": 0, "tipo": "Benzodiacepina de Alta Potencia"},
    "Haloperidol (5 mg Intramuscular)": {"d2": 85, "5ht2a": 15, "gaba": 0, "nav": 0, "riesgo_desin": 5, "riesgo_acatisia": 88, "tipo": "Antipsicótico Típico Incisivo"},
    "Quetiapina (50 mg Vía Oral)": {"d2": 25, "5ht2a": 65, "gaba": 0, "nav": 0, "riesgo_desin": 12, "riesgo_acatisia": 5, "tipo": "Atípico / Sedativo Histaminérgico"},
    "Aripiprazol (5 mg Vía Oral)": {"d2": 72, "5ht2a": 60, "gaba": 0, "nav": 0, "riesgo_desin": 8, "riesgo_acatisia": 22, "tipo": "Agonista Parcial D2 / Estabilizador"},
    "Lamotrigina (100 mg Vía Oral - Mantenimiento previo de base)": {"d2": 0, "5ht2a": 0, "gaba": 0, "nav": 65, "riesgo_desin": 0, "riesgo_acatisia": 0, "tipo": "Modulador Glutamatérgico / Canales Na+ (Fármaco de Base)"}
}

f_eval = farmaco_datos[farmaco_1]

# Ponderación objetiva del riesgo asistencial (Art. 20 Ley 26.657)
pts_estres = severidad_estres * 0.35
pts_fenotipo = (p_actual["Desinhibición"] * 0.35) if "Límite" in trastorno_foco or "Antisocial" in trastorno_foco else 20.0
pts_red = 10.0 if "Presente" in soporte_red else 30.0
pts_iatrogenia = (f_eval["riesgo_desin"] * 0.20)
rci_total = float(np.clip(pts_estres + pts_fenotipo + pts_red + pts_iatrogenia, 10.0, 100.0))

# ==============================================================================
# 4. ENCABEZADO Y MÉTRICAS INSTITUCIONALES
# ==============================================================================
st.title("Atlas Neurosemiológico y Farmacológico del Clúster B")
st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -0.3rem;'><b>Modelo Dimensional Integrado (HiTOP / DSM-5 III), Conectómica Funcional y Criterio Asistencial</b> | Ateneo de Residencia</p>", unsafe_allow_html=True)

c_m1, c_m2, c_m3, c_m4 = st.columns(4)

with c_m1:
    st.metric(
        label="Freno Prefrontal Top-Down",
        value=f"{acoplamiento_frontal:.1f} %",
        delta=f"{-factor_caida*100:.1f} % por Estrés",
        delta_color="inverse",
        help="Analogía: Pastillas de freno del vehículo. Control consciente prefrontal dlPFC/vlPFC sobre el impulso motor."
    )
    st.caption("Freno voluntario sobre el impulso.")

with c_m2:
    st.metric(
        label="Reactividad Amigdalina / Insula",
        value=f"{actividad_amigdala:.1f} %",
        delta="Alarma Disparada" if actividad_amigdala > 65 else "Línea de Base",
        delta_color="inverse" if actividad_amigdala > 65 else "normal",
        help="Analogía: Sensor de humo hipersensible. Alarma de amenaza reactiva ante el dolor social o rechazo."
    )
    st.caption("Sensibilidad límbica de alarma.")

with c_m3:
    st.metric(
        label="Riesgo Desinhibición Paradójica",
        value=f"{f_eval['riesgo_desin']} %",
        delta="[Alerta] Desinhibición Motriz" if f_eval['riesgo_desin'] > 50 else "Seguro / Neutro",
        delta_color="inverse" if f_eval['riesgo_desin'] > 50 else "normal",
        help="Analogía: Cortar el cable de freno de emergencia. La benzodiacepina apaga el freno frontal consciente."
    )
    st.caption(f"Fármaco: {farmaco_1.split('(')[0]}")

with c_m4:
    color_rci = "inverse" if rci_total >= 70.0 else "normal"
    st.metric(
        label="Indice de Vulnerabilidad (RCI)",
        value=f"{rci_total:.1f} %",
        delta="Revisión de Internación" if rci_total >= 70.0 else "Manejo Ambulatorio",
        delta_color=color_rci,
        help="Analogía: Intensidad de la tormenta. Gravedad del riesgo vital conforme al Art. 20 de la Ley 26.657."
    )
    st.caption("Criterio Asistencial Ley 26.657.")

st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. MÓDULOS ACADÉMICOS DE TRABAJO
# ==============================================================================
pestana_1, pestana_2, pestana_3, pestana_4, pestana_5 = st.tabs([
    "1. Radar Dimensional (HiTOP / AMPD)",
    "2. Sala de Guardia y Dinámica Vincular (4 Fenotipos)",
    "3. Evidencia Científica y Hallazgos Neurobiológicos",
    "4. Farmacología Racional y Justificación Asistencial",
    "5. Dosier Bibliográfico y Justificación de Variables"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: RADAR DIMENSIONAL (HiTOP / AMPD)
# ------------------------------------------------------------------------------
with pestana_1:
    st.subheader("Huella Dimensional Comparativa: Deconstrucción Gráfica de los 4 Fenotipos")
    st.caption("Modelo Alternativo de la Personalidad (AMPD / HiTOP / PID-5). Fundamento: Krueger et al., 2018; Skodol et al., 2015.")
    
    col_rad_izq, col_rad_der = st.columns([1.1, 1])
    
    # Cálculo dinámico del paciente simulado
    val_af_din = float(np.clip(p_actual["Afecto Negativo"] * (1.0 + (severidad_estres / 300.0)), 0, 100))
    val_des_din = float(np.clip(p_actual["Desinhibición"] * (1.0 + (severidad_estres / 400.0)), 0, 100))
    val_ant_din = float(p_actual["Antagonismo"])
    val_desap_din = float(p_actual["Desapego"])
    val_psi_din = float(np.clip(p_actual["Psicoticismo"] + (severidad_estres * 0.25), 0, 100))
    
    valores_dinamicos = {
        "Afecto Negativo": val_af_din,
        "Desinhibición": val_des_din,
        "Antagonismo": val_ant_din,
        "Desapego": val_desap_din,
        "Psicoticismo": val_psi_din
    }
    
    with col_rad_izq:
        categorias = ["Afecto Negativo", "Desinhibición", "Antagonismo", "Desapego", "Psicoticismo"]
        fig_radar = go.Figure()
        
        for nombre, datos in perfiles_hitop.items():
            valores = [datos[c] for c in categorias]
            valores.append(valores[0])
            es_foco = (nombre == trastorno_foco)
            fig_radar.add_trace(go.Scatterpolar(
                r=valores,
                theta=categorias + [categorias[0]],
                name=nombre.split()[1],
                line=dict(
                    color=datos["color"],
                    width=3.5 if es_foco else 1.2,
                    dash="solid" if es_foco else "dot"
                ),
                fill="toself" if es_foco else "none",
                opacity=0.30 if es_foco else 0.08
            ))
            
        valores_paciente = [val_af_din, val_des_din, val_ant_din, val_desap_din, val_psi_din]
        valores_paciente.append(valores_paciente[0])
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_paciente,
            theta=categorias + [categorias[0]],
            name="Paciente Simulado (Estrés)",
            line=dict(color="#38BDF8", width=2.5, dash="dash"),
            fill="none"
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(255, 255, 255, 0.08)",
                    linecolor="rgba(255, 255, 255, 0.08)",
                    tickfont=dict(color="#64748B", size=9, family="Inter")
                ),
                angularaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.08)",
                    linecolor="rgba(255, 255, 255, 0.08)",
                    tickfont=dict(color="#F1F5F9", size=11, family="Inter")
                ),
                bgcolor="rgba(10, 15, 29, 0.8)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.28,
                xanchor="center",
                x=0.5,
                font=dict(family="Inter", size=11, color="#94A3B8")
            ),
            margin=dict(l=35, r=35, t=15, b=50),
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True, key="fig_radar_hitop")
        
    with col_rad_der:
        st.markdown(f"#### Perfil Clínico: **{trastorno_foco}**")
        st.markdown(f"**Lectura Semiológica Clásica:** {p_actual['semiologia_clasica']}")
        st.markdown(f"**Analogía del Radar:** {p_actual['analogia_radar']}")
        st.markdown("**Dominios Dimensionales en Tiempo Real (Basal / Bajo Estrés Actual):**")
        for c in categorias:
            val_basal = p_actual[c]
            val_reactivo = valores_dinamicos[c]
            delta_val = val_reactivo - val_basal
            texto_delta = f" (+{delta_val:.1f} por estrés)" if delta_val > 0.1 else ""
            st.write(f"- **{c}:** {val_reactivo:.1f}/100 <span style='color:#F87171; font-size:0.85rem;'>{texto_delta}</span>", unsafe_allow_html=True)
            st.progress(val_reactivo / 100.0)
            
        st.info(
            "**Diferenciación Conceptual Directa:**\n\n"
            "* **TLP:** Ocupa el cuadrante superior (*Afecto Negativo* alto + *Desinhibición* alta): actúa impulsivamente para apagar el dolor interno.\n"
            "* **TNP:** Ocupa casi exclusivamente el cuadrante de *Antagonismo*: preserva el control ejecutivo prefrontal para sostener su imagen de poder.\n"
            "* **TASP:** Combina *Antagonismo* con *Desinhibición*, pero con bajo *Afecto Negativo*: transgrede con frialdad afectiva instrumental.\n"
            "* **THP:** Muestra muy bajo *Desapego* y alto *Afecto Negativo*: necesita desesperadamente la mirada externa pero sin quiebre psicótico."
        )

# ------------------------------------------------------------------------------
# PESTAÑA 2: SALA DE GUARDIA Y DINÁMICA VINCULAR
# ------------------------------------------------------------------------------
with pestana_2:
    st.subheader("La Escena Clínica: 4 Respuestas Fenomenológicas ante el Mismo Hecho")
    st.markdown(f"**Situación Desencadenante:** '{estresor_tipo}' | **Carga Afectiva Percibida:** `{severidad_estres}/100`")
    
    c_tlp, c_tnp, c_tasp, c_thp = st.columns(4)
    card_style = "background: #0D1424; border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 14px 16px; margin-bottom: 12px; height: 100%;"
    
    with c_tlp:
        st.markdown(f"<div style='{card_style}'><h4 style='color:#F87171; margin-top:0;'>Trastorno Límite</h4>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Vivencia Subjetiva:</b></p>"
                    f"<p style='color:#E2E8F0; font-size:0.88rem; font-style:italic;'>«{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['vivencia_subjetiva']}»</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Mecanismo Defensivo:</b></p>"
                    f"<p style='color:#CBD5E1; font-size:0.88rem;'>{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['mecanismo_defensa']}</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Conducta Manifiesta:</b></p>"
                    f"<p style='color:#FCA5A5; font-size:0.88rem;'>Amenaza de autolesión o corte superficial como intento de regulación homeostática.</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Impacto en el Médico:</b></p>"
                    f"<p style='color:#FCD34D; font-size:0.88rem;'>{perfiles_hitop['Trastorno Límite de la Personalidad (TLP)']['impacto_equipo']}</p></div>",
                    unsafe_allow_html=True)
    with c_tnp:
        st.markdown(f"<div style='{card_style}'><h4 style='color:#FBBF24; margin-top:0;'>Trastorno Narcisista</h4>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Vivencia Subjetiva:</b></p>"
                    f"<p style='color:#E2E8F0; font-size:0.88rem; font-style:italic;'>«{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['vivencia_subjetiva']}»</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Mecanismo Defensivo:</b></p>"
                    f"<p style='color:#CBD5E1; font-size:0.88rem;'>{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['mecanismo_defensa']}</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Conducta Manifiesta:</b></p>"
                    f"<p style='color:#FDE68A; font-size:0.88rem;'>Cuestionamiento de la jerarquía médica, descalificación del criterio y quejas formales.</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Impacto en el Médico:</b></p>"
                    f"<p style='color:#FCD34D; font-size:0.88rem;'>{perfiles_hitop['Trastorno Narcisista de la Personalidad (TNP)']['impacto_equipo']}</p></div>",
                    unsafe_allow_html=True)
    with c_tasp:
        st.markdown(f"<div style='{card_style}'><h4 style='color:#A78BFA; margin-top:0;'>Trastorno Antisocial</h4>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Vivencia Subjetiva:</b></p>"
                    f"<p style='color:#E2E8F0; font-size:0.88rem; font-style:italic;'>«{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['vivencia_subjetiva']}»</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Mecanismo Defensivo:</b></p>"
                    f"<p style='color:#CBD5E1; font-size:0.88rem;'>{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['mecanismo_defensa']}</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Conducta Manifiesta:</b></p>"
                    f"<p style='color:#DDD6FE; font-size:0.88rem;'>Presión coercitiva para obtener psicofármacos; desafío directo a las normas de guardia.</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Impacto en el Médico:</b></p>"
                    f"<p style='color:#FCD34D; font-size:0.88rem;'>{perfiles_hitop['Trastorno Antisocial de la Personalidad (TASP)']['impacto_equipo']}</p></div>",
                    unsafe_allow_html=True)
    with c_thp:
        st.markdown(f"<div style='{card_style}'><h4 style='color:#22D3EE; margin-top:0;'>Trastorno Histriónico</h4>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Vivencia Subjetiva:</b></p>"
                    f"<p style='color:#E2E8F0; font-size:0.88rem; font-style:italic;'>«{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['vivencia_subjetiva']}»</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Mecanismo Defensivo:</b></p>"
                    f"<p style='color:#CBD5E1; font-size:0.88rem;'>{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['mecanismo_defensa']}</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Conducta Manifiesta:</b></p>"
                    f"<p style='color:#A5F3FC; font-size:0.88rem;'>Dramatización somática aparatosa, desmayo psicógeno o crisis de hiperventilación reactiva.</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Pauta de Descarte Sobrio:</b></p>"
                    f"<p style='color:#38BDF8; font-size:0.85rem;'>Examen neurológico dirigido rápido sin cascadas de estudios invasivos que cristalicen el rol de enfermo.</p>"
                    f"<p style='color:#94A3B8; font-size:0.85rem; margin-bottom:4px;'><b>Impacto en el Médico:</b></p>"
                    f"<p style='color:#FCD34D; font-size:0.88rem;'>{perfiles_hitop['Trastorno Histriónico de la Personalidad (THP)']['impacto_equipo']}</p></div>",
                    unsafe_allow_html=True)

    st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 1.2rem 0;'></div>", unsafe_allow_html=True)
    st.markdown("#### Pautas de Contención Verbal y Encuadre Asistencial (DBT / MBT)")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.error(
            "**Intervención Desaconsejada (Escala el Conflicto):**\n\n"
            "*Confrontación lógica directa o desacreditación:* «Tranquilícese, que lo suyo no es una urgencia real» "
            "o «No me hable en ese tono o llamo a seguridad». En el paciente con TLP confirma la vivencia de rechazo y acelera el paso al acto; "
            "en el paciente narcisista intensifica la furia por herida a su estatus."
        )
    with col_d2:
        st.success(
            "**Intervención Recomendada por la Evidencia (Desactiva la Reactividad):**\n\n"
            "*Validación afectiva firme con sostenimiento del encuadre:* «Comprendo que esta situación le genera una angustia y un malestar muy intensos, "
            "pero internarlo/a en una sala cerrada sería perjudicial para su evolución. Vamos a conversar sobre cómo organizar el acompañamiento de manera ambulatoria». "
            "Esta intervención calma la hiperactividad de la amígdala al otorgar reconocimiento emocional sin perder el encuadre asistencial."
        )

# ------------------------------------------------------------------------------
# PESTAÑA 3: EVIDENCIA CIENTÍFICA Y PARADOJAS NEUROBIOLÓGICAS
# ------------------------------------------------------------------------------
with pestana_3:
    st.subheader("Fundamentos Científicos y Hallazgos Contraintuitivos")
    st.caption("Evidencia de neuroimagen y epidemiología clínica que desafía los preconceptos tradicionales sobre el Clúster B:")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("#### 1. La Paradoja de la Detección Emocional (Fertuck et al., Biol Psychiatry, 2009)")
        st.markdown(
            "* **Concepto Erróneo Común:** Se suele asumir que el paciente límite carece de empatía y actúa de forma puramente calculadora.\n"
            "* **Evidencia Empírica:** En pruebas estandarizadas de lectura de miradas (*Reading the Mind in the Eyes Test*), los pacientes con TLP "
            "identifican microexpresiones faciales de malestar o tristeza con **mayor rapidez y agudeza que los sujetos sanos de control**.\n"
            "* **El Problema Real:** Tienen una **hiperempatía afectiva primaria inmediata**, pero una marcada falla en la corteza prefrontal medial "
            "para la atribución cognitiva. Detectan el cansancio o la seriedad en el rostro del médico, pero lo decodifican de forma errónea como desprecio u hostilidad inminente hacia ellos."
        )
        st.markdown("#### 2. La Paradoja de la Oxitocina en Apego Desorganizado (Bartz et al., SCAN, 2011)")
        st.markdown(
            "* **Concepto Erróneo Común:** La oxitocina se considera universalmente la hormona que promueve la confianza y la calma social.\n"
            "* **Evidencia Empírica:** En sujetos sanos fomenta la cooperación; sin embargo, en personas con TLP y antecedentes de trauma vincular temprano, "
            "la administración de oxitocina produce el efecto inverso: **disminuye la confianza y despierta suspicacia paranoide**.\n"
            "* **Analogía Biológica:** Para un sistema nervioso moldeado por abusos o negligencia temprana, la cercanía afectiva se procesa fisiológicamente "
            "como una señal de riesgo inminente de invasión o daño."
        )
    with col_e2:
        st.markdown("#### 3. Evolución Natural y Remisión (Estudio MSBPD de Zanarini et al. a 24 años)")
        st.markdown(
            "* **Concepto Erróneo Común:** El trastorno límite se describe habitualmente como un cuadro refractario e invariable a lo largo de toda la vida.\n"
            "* **Evidencia Empírica:** Constituye uno de los trastornos con **mayor tasa de remisión sintomática espontánea con el paso de los años**. "
            "A los 10 años de evolución, **más del 85% de los pacientes dejan de reunir los criterios formales del DSM**.\n"
            "* **Implicancia Asistencial:** La impulsividad motriz y las conductas autolesivas van disminuyendo de forma natural con la maduración biológica. "
            "El desafío terapéutico a largo plazo se centra en la reintegración social, laboral y vincular."
        )
        st.markdown("#### 4. Integridad del Fascículo Uncinado (Meta-análisis DTI - Ruocco et al., 2016)")
        st.markdown(
            "Los estudios de resonancia magnética con tensor de difusión (DTI) revelan una **disminución objetiva en la anisotropía fraccional (FA < 0.38)** "
            "del fascículo uncinado, el haz de sustancia blanca que comunica la corteza orbitofrontal con la amígdala.\n\n"
            "* **Analogía:** Representa una vía de comunicación con ancho de banda reducido. La dificultad para frenar el impulso responde a una "
            "limitación microestructural del cableado cerebral frente a sobrecargas afectivas agudas."
        )

# ------------------------------------------------------------------------------
# PESTAÑA 4: FARMACOLOGÍA RACIONAL Y JUSTIFICACIÓN ASISTENCIAL
# ------------------------------------------------------------------------------
with pestana_4:
    st.subheader("Psicofarmacología de Circuitos y Resguardo Asistencial")
    st.caption("Uso racional de psicofármacos según síntomas-blanco y fundamentación clínica de las decisiones de guardia:")
    
    col_far_l, col_far_r = st.columns([1, 1])
    with col_far_l:
        st.markdown(f"#### Perfil Farmacodinámico: `{farmaco_1}`")
        st.write(f"**Clasificación:** {f_eval['tipo']}")
        d2_val = f_eval['d2']
        ht2a_val = f_eval['5ht2a']
        gaba_val = f_eval['gaba']
        nav_val = f_eval['nav']
        
        st.markdown("**Ocupación Estimada de Sitios de Acción:**")
        st.write(f"- Receptores Dopaminérgicos D2: {d2_val}%")
        st.progress(d2_val / 100.0)
        st.write(f"- Receptores Serotoninérgicos 5-HT2A: {ht2a_val}%")
        st.progress(ht2a_val / 100.0)
        st.write(f"- Modulación Alostérica del Complejo GABAA: {gaba_val}%")
        st.progress(gaba_val / 100.0)
        st.write(f"- Bloqueo de Canales de Sodio Nav: {nav_val}%")
        st.progress(nav_val / 100.0)
        
        if f_eval["riesgo_desin"] > 50:
            st.error(
                f"**ALERTA DE DESINHIBICIÓN PARADÓJICA (Probabilidad estimada: {f_eval['riesgo_desin']}%):**\n\n"
                "Las benzodiacepinas de alta potencia inhiben la actividad de las interneuronas en la corteza orbitofrontal. "
                "En pacientes con control prefrontal basal disminuido, esto puede desconectar el freno consciente restante, "
                "incrementando la agresividad verbal o facilitando el paso al acto impulsivo. Las guías internacionales (NICE CG78) "
                "desaconsejan su uso rutinario en situaciones de crisis de personalidad."
            )
        elif f_eval["riesgo_acatisia"] > 50:
            st.error(
                f"**ALERTA DE INQUIETUD MOTORA Y ACATISIA (Probabilidad estimada: {f_eval['riesgo_acatisia']}%):**\n\n"
                "Un bloqueo dopaminérgico agudo elevado (> 80% en vía nigroestriatal) puede desencadenar acatisia severa. "
                "En la práctica de guardia suele confundirse erróneamente con mayor agitación psicomotriz del paciente, "
                "induciendo el error de prescribir dosis adicionales del antipsicótico."
            )
        elif "Lamotrigina" in farmaco_1:
            st.warning(
                "**PRECISIÓN CLÍNICA SOBRE LAMOTRIGINA:**\n\n"
                "Este fármaco **nunca se inicia en agudo durante una urgencia** debido a que requiere un protocolo estricto "
                "de titulación ascendente lenta a lo largo de varias semanas para prevenir el síndrome de Stevens-Johnson. "
                "En esta simulación se evalúa exclusivamente como **estabilizador de base preexistente**, modulando el tono glutamatérgico y los canales de sodio."
            )
        else:
            st.success(
                "**PERFIL TERAPÉUTICO ACOTADO:** La intervención se orienta a modular un síntoma específico (como la desorganización aguda o el insomnio pertinaz) "
                "sin anular los mecanismos de autorregulación del paciente ni generar dependencia biológica rápida."
            )
            
    with col_far_r:
        st.markdown("#### Registro Asistencial y Criterios Conforme a la Ley 26.657")
        st.caption("Pautas descriptivas para asentar en la Historia Clínica protegiendo el criterio del equipo médico:")
        
        criterio_internacion = rci_total >= 70.0
        criterio_texto = (
            "Se evalúa que la confluencia de factores de riesgo agudo requiere un período breve de observación y compensación clínica en Hospital General, bajo consentimiento o según criterios del Art. 20, con revisión inmediata una vez estabilizado el cuadro vital."
            if criterio_internacion else
            "NO se configuran criterios de riesgo cierto e inminente de gravedad extrema en los términos del Art. 20. La conducta se inscribe en un patrón crónico de desregulación emocional. La internación en institución monovalente o asilar se considera formalmente contraindicada, debido al riesgo documentado de inducir regresión institucional, pérdida de autonomía y escalada en conductas de autoagresión. Procede el sostenimiento del encuadre ambulatorio."
        )
        
        minuta_asistencial = f"""REGISTRO ASISTENCIAL DE INTERVENCIÓN EN GUARDIA
Contexto: Evaluación psiquiátrica de urgencia
Motivo de Consulta: Crisis de desregulación afectiva reactiva ({trastorno_foco})

1. EXAMEN DEL SENSORIO Y ORIENTACIÓN TEMPOROESPACIAL:
Al momento de la entrevista, el/la paciente se encuentra vigil, lúcido/a y orientado/a en tiempo y espacio.
No se observan signos de obnubilación ni desestructuración de la conciencia.
No se evidencian fenómenos sensoperceptivos alucinatorios ni ideación delirante primaria estructurada.
El cuadro conductual se asocia a un pico de desregulación emocional reactivo frente a estresor vincular.

2. EVALUACIÓN ASISTENCIAL SEGÚN LEY NACIONAL DE SALUD MENTAL N° 26.657:
Índice de Vulnerabilidad Aguda: {rci_total:.1f}%.
Criterio Clínico Interdisciplinario:
{criterio_texto}

3. PLAN DE CUIDADO Y CONTINUIDAD:
- Estrategia Farmacológica: {farmaco_1} (indicación sintomática acotada con retiro programado).
- Abordaje Central: Indicación de tratamiento psicoterapéutico manualizado basado en la evidencia (DBT / MBT).
Se entrevista a los referentes afectivos presentes, acordando pautas claras de acompañamiento y corresponsabilidad."""

        st.text_area("Modelo de Nota Evolutiva para Historia Clínica:", value=minuta_asistencial, height=340)

# ------------------------------------------------------------------------------
# PESTAÑA 5: DOSIER BIBLIOGRÁFICO Y JUSTIFICACIÓN DE VARIABLES
# ------------------------------------------------------------------------------
with pestana_5:
    st.subheader("Dosier Bibliográfico y Justificación Epistemológica del Modelo")
    st.caption("Respaldo científico que sustenta la elección de cada variable y ecuación operativa en la aplicación:")
    
    col_bib_1, col_bib_2 = st.columns(2)
    with col_bib_1:
        st.markdown("#### ¿Por qué estas variables y no otras?")
        st.markdown(
            "1. **Freno Prefrontal Top-Down (dlPFC/vlPFC):**\n"
            "* *Justificación:* Los modelos categoriales clásicos atribuyen la impulsividad a un 'defecto del carácter'. "
            "Los estudios de neuroimagen funcional demuestran que existe una hipoactivación objetiva de la corteza prefrontal dorsolateral "
            "ante estímulos afectivos negativos. Es la variable indispensable para cuantificar la capacidad de autorregulación biológica.\n"
            "* *Fuente:* **Ruocco et al., Biol Psychiatry (2016)**; **Blair, Neuropsychopharmacology (2013)**.\n\n"
            "2. **Reactividad Amigdalina / Insula Anterior:**\n"
            "* *Justificación:* Modela la magnitud de la alarma emocional ante claves sociales. Se utiliza en lugar de la 'ansiedad' "
            "porque el Clúster B no cursa con preocupación cognitiva difusa, sino con pánico somático ante el rechazo.\n"
            "* *Fuente:* **Schulze et al., Am J Psychiatry (2016)**; **Fertuck et al., Biol Psychiatry (2009)**.\n\n"
            "3. **Estresor Interpersonal de Apego como Variable Dinámica:**\n"
            "* *Justificación:* En reposo, los circuitos frontales del paciente operan con indemnidad. La desconexión es estado-dependiente: "
            "solo se manifiesta cuando el sistema vincular percibe amenaza o invalidación.\n"
            "* *Fuente:* **Bateman & Fonagy, Am J Psychiatry (2008)**; **Bartz et al., SCAN (2011)**."
        )
    with col_bib_2:
        st.markdown("#### Bibliografía Principal de Referencia (Nivel 1a / Guías)")
        st.markdown(
            "* **Modelo Dimensional HiTOP y DSM-5 Sección III:**\n"
            "  * Krueger RF, et al. *The Hierarchical Taxonomy of Psychopathology (HiTOP): A dimensional alternative to traditional nosologies.* World Psychiatry, 2018.\n"
            "  * Skodol AE, et al. *The Alternative DSM-5 Model for Personality Disorders.* Lancet Psychiatry, 2015.\n\n"
            "* **Neurobiología y Conectómica Funcional:**\n"
            "  * Fertuck EA, et al. *Enhanced 'reading the mind in the eyes' in borderline personality disorder.* Biol Psychiatry, 2009.\n"
            "  * Bartz J, et al. *Oxytocin can hinder trust and cooperation in borderline personality disorder.* Social Cognitive and Affective Neuroscience, 2011.\n"
            "  * Ruocco AC, Carcone D. *A neurobiological model of affective instability in borderline personality disorder.* Biol Psychiatry, 2016.\n\n"
            "* **Evolución Longitudinal y Psicoterapia:**\n"
            "  * Zanarini MC, et al. *A 24-year follow-up study of the course of borderline personality disorder.* Am J Psychiatry, 2016.\n"
            "  * Storebø OJ, et al. *Psychological therapies for people with borderline personality disorder.* Cochrane Database of Systematic Reviews, 2020.\n\n"
            "* **Psicofarmacología y Toxicología Clínica:**\n"
            "  * Stahl SM. *Stahl's Essential Psychopharmacology: Neuroscientific Basis and Practical Applications.* 5th ed. Cambridge University Press, 2021.\n"
            "  * National Institute for Health and Care Excellence (NICE). *Borderline personality disorder: recognition and management (CG78).* London, 2009 (actualizado)."
        )
