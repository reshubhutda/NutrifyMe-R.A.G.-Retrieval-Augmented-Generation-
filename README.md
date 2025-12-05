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

![image]("Rag%20pipeline.jpg")

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
  <p align="center">••••••••••••</p>
</div>


<div>
<h3>Data Sources & Overview</h3>
<p>NutrifyMe integrates four major datasets through the ETL pipeline before converting them into RAG-ready vector embeddings. Each dataset contributes different layers of nutritional, biological, and health-risk intelligence.</p>
<p><b>Open Nutrition Dataset</b></p>
<ul>
  <li>Name</li>
  <li>Alternate Names</li>
  <li>Description</li>
  <li>Serving</li>
  <li>Nutrition_100gm</li>
  <li>Labels</li>
  <li>Package Size</li>
  <li>Ingredients</li>
  <li>Ingredient Analysis</li>
</ul>
<p><b>Open Food Facts Dataset</b></p>
<ul>
  <li>Product Name</li>
  <li>Generic Name</li>
  <li>Quantity</li>
  <li>Categories EN</li>
  <li>Labels EN</li>
  <li>Ingredients Text</li>
  <li>Allergens EN</li>
  <li>Traces EN</li>
  <li>Serving Size</li>
  <li>Additives EN</li>
  <li>Nutrtion 100gm</li>
</ul>
<p><b>NHANES Health Dataset</b></p>
<ul>
  <li>USER_ID</li>
  <li>GENDER</li>
  <li>Age</li>
  <li>Race</li>
  <li>Birth Country</li>
  <li>Marital Status</li>
  <li>WEIGHT_KG</li>
  <li>HEIGHT_CM</li>
  <li>BMI</li>
  <li>BMI Category</li>
  <li>WBC_COUNT</li>
  <li>LYMPHOCYTE_PCT</li>
  <li>MONOCYTE_PCT</li>
  <li>NEUTROPHIL_PCT</li>
  <li>EOSINOPHIL_PCT</li> 
  <li>BASOPHIL_PCT</li> 
  <li>LYMPHOCYTE_NUM</li>
  <li>RBC_COUNT</li>
  <li>HEMOGLOBIN</li>
  <li>HEMATOCRIT</li>
  <li>PLATELET_COUNT</li>
  <li>HDL Cholesterol (mg/dL)</li>
  <li>TRIGLYCERIDES_MG_DL_X</li> 
  <li>LDL Cholesterol (mg/dL)</li>
  <li>Total Cholesterol (mg/dL)</li>
  <li>TRIGLYCERIDES_MG_DL_Y</li>
  <li>HBA1C_PERCENT</li>
  <li>Fasting Glucose (mg/dL)</li> 
  <li>HS_CRP_MG_L</li>
  <li>ALT</li>
  <li>ALP</li>
  <li>AST</li> 
  <li>GGT</li>
  <li>Albumin</li>
  <li>Total Protein</li>
  <li>Creatinine</li>
  <li>BUN</li> 
  <li>Albumin_Creatinine_Ratio_MG_G</li>
  <li>Total Bilirubin</li>
  <li>Sodium</li>
  <li>Potassium</li>
  <li>Chloride</li>
  <li>Magnesium</li>
  <li>Phosphorus</li>
  <li>Calcium</li>
  <li>Bicarbonate</li>
  <li>Osmolality</li>
  <li>Iron</li>
  <li>LDH</li>
  <li>CK</li> 
  <li>Vitamin D</li>
</ul>  
<p><b>Reference Range Dataset (NHANES Normal Ranges)</b></p>
<ul>
  <li>Test</li>
  <li>Adult Range</li>
  <li>Units</li>
  <li>Chld Range</li>
  <li>Adult Min</li>
  <li>Adult Max</li>
  <li>Child Min</li>
  <li>Child Max</li>
</ul>
<p align="center">••••••••••••</p>
</div>

<h3>Project Directory Structure</h3>

```markdown
project-root/
│── .venv/
│── airflow/
│   ├── dags/
│   ├── logs/
│   ├── plugins/
│   └── docker-compose.yml
│
│── chroma_data/
│   ├── chroma.sqlite3
│   ├── b5c719bb-...
│   ├── b9f6e813-...
│   └── e5959423-...
│
│── data/
│   ├── Processed_Health.csv
│   ├── Processed_Nutrition.csv
│   ├── Processed_Reference_Range.csv
│   ├── health_embeddings.npy
│   ├── health_row_ids.npy
│   ├── nutrition_embeddings.npy
│   ├── nutrition_row_ids.npy
│   ├── reference_embeddings.npy
│   └── reference_row_ids.npy
│
│── notebook/
│   ├── app.py
│   ├── build_all.py
│   ├── build_health_db.py
│   ├── build_nutrition_db.py
│   ├── build_profile_db.py
│   ├── build_reference_db.py
│   ├── context_builder.py
│   ├── health_embed_utils.py
│   ├── nutrition_embed_utils.py
│   ├── nutrition_retriever.py
│   ├── profile_matcher_file.py
│   ├── query_health.py
│   ├── query_nutrition.py
│   ├── query_reference.py
│   ├── reference_embed_utils.py
│   ├── reference_loader.py
│   ├── run_embeddings.py
│   ├── Snowflake_Connector.py
│   ├── store_embed_csv.py
│   ├── user_db.py
│   └── user_query.py
│
│── sql/
│   └── RawData.sql
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── uv.lock

```

<p align="center">••••••••••••</p>

