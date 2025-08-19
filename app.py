import streamlit as st
from finance_agent import get_agent

# Page configuration
st.set_page_config(
    page_title="Agno Finance Agent",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .api-key-section {
        background-color: #e8f4fd;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #1f77b4;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .response-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 20px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">📊 Agno Finance Agent</h1>', unsafe_allow_html=True)
st.markdown("### Real-time Financial Analysis with AI")
st.markdown("---")

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'api_key_valid' not in st.session_state:
    st.session_state.api_key_valid = False

# API Key Configuration Section
st.markdown('<div class="api-key-section">', unsafe_allow_html=True)
st.subheader("🔑 API Configuration")

col1, col2 = st.columns([3, 1])

with col1:
    groq_api_key = st.text_input(
        "Enter your Groq API Key:",
        type="password",
        placeholder="gsk_...",
        help="Get your free API key from https://console.groq.com/keys"
    )

with col2:
    st.markdown("**Get API Key:**")
    st.markdown("[Groq Console](https://console.groq.com/keys)")
    st.markdown("*Free tier available*")

if groq_api_key:
    try:
        # Test the API key by creating an agent
        test_agent = get_agent(groq_api_key)
        st.session_state.api_key_valid = True
        st.success("✅ API Key validated successfully!")
    except Exception as e:
        st.session_state.api_key_valid = False
        st.error(f"❌ Invalid API Key: {str(e)}")
else:
    st.session_state.api_key_valid = False
    st.markdown('<div class="warning-box">⚠️ Please enter your Groq API key to get started.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Main application (only show if API key is valid)
if st.session_state.api_key_valid and groq_api_key:
    
    # Sidebar with information
    with st.sidebar:
        st.header("📈 Features")
        st.write("• **Real-time Stock Prices** - Current market data")
        st.write("• **Market Analysis** - Comprehensive insights")
        st.write("• **Financial News** - Latest market updates")
        st.write("• **Company Research** - Detailed company info")
        
        st.header("🛠️ Tools Used")
        st.write("• YFinance - Stock market data")
        st.write("• DuckDuckGo - Financial news & info")
        st.write("• Groq LLM - AI analysis")
        
        if st.button("🗑️ Clear History"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Initialize user_question
    user_question = None
    
    # Question Selection Section
    st.subheader("💬 Ask Your Finance Question")
    
    # Create tabs for different types of questions
    tab1, tab2, tab3 = st.tabs(["📊 Stock Queries", "📈 Market Analysis", "✍️ Custom Question"])
    
    with tab1:
        stock_questions = [
            "What is the current stock price of Apple (AAPL)?",
            "What is the current stock price of Tesla (TSLA)?",
            "What is the current stock price of Microsoft (MSFT)?",
            "Compare Apple and Microsoft stock performance",
            "Show me Ford (F) stock information"
        ]
        selected_stock_question = st.selectbox("Select a stock question:", stock_questions, key="stock_tab")
        if st.button("Ask Stock Question", key="stock_btn"):
            user_question = selected_stock_question
    
    with tab2:
        market_questions = [
            "What are the latest tech stock trends?",
            "Analyze the S&P 500 index performance today",
            "What are the top performing stocks this week?",
            "Tell me about recent market volatility",
            "What's happening in the cryptocurrency market?"
        ]
        selected_market_question = st.selectbox("Select a market question:", market_questions, key="market_tab")
        if st.button("Ask Market Question", key="market_btn"):
            user_question = selected_market_question
    
    with tab3:
        custom_question = st.text_area(
            "Enter your custom finance question:",
            height=100,
            placeholder="e.g., What should I know about investing in renewable energy stocks?"
        )
        if st.button("Ask Custom Question", key="custom_btn"):
            if custom_question and custom_question.strip():
                user_question = custom_question
    
    # Quick stock lookup section
    st.markdown("### 🔍 Quick Stock Lookup")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        quick_symbol = st.text_input("Enter stock symbol:", placeholder="AAPL, TSLA, MSFT, etc.")
    
    with col2:
        if st.button("Get Price", key="quick_price"):
            if quick_symbol:
                user_question = f"What is the current stock price and key information for {quick_symbol.upper()}?"
    
    with col3:
        if st.button("Full Analysis", key="quick_analysis"):
            if quick_symbol:
                user_question = f"Provide a comprehensive analysis of {quick_symbol.upper()} including price, performance, and recent news"
    
    # Process the question if one was selected/entered
    if user_question and user_question.strip():
        with st.spinner("🤖 Agent is analyzing your question..."):
            try:
                # Get the agent and run the query
                finance_agent = get_agent(groq_api_key)
                response = finance_agent.run(user_question)
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    'question': user_question,
                    'response': response
                })
                
                # Display the response
                st.markdown("---")
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.markdown("### 🤖 Agent Response:")
                
                # Handle different response types
                if hasattr(response, 'content'):
                    st.markdown(response.content)
                elif hasattr(response, 'messages') and response.messages:
                    # Handle response with messages
                    for message in response.messages:
                        if hasattr(message, 'content') and message.content:
                            st.markdown(message.content)
                else:
                    st.markdown(str(response))
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.error("Please check your API key and try again.")

# Display conversation history
if st.session_state.conversation_history and st.session_state.api_key_valid:
    st.markdown("---")
    st.subheader("📜 Conversation History")
    
    for i, chat in enumerate(reversed(st.session_state.conversation_history)):
        with st.expander(f"💬 Q{len(st.session_state.conversation_history)-i}: {chat['question'][:60]}..."):
            st.markdown("**❓ Question:**")
            st.info(chat['question'])
            st.markdown("**🤖 Response:**")
            
            # Handle different response types in history
            if hasattr(chat['response'], 'content'):
                st.markdown(chat['response'].content)
            elif hasattr(chat['response'], 'messages') and chat['response'].messages:
                for message in chat['response'].messages:
                    if hasattr(message, 'content') and message.content:
                        st.markdown(message.content)
            else:
                st.markdown(str(chat['response']))

# Footer with instructions
if not st.session_state.api_key_valid:
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.info(
        "**To use this finance agent:**\n\n"
        "1. Get a free API key from [Groq Console](https://console.groq.com/keys)\n"
        "2. Enter your API key in the field above\n"
        "3. Start asking finance questions!\n\n"
        "**Note:** Your API key is only stored in your browser session and is never saved permanently."
    )

st.markdown("---")
st.markdown(
    "**🛠️ Built with:** [Streamlit](https://streamlit.io) • [Agno Framework](https://github.com/agno-ai/agno) • [Groq LLM](https://groq.com) • [YFinance](https://pypi.org/project/yfinance/)"
)