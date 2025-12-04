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
        <li>relevant foods</li>https://github.com/account/organizations/new
        <li>health data</li>
        <li>user data</li>
        <li>reference data</li>
      </ol>
      <li>A structured final context is assembled (food + health + user + reference).</li>
      <li>Gemini 2.0 Flash generates a personalized, rule-based response.</li>
      <li>The result is returned to Streamlit for display.</li>

      <img width="1536" height="1024" alt="ChatGPT Image Dec 3, 2025, 11_45_26 PM" src="https://github.com/user-attachments/assets/9922378e-8b52-4294-945e-969598cf6cb7" />

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
  <p align="center">••••••••••••</p>
</div>


<div>
  <h3>Tech Stack</h3>
  <p><b>Programming & Core Libraries</b></p>
  <ul>
  <li>Python 3.10 – Main development language</li>
  <li>NumPy – Numerical operations</li>
  <li>Pandas – Data preprocessing & cleaning</li>
  <li>json / time / tqdm – Utilities for parsing, timing, progress visualization</li>
  <li>LangChain – Prompt orchestration, RAG chain logic</li>
  <li>google-generativeai – Gemini 2.0 Flash client</li>
  <li>sentence-transformers – MiniLM-L6-v2 embeddings</li>
  </ul>
  <br>
  <p><b>Application Layer</b></p>
  <p><b>Streamlit</b> Used to build the complete user experience: onboarding, voice/text input, results display, and profile pages.</p>
  <br>
  <p><b>Databases & Storage</b></p>
  <p>MySQL</p>
  <ul>
  <li>Raw User Database</li>
  <li>Raw Food Database</li>
  <li>Raw Health Database</li>
  <li>Raw Reference Database</li>
  </ul>
    
  <p>ChromaDB</p>
  <ul>
  <li>MiniLM L6-v2 embeddings</li>
  <li>Semantic search vectors</li>
  <li>Food + nutrition + health chunks + user profile</li>
  </ul>

  <p>AWS</p>
  <ul>
  <li>Acts as the student-budget data lake for staging raw/intermediate files.</li>
  </ul>

  <p><b>Data Transformation</b></p>
  <p>Docker</p>
  <ul>
  <li>Hosts the full Airflow environment in containers.</li>
  </ul>

  <p>Airflow Manual, DAG-based orchestration for:</p>
  <ul>
  <li>Extract → Stage → Load</li>
  <li>Moving data between MySQL → S3</li>
  </ul>

  <p>Databricks - Cleaning, Merging, Feature Engineering, Rebuliding Tables</p>

  <p>Snowflake - Final warehouse storing production-ready cleaned data for RAG consumption</p>
  
  <p><b>Machine Learning & LLM </b></p>
  <p>MiniLM-L6-v2 (Sentence Transformers) - Generates embeddings for semantic retrieval.</p>
  <p>Google Gemini 2.0 Flash - Deep Reasoning, Precision Based Filering, Safety-first food recommendation logic, User-condition-specific personalization</p>

  <p><b>Development & Workflow Tools</b></p>
  <p>VS Code - Development, debugging, RAG module building.</p>
  <p>Docker Desktop - Environment runner for Airflow container setup.</p>
  <p>Git / GitHub - Version control and project management.</p>
  <p>Figma - High-fidelity UI prototypes and user flow design.</p>
  <p align="center">••••••••••••</p>
</div>


<div>
<h3>How The System Works?</h3>
<p>NutrifyMe combines a data-rich ETL pipeline, a vector-based retrieval layer, and LLM-driven personalized reasoning.
The system operates in two modes: </p>
  <ol>
  <li>Online Mode (RAG Workflow) → answering user questions with precision</li>
  <p>Step 1 — User Interacts Through Streamlit. The user asks a question through:
  Text input, or Voice input (converted to text) <br>
  <i>Example: “I’m pre-diabetic and want a snack. Is guacamole okay for me?”</i></p>
  <p>Step 2 — Load User Profile from MySQL : Age, height, weight, BMI Conditions (e.g., diabetes, thyroid, BP), Medications, Any metabolic flags. This gives the system context about who is asking.</p>
  <p> Step 3 — Embedding Generation (MiniLM-L6-v2). The user query is embedded using MiniLM-L6-v2. This converts the text into a numeric vector representing:
    Intent, Food terms, Health-specific semantics</p>  
  <p>Step 4 — Vector Retrieval from ChromaDB. ChromaDB searches thousands of embedded chunks: Food names + alt names, Allergens, Nutrient lists, Serving sizes, NHANES biomarker, reference info, Health-condition rules</p>
  <p>Step 5 — Structured Context Builder. Your custom module combines:<br>
    Food Data (serving size, allergens, nutrient 100g values, ingredient analysis)<br>
    User Data (profile, conditions, medications)<br>
    Reference Health Data (NHANES reference ranges, safe/unsafe biomarkers)<br>
    Logic Constraints (allergen filters, risky ingredients, high-sodium alerts, etc.)<br>
    This creates the final context block sent to Gemini.</p>
    <p>Step 6 — Gemini 2.0 Flash Reasoning. The Gemini prompt receives: Cleaned structured context, User biological/medical profile, Food metadata, Safety rules, Required output format (short, clear, actionable). <br> 
    Gemini performs: Multi-step reasoning, Risk assessment, Personalization, Safety-based filtration, Step-by-step justification</p>
    <p>Step 7 — Final Answer Returned to Streamlit, User sees: Personalized recommendation, Why it is safe/unsafe, What to avoid, Better alternatives, Portion guidance</p> <br>

  <li>Offline Mode (ETL + Data Preparation) → preparing high-quality structured data </li>
  <p>Step 1 — Raw Data Extraction, Sources: NHANES (health + biomarker + demographic data), Open Food Facts (food metadata + ingredients + allergens + nutrition), Open Nutrition Data (nutrients 100g). All pulled from MySQL (staging layer).</p>
  <p>Step 2 — Docker + Airflow (Orchestration). You manually trigger DAGs (student budget), but architecture is production-ready. Airflow moves data between: <br>MySQL → S3</p>
  <p>Step 3 — S3 as Raw + Semi-Processed Data Lake, S3 stores: Cleaned/intermediate CSV</p>
  <p>Step 4 — Databricks CE (Cleaning + Feature Engineering). Even without paid clusters, you manually run transformations:<br>
  Merging NHANES + nutrition datasets, Removing corrupted values, Standardizing units, Calculation of normalized nutrition fields, Deriving features for ML/RAG
  <br>Outputs → Uploaded to Snowflake</p>
  <p>Step 5 — Snowflake as Final Analytical Warehouse, Snowflake holds fully cleaned, merged, RAG-ready tables: Foods (standardized), Nutrients (100g normalized), Allergen tables, Ingredient analysis tables, NHANES reference ranges. This is the source of truth for your retrieval layer</p>
  <p>Step 6 — VS Code (RAG Model Development). From VS Code you:<br>
  Pull Snowflake tables, Build chunking logic, Generate embeddings, Insert vectors into ChromaDB, Test prompt logic, Run RAG end-to-end</p>
  <p>Step 7 — ChromaDB as Local Vector Store: All food vectors, Health-condition vectors, Reference-range vectors, Merged context vectors</p>

  <p><b>Final Response Generation</b></p>
  <ul>
    <li>A personalized food recommendation</li>
    <li>Why it is OK or not OK</li>
    <li>What ingredients pose risk</li>
    <li>Safer alternatives</li>
    <li>Portion suggestions</li>
    <li>Evidence-based reasoning from NHANES + nutrient tables</li>
  </ul>
  </ol>
</div>


<div>

  
</div>


</div>
