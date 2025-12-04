# NutrifyMe – End-to-End RAG System for Personalized Nutrition

<h3>A full-stack RAG pipeline integrating MySQL, ChromaDB, Snowflake, Airflow, S3, Databricks, and Gemini LLM for health-aware nutrition insights</h3>
<br>
<div>

<p>NutrifyMe is an end-to-end AI nutrition intelligence system designed to operate like a modern production RAG application. It brings together structured health profiles, multi-source nutrition datasets, semantic vector search, and LLM-driven reasoning to generate personalized, context-aware nutrition recommendations. The system is built as a complete engineering solution—combining data ingestion, cleaning, embedding generation, retrieval, and final LLM decision-making into one coherent pipeline.

It integrates a custom Retrieval-Augmented Generation workflow with real ETL components, including MySQL, ChromaDB, Docker, Airflow, AWS S3, Databricks Community Edition, and Snowflake. Large datasets such as NHANES, Open Food Facts, and Open Nutrition are cleaned and transformed, embedded using MiniLM-L6-v2, stored in ChromaDB, and ultimately consumed by Google Gemini 2.0 Flash for reasoning. A Streamlit interface supports both text and voice input, making the system easy and natural to use.

While pipeline components are manually triggered due to student budget constraints, every part of the architecture—from ingestion to transformation to retrieval—has been fully implemented, demonstrating how enterprise-grade AI systems can be built end-to-end even under resource limitations.</p>
<p align="center">••••••••••••</p>
</div>


<div>
  <h3>Key Features</h3>
  <ul>
  <li>End-to-end RAG system combining structured health data, enriched food datasets, semantic retrieval, and LLM reasoning.</li>
  <li>Full ETL pipeline built with Airflow, Docker, MySQL, S3, Databricks CE, and Snowflake (manually triggered due to budget constraints).</li>
  <li>Multi-source nutrition database integrating NHANES, Open Food Facts, and Open Nutrition.</li>
  <li>Semantic food retrieval using MiniLM-L6-v2 embeddings stored in ChromaDB.</li>
  <li>Personalized, health-aware recommendations powered by Google Gemini 2.0 Flash.</li>
  <li>Streamlit UI supporting both text and voice queries.</li>
  <li>Figma-designed UX covering onboarding, profile, and chat screens.</li>
  </ul>
  <p align="center">••••••••••••</p>
</div>

<div>
  <h3>System Architecture</h3>
  <p>NutrifyMe is built as two connected layers:</p>
  <ol>
    <li>A real-time RAG pipeline that handles user queries</li>
    <p><br><b>User → Streamlit UI → MySQL → ChromaDB → RAG Pipeline → Gemini → Response</b><br></p>
    <ul>
      <li>The user submits a query through text or voice.</li>
      <li>The system loads the user profile from MySQL.</li>
      <li>The query is embedded with MiniLM-L6-v2.</li>
      <li>ChromaDB performs semantic search + similarity analytics, retrieving:</li>
      <ol>
        <li>relevant foods</li>
        <li>health data</li>
        <li>user data</li>
        <li>reference data</li>
      </ol>
      <li>A structured final context is assembled (food + health + user + reference).</li>
      <li>Gemini 2.0 Flash generates a personalized, rule-based response.</li>
      <li>The result is returned to Streamlit for display.</li>
      
   </ul>
    <br>
    <li>A fully implemented ETL pipeline that prepares all nutrition and health data</li>
    <p><br><b>Raw Data → MySQL → Docker/Airflow → S3 → Databricks CE → Snowflake → VSCode → ChromaDB</b><br></p>
    <ul>
      <li>Docker hosts the Airflow environment.</li>
      <li>Airflow orchestrates extraction and upload tasks (manual trigger).</li>
      <li>MySQL (staging) stores raw extracted datasets.</li>
      <li>S3 functions as the data lake for raw + intermediate files.</li>
      <li>Databricks CE handles cleaning, merging, joins, and feature engineering.</li>
      <li>Snowflake stores cleaned & analytical tables.</li>
      <li>Data returns to VSCode for RAG model development.</li>
      <li>Embeddings are generated and saved into ChromaDB, completing the loop.</li>
   </ul>
  </ol>
</div>

