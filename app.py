import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Document Search Engine",
    page_icon="🔍",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .score-badge {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔍 Semantic Document Search Engine</div>', unsafe_allow_html=True)
st.markdown("### Multi-Document Embedding Search with Caching")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    top_k = st.slider("Number of results", min_value=1, max_value=20, value=5)
    
    st.markdown("---")
    st.header("📊 Statistics")
    
    # Fetch stats
    try:
        stats_response = requests.get(f"{API_URL}/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
            st.metric("Total Documents", stats['total_documents'])
            st.metric("Index Size", stats['index_size'])
            st.metric("Embedding Dimension", stats['embedding_dimension'])
            
            st.markdown("#### Cache Performance")
            cache_stats = stats['cache_stats']
            st.metric("Cached Embeddings", cache_stats['cached_embeddings'])
            st.metric("Cache Hit Rate", f"{cache_stats['hit_rate_percent']}%")
            st.metric("Cache Hits", cache_stats['cache_hits'])
            st.metric("Cache Misses", cache_stats['cache_misses'])
    except:
        st.warning("API not connected")
    
    st.markdown("---")
    st.markdown("#### About")
    st.info("This search engine uses sentence-transformers and FAISS for semantic search with intelligent caching.")

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input("🔎 Enter your search query:", placeholder="e.g., quantum physics basics")

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    search_button = st.button("Search", type="primary", use_container_width=True)

# Search functionality
if search_button and query:
    with st.spinner("Searching..."):
        try:
            # Make API request
            response = requests.post(
                f"{API_URL}/search",
                json={"query": query, "top_k": top_k}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Display results summary
                st.success(f"Found {len(data['results'])} results in {data['processing_time_ms']:.2f}ms")
                
                # Display results
                st.markdown("### 📄 Search Results")
                
                for result in data['results']:
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <h4>#{result['rank']} {result['doc_id']} 
                            <span class="score-badge">Score: {result['score']:.3f}</span></h4>
                            <p><strong>Category:</strong> {result['category']}</p>
                            <p><strong>Preview:</strong> {result['preview']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Expandable explanation
                        with st.expander("📊 View Ranking Explanation"):
                            exp = result['explanation']
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Overlap Ratio", f"{exp['overlap_ratio']:.1%}")
                            with col2:
                                st.metric("Document Length", exp['doc_length'])
                            with col3:
                                st.metric("Embedding Score", exp['embedding_score'])
                            
                            if exp['matched_keywords']:
                                st.markdown(f"**Matched Keywords:** {', '.join(exp['matched_keywords'])}")
                            else:
                                st.info("No direct keyword matches (semantic similarity only)")
                
                # Export results
                st.markdown("---")
                if st.button("📥 Export Results as JSON"):
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(data, indent=2),
                        file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
            else:
                st.error(f"Search failed: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Make sure the FastAPI server is running:")
            st.code("uvicorn src.api:app --reload")
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif search_button:
    st.warning("Please enter a search query")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280;'>
    <p>Built with Sentence Transformers, FAISS, FastAPI, and Streamlit</p>
    <p>AI Engineer Intern Assignment - CodeAtRandom</p>
</div>
""", unsafe_allow_html=True)
