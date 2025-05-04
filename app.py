import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from utils.document_validator import validate_document, process_image_ocr
from utils.social_media import extract_social_media_info, analyze_social_relevance
from utils.data_visualization import create_interest_chart, create_activity_timeline

# Configuração da página
st.set_page_config(
    page_title="Conheça Seu Fã - Esports",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa as variáveis do estado da sessão se elas não existirem
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'personal': {},
        'interests': {},
        'documents': {},
        'social_media': {},
        'esports_profiles': {}
    }
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Funções para navegar entre as etapas
def next_step():
    if st.session_state.step < 5:
        st.session_state.step += 1
        st.session_state.progress = (st.session_state.step - 1) * 25

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.session_state.progress = (st.session_state.step - 1) * 25

def save_form_data(form_data, category):
    st.session_state.user_data[category].update(form_data)

# Cabeçalho
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.svg", width=80)
with col2:
    st.title("Conheça Seu Fã - Esports")
    st.subheader("Crie seu perfil de fã para desbloquear experiências exclusivas")

# Barra de progresso
st.progress(st.session_state.progress)

# Indicadores de etapa
steps_col1, steps_col2, steps_col3, steps_col4, steps_col5 = st.columns(5)
with steps_col1:
    st.markdown(f"**{'1. Dados Pessoais' if st.session_state.step != 1 else '→ 1. Dados Pessoais'}**")
with steps_col2:
    st.markdown(f"**{'2. Interesses' if st.session_state.step != 2 else '→ 2. Interesses'}**")
with steps_col3:
    st.markdown(f"**{'3. Verificação' if st.session_state.step != 3 else '→ 3. Verificação'}**")
with steps_col4:
    st.markdown(f"**{'4. Redes Sociais' if st.session_state.step != 4 else '→ 4. Redes Sociais'}**")
with steps_col5:
    st.markdown(f"**{'5. Painel' if st.session_state.step != 5 else '→ 5. Painel'}**")

# Etapa 1: Informações Pessoais
if st.session_state.step == 1:
    st.header("Informações Pessoais")
    
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome Completo", value=st.session_state.user_data['personal'].get('name', ''))
            email = st.text_input("Email", value=st.session_state.user_data['personal'].get('email', ''))
            cpf = st.text_input("CPF", value=st.session_state.user_data['personal'].get('cpf', ''))
            phone = st.text_input("Telefone", value=st.session_state.user_data['personal'].get('phone', ''))
        
        with col2:
            address = st.text_input("Endereço", value=st.session_state.user_data['personal'].get('address', ''))
            city = st.text_input("Cidade", value=st.session_state.user_data['personal'].get('city', ''))
            state = st.text_input("Estado", value=st.session_state.user_data['personal'].get('state', ''))
            birth_date = st.date_input("Data de Nascimento", value=datetime.strptime(st.session_state.user_data['personal'].get('birth_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d') if 'birth_date' in st.session_state.user_data['personal'] else None)
        
        submitted = st.form_submit_button("Salvar e Continuar")
        
        if submitted:
            form_data = {
                'name': name,
                'email': email,
                'cpf': cpf,
                'phone': phone,
                'address': address,
                'city': city,
                'state': state,
                'birth_date': birth_date.strftime('%Y-%m-%d') if birth_date else None
            }
            
            # Validar campos obrigatórios
            required_fields = ['name', 'email', 'cpf']
            empty_fields = [field for field in required_fields if not form_data.get(field)]
            
            if empty_fields:
                st.error(f"Por favor, preencha os seguintes campos obrigatórios: {', '.join(empty_fields)}")
            else:
                save_form_data(form_data, 'personal')
                next_step()

# Etapa 2: Interesses e Atividades
elif st.session_state.step == 2:
    st.header("Interesses e Atividades de Esports")
    
    with st.form("interests_form"):
        # Jogos favoritos
        st.subheader("Jogos Favoritos")
        games_options = ["League of Legends", "Counter-Strike", "Valorant", "Dota 2", "Overwatch", "Fortnite", "Rainbow Six Siege", "Rocket League", "Outro"]
        favorite_games = st.multiselect("Selecione seus jogos favoritos", games_options, default=st.session_state.user_data['interests'].get('favorite_games', []))
        
        # Inicialize other_games para corrigir o erro de "possibly unbound"
        other_games = ""
        if "Outro" in favorite_games:
            other_games = st.text_input("Especifique outros jogos", value=st.session_state.user_data['interests'].get('other_games', ''))
        
        # Times favoritos
        st.subheader("Times Favoritos")
        teams_options = ["FURIA", "LOUD", "Team Liquid", "paiN Gaming", "Cloud9", "Fnatic", "G2 Esports", "T1", "FaZe Clan", "Outro"]
        favorite_teams = st.multiselect("Selecione seus times favoritos", teams_options, default=st.session_state.user_data['interests'].get('favorite_teams', []))
        
        # Inicialize other_teams para corrigir o erro de "possibly unbound"
        other_teams = ""
        if "Outro" in favorite_teams:
            other_teams = st.text_input("Especifique outros times", value=st.session_state.user_data['interests'].get('other_teams', ''))
        
        # Eventos frequentados
        st.subheader("Eventos Frequentados no Último Ano")
        attended_events = st.text_area("Liste os eventos que você frequentou (um por linha)", value=st.session_state.user_data['interests'].get('attended_events', ''))
        
        # Hábitos de jogo
        st.subheader("Hábitos de Jogo")
        hours_gaming = st.slider("Horas jogando por semana", 0, 50, st.session_state.user_data['interests'].get('hours_gaming', 10))
        hours_watching = st.slider("Horas assistindo esports por semana", 0, 30, st.session_state.user_data['interests'].get('hours_watching', 5))
        
        # Compras de produtos
        st.subheader("Compras de Produtos")
        merch_options = ["Camisetas de Times", "Acessórios de Times", "Equipamentos de Gaming", "Colecionáveis", "Nenhum"]
        merchandise = st.multiselect("Produtos comprados no último ano", merch_options, default=st.session_state.user_data['interests'].get('merchandise', []))
        
        submitted = st.form_submit_button("Salvar e Continuar")
        
        if submitted:
            form_data = {
                'favorite_games': favorite_games,
                'favorite_teams': favorite_teams,
                'attended_events': attended_events,
                'hours_gaming': hours_gaming,
                'hours_watching': hours_watching,
                'merchandise': merchandise
            }
            
            if "Outro" in favorite_games:
                form_data['other_games'] = other_games
            if "Outro" in favorite_teams:
                form_data['other_teams'] = other_teams
            
            save_form_data(form_data, 'interests')
            next_step()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar"):
            prev_step()

# Etapa 3: Verificação de Documentos
elif st.session_state.step == 3:
    st.header("Verificação de Documentos")
    
    # Use colunas para melhor layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Por favor, carregue seus documentos de identificação para verificação.")
        
        # Upload de Documento de Identidade
        st.subheader("Documento de Identidade")
        id_doc = st.file_uploader("Carregue seu documento de identidade (frente)", type=["jpg", "jpeg", "png"])
        
        if id_doc:
            # Exibir o documento carregado
            st.image(id_doc, caption="Documento Carregado", width=300)
            
            # Processar e validar documento usando OCR
            if st.button("Validar Documento"):
                with st.spinner("Processando documento..."):
                    # Processar o documento usando OCR
                    extracted_text = process_image_ocr(id_doc)
                    
                    # Validar as informações extraídas
                    is_valid, validation_message = validate_document(extracted_text, st.session_state.user_data['personal'])
                    
                    if is_valid:
                        st.success(validation_message)
                        st.session_state.user_data['documents']['id_validated'] = True
                        st.session_state.user_data['documents']['id_validation_message'] = validation_message
                    else:
                        st.error(validation_message)
                        st.session_state.user_data['documents']['id_validated'] = False
                        st.session_state.user_data['documents']['id_validation_message'] = validation_message
        
        # Documento secundário (opcional)
        st.subheader("Documento Secundário (Opcional)")
        secondary_doc = st.file_uploader("Carregue outro documento para verificação adicional", type=["jpg", "jpeg", "png"])
        
        if secondary_doc:
            st.image(secondary_doc, caption="Documento Secundário Carregado", width=300)

    with col2:
        st.subheader("Status de Verificação")
        
        # Exibir status de verificação
        if st.session_state.user_data['documents'].get('id_validated'):
            st.success("Documento Verificado ✓")
        else:
            st.warning("Documento Ainda Não Verificado")
        
        # Informações sobre o processo de verificação
        st.info("""
        ## Processo de Verificação de Documentos
        
        1. Carregue uma imagem clara do seu documento
        2. Nossa IA processará o documento
        3. As informações serão verificadas com seu perfil
        4. Você receberá um status de verificação
        
        Documentos válidos incluem:
        - Carteira de Identidade (RG)
        - Carteira Nacional de Habilitação (CNH)
        - Passaporte
        """)
    
    # Botões de navegação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar"):
            prev_step()
    
    with col2:
        # Só permitir avançar se o documento for validado ou o usuário quiser pular
        if st.session_state.user_data['documents'].get('id_validated') or st.button("Pular Verificação"):
            next_step()

# Etapa 4: Integração com Redes Sociais
elif st.session_state.step == 4:
    st.header("Redes Sociais e Perfis de Esports")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        with st.form("social_media_form"):
            st.subheader("Conecte Suas Redes Sociais")
            
            # Twitter/X
            twitter_username = st.text_input("Usuário do Twitter/X", value=st.session_state.user_data['social_media'].get('twitter_username', ''))
            
            # Instagram
            instagram_username = st.text_input("Usuário do Instagram", value=st.session_state.user_data['social_media'].get('instagram_username', ''))
            
            # Facebook
            facebook_profile = st.text_input("URL do Perfil do Facebook", value=st.session_state.user_data['social_media'].get('facebook_profile', ''))
            
            # Discord
            discord_username = st.text_input("Usuário do Discord", value=st.session_state.user_data['social_media'].get('discord_username', ''))
            
            st.subheader("Perfis em Plataformas de Esports")
            
            # Twitch
            twitch_username = st.text_input("Usuário da Twitch", value=st.session_state.user_data['esports_profiles'].get('twitch_username', ''))
            
            # Steam
            steam_profile = st.text_input("URL do Perfil Steam", value=st.session_state.user_data['esports_profiles'].get('steam_profile', ''))
            
            # Outras plataformas de jogos
            other_platforms = st.text_area("Outras Plataformas de Jogos (Plataforma: Usuário)", value=st.session_state.user_data['esports_profiles'].get('other_platforms', ''))
            
            submitted = st.form_submit_button("Conectar e Analisar")
            
            if submitted:
                social_media_data = {
                    'twitter_username': twitter_username,
                    'instagram_username': instagram_username,
                    'facebook_profile': facebook_profile,
                    'discord_username': discord_username
                }
                
                esports_profiles_data = {
                    'twitch_username': twitch_username,
                    'steam_profile': steam_profile,
                    'other_platforms': other_platforms
                }
                
                # Verificar se pelo menos um perfil de rede social foi fornecido
                if any(social_media_data.values()):
                    save_form_data(social_media_data, 'social_media')
                    
                    # Simular análise de redes sociais
                    with st.spinner("Analisando perfis de redes sociais..."):
                        social_media_info = extract_social_media_info(social_media_data)
                        st.session_state.user_data['social_media']['analysis'] = social_media_info
                        st.success("Perfis de redes sociais analisados com sucesso!")
                else:
                    st.warning("Por favor, forneça pelo menos um perfil de rede social.")
                
                # Verificar se pelo menos um perfil de esports foi fornecido
                if any(esports_profiles_data.values()):
                    save_form_data(esports_profiles_data, 'esports_profiles')
                    
                    # Simular análise de perfil de esports
                    with st.spinner("Analisando perfis de esports..."):
                        esports_relevance = analyze_social_relevance(esports_profiles_data, st.session_state.user_data['interests'])
                        st.session_state.user_data['esports_profiles']['relevance'] = esports_relevance
                        st.success("Perfis de esports analisados com sucesso!")
                else:
                    st.warning("Por favor, forneça pelo menos um perfil de esports.")
    
    with col2:
        st.subheader("Por que Conectar Redes Sociais?")
        st.info("""
        ## Benefícios de Conectar
        
        1. **Experiências Personalizadas**: Receba conteúdo personalizado com base em seus interesses em esports.
        
        2. **Acesso à Comunidade**: Junte-se a comunidades exclusivas de fãs dos seus times favoritos.
        
        3. **Ofertas Especiais**: Receba ofertas direcionadas para eventos e produtos.
        
        4. **Validação de Perfil**: Verifique seu status como um entusiasta genuíno de esports.
        
        Seus dados são protegidos e usados apenas para melhorar sua experiência como fã.
        """)
        
        # Exibir uma imagem de amostra de fãs de esports
        st.image("https://images.unsplash.com/photo-1513151233558-d860c5398176", caption="Fãs de esports celebrando em um evento", use_column_width=True)
    
    # Resultados da análise de redes sociais (se disponível)
    if 'analysis' in st.session_state.user_data['social_media']:
        st.subheader("Resultados da Análise de Redes Sociais")
        
        analysis = st.session_state.user_data['social_media']['analysis']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Posts Relacionados a Esports", analysis.get('esports_posts', 'N/A'))
        with col2:
            st.metric("Menções a Times", analysis.get('team_mentions', 'N/A'))
        with col3:
            st.metric("Pontuação de Engajamento", analysis.get('engagement_score', 'N/A'))
    
    # Relevância do perfil de esports (se disponível)
    if 'relevance' in st.session_state.user_data['esports_profiles']:
        st.subheader("Relevância do Perfil de Esports")
        
        relevance = st.session_state.user_data['esports_profiles']['relevance']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pontuação de Relevância", f"{relevance.get('relevance_score', 0)}/10")
        with col2:
            st.metric("Nível de Confiança", relevance.get('confidence', 'Médio'))
    
    # Botões de navegação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar"):
            prev_step()
    
    with col2:
        if st.button("Ver Painel"):
            next_step()

# Etapa 5: Painel
elif st.session_state.step == 5:
    st.header("Seu Painel de Perfil de Fã")
    
    # Verificar se temos dados do usuário para exibir
    if st.session_state.user_data['personal'].get('name'):
        st.subheader(f"Bem-vindo, {st.session_state.user_data['personal']['name']}!")
        
        # Resumo do perfil
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Exibir uma imagem de configuração de jogo como foto de perfil
            st.image("https://images.unsplash.com/photo-1598550457678-aa60413d7c80", use_column_width=True)
            
            # Exibir status de verificação
            if st.session_state.user_data['documents'].get('id_validated'):
                st.success("✓ Fã Verificado")
            else:
                st.warning("⚠ Fã Não Verificado")
            
            # Informações básicas
            st.markdown("### Informações Básicas")
            if 'personal' in st.session_state.user_data:
                personal = st.session_state.user_data['personal']
                st.markdown(f"**Email:** {personal.get('email', 'Não fornecido')}")
                st.markdown(f"**Localização:** {personal.get('city', '')} {', ' + personal.get('state', '') if personal.get('state') else ''}")
        
        with col2:
            # Visualização de interesses do fã
            st.markdown("### Seus Interesses em Esports")
            
            if 'interests' in st.session_state.user_data and st.session_state.user_data['interests']:
                # Criar gráfico de interesses
                fig = create_interest_chart(st.session_state.user_data['interests'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado de interesse disponível. Complete a etapa 2 para ver a visualização de seus interesses.")
        
        # Insights de redes sociais
        st.markdown("### Insights de Redes Sociais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'analysis' in st.session_state.user_data['social_media']:
                # Criar linha do tempo de atividade
                fig = create_activity_timeline(st.session_state.user_data['social_media']['analysis'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado de redes sociais disponível. Conecte suas contas para ver insights.")
        
        with col2:
            # Contas conectadas
            st.markdown("### Contas Conectadas")
            
            social_media = st.session_state.user_data['social_media']
            esports_profiles = st.session_state.user_data['esports_profiles']
            
            if any(social_media.get(platform) for platform in ['twitter_username', 'instagram_username', 'facebook_profile', 'discord_username']):
                for platform, username in social_media.items():
                    if platform in ['twitter_username', 'instagram_username', 'facebook_profile', 'discord_username'] and username:
                        st.markdown(f"- **{platform.replace('_username', '').replace('_profile', '').title()}**: {username}")
            else:
                st.info("Nenhuma conta de rede social conectada.")
            
            st.markdown("### Plataformas de Esports")
            
            if any(esports_profiles.get(platform) for platform in ['twitch_username', 'steam_profile']):
                for platform, username in esports_profiles.items():
                    if platform in ['twitch_username', 'steam_profile'] and username:
                        st.markdown(f"- **{platform.replace('_username', '').replace('_profile', '').title()}**: {username}")
            else:
                st.info("Nenhuma conta de plataforma de esports conectada.")
        
        # Recomendações baseadas no perfil
        st.markdown("### Recomendações Personalizadas")
        
        recommendations_col1, recommendations_col2, recommendations_col3 = st.columns(3)
        
        with recommendations_col1:
            st.markdown("#### Próximos Eventos")
            st.markdown("- FURIA vs. Liquid - 15 de Junho")
            st.markdown("- ESL Pro League Temporada 18 - Julho 2023")
            st.markdown("- GamesCon Brasil - Setembro 2023")
        
        with recommendations_col2:
            st.markdown("#### Produtos")
            st.markdown("- Camiseta de Edição Limitada do Time")
            st.markdown("- Pacote de Periféricos de Gaming")
            st.markdown("- Itens Colecionáveis do Campeonato")
        
        with recommendations_col3:
            st.markdown("#### Comunidade")
            st.markdown("- Entre no Discord Oficial")
            st.markdown("- Siga as Redes Sociais do Time")
            st.markdown("- Participe de Concursos para Fãs")
        
        # Galeria de imagens de fãs
        st.markdown("### Comunidade de Fãs de Esports")
        
        gallery_col1, gallery_col2, gallery_col3, gallery_col4 = st.columns(4)
        
        with gallery_col1:
            st.image("https://images.unsplash.com/photo-1527529482837-4698179dc6ce", use_column_width=True)
        
        with gallery_col2:
            st.image("https://images.unsplash.com/photo-1593305841991-05c297ba4575", use_column_width=True)
        
        with gallery_col3:
            st.image("https://images.unsplash.com/photo-1516880711640-ef7db81be3e1", use_column_width=True)
        
        with gallery_col4:
            st.image("https://images.unsplash.com/photo-1467810563316-b5476525c0f9", use_column_width=True)
        
        # Opção de exportar dados
        st.markdown("### Gerenciamento de Dados")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("Exportar Dados do Perfil"):
                # Converter os dados para JSON
                profile_json = json.dumps(st.session_state.user_data, indent=4)
                
                # Criar um botão de download
                st.download_button(
                    label="Baixar JSON",
                    data=profile_json,
                    file_name="perfil_fa_esports.json",
                    mime="application/json"
                )
        
        with export_col2:
            if st.button("Recomeçar"):
                # Resetar o estado da sessão
                st.session_state.user_data = {
                    'personal': {},
                    'interests': {},
                    'documents': {},
                    'social_media': {},
                    'esports_profiles': {}
                }
                st.session_state.step = 1
                st.session_state.progress = 0
                st.rerun()
    else:
        st.warning("Nenhum dado de perfil disponível. Por favor, complete as etapas anteriores.")
        
        if st.button("Iniciar Criação de Perfil"):
            st.session_state.step = 1
            st.rerun()

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p>Plataforma Conheça Seu Fã &copy; 2023 - Conectando Fãs de Esports em Todo o Mundo</p>
    <p>Política de Privacidade | Termos de Serviço | Proteção de Dados</p>
</div>
""", unsafe_allow_html=True)
