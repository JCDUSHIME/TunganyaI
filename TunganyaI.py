import streamlit as st
import decimal
from datetime import date
import pandas as pd # For dashboard table demo

# --- Configuration ---
st.set_page_config(
    page_title="SME TaxEase Rwanda - Full Prototype",
    page_icon="🇷🇼",
    layout="wide", # Use 'wide' layout for more space
    initial_sidebar_state="expanded"
)

# Custom CSS for "Duck Egg" background and responsiveness
st.markdown(
    """
    <style>
    /* Background color for the main content area */
    .stApp {
        background-color: #EEF5EB; /* A light, soft green resembling Duck Egg */
    }

    /* Adjust padding for responsiveness */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Center align the title and main headers */
    h1, h2, h3 {
        text-align: center;
        color: #2F4F4F; /* Dark Slate Gray for text for contrast */
    }

    /* Enhance buttons */
    div.stButton > button:first-child {
        background-color: #4CAF50; /* Green */
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        cursor: pointer;
        transition-duration: 0.4s;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049;
        box-shadow: 0 6px 12px 0 rgba(0,0,0,0.24);
    }

    /* Sidebar styling */
    .css-1d391kg { /* Target sidebar background */
        background-color: #D9EDD2; /* Slightly darker duck egg for sidebar */
        border-right: 1px solid #C0D3C0;
    }
    .css-pkajk0 { /* Sidebar content padding */
        padding-top: 2rem;
    }

    /* Make selectboxes and input fields slightly larger and rounded */
    .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input, .stDateInput > div > div > input, .stTextArea > div > textarea {
        border-radius: 8px;
        border: 1px solid #B0C4DE; /* LightSteelBlue */
        padding: 8px 10px;
    }

    /* Info/Warning/Success boxes styling */
    .stAlert {
        border-radius: 10px;
        padding: 1rem;
    }

    /* Adjust column spacing for responsiveness */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        .stColumn {
            width: 100% !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Use Decimal for financial calculations to avoid floating-point inaccuracies
D = decimal.Decimal
decimal.getcontext().prec = 10

# --- Translation Dictionary ---
# All user-facing strings are stored here, by language code.
# In a real app, this would be loaded from external JSON/YAML files or a database.
# Note: Kinyarwanda translations are AI-generated for demonstration and should be
# verified by native speakers for accuracy and naturalness.
TRANSLATIONS = {
    'en': {
        "app_title": "SME TaxEase Rwanda - Prototype",
        "welcome_page_title": "Welcome to SME TaxEase Rwanda Prototype",
        "welcome_page_desc": "This prototype showcases the key functionalities of the SME TaxEase Rwanda application, designed to simplify tax compliance for small and medium enterprises (SMEs) and reduce the need for tax experts. Our goal is to provide **all key information** you need to manage your taxes independently. Use the navigation bar on the left to explore different modules.",
        "modules_included": "Modules included in this prototype:",
        "module_welcome": "Welcome", # Added for navigation formatting
        "module_onboarding": "Onboarding & Profile",
        "module_calculator": "Tax Calculator",
        "module_dashboard": "Smart Dashboard",
        "module_guides": "Educational Guides",
        "module_reporting": "Declaration & Reporting",
        "welcome_disclaimer": "**Disclaimer:** This is a conceptual prototype. All calculations and data presented are simplified for demonstration purposes and **do not represent actual tax advice**. Always consult official RRA guidelines or a qualified tax expert for precise tax compliance.",
        "welcome_start_info": "Start by navigating to 'Onboarding & Profile' to set up your business and discover your tax journey!",
        "sidebar_nav_title": "SME TaxEase Navigation",
        "go_to": "Go to",
        "about_app_title": "About SME TaxEase",
        "about_app_desc": "This prototype aims to show how SME TaxEase Rwanda will:\n- **Simplify Tax Compliance:** By breaking down complex tax concepts into easy steps.\n- **Reduce Costs:** Minimizing reliance on external tax professionals by empowering you with knowledge.\n- **Increase Compliance:** By providing clear tools and information for accurate and timely filings.",
        "developed_by": "Developed with ❤️ for Rwandan SMEs.",
        "copyright": "SME TaxEase Rwanda © 2025",
        "onboarding_desc_short": "Set up your business profile and understand your tax obligations.",
        "calculator_desc_short": "Estimate your tax liabilities based on your financial inputs.",
        "dashboard_desc_short": "View a summary of your tax status, upcoming deadlines, and past submissions.",
        "guides_desc_short": "Access simplified explanations of Rwandan tax obligations and filing steps.",
        "reporting_desc_short": "Generate pre-filled tax reports and understand submission procedures.",


        # Onboarding & Profile
        "onboarding_title": "👤 Onboarding & Business Profile Setup",
        "onboarding_desc": "Complete your business profile to help us identify your specific tax obligations in Rwanda. This step is designed to mimic the questions a tax expert would ask to understand your tax categories.",
        "section_business_info": "1. Business Basic Information",
        "label_business_name": "Official Business Name",
        "label_rra_tin": "RRA TIN (Taxpayer Identification Number)",
        "help_rra_tin": "If you are a formal business, provide your RRA TIN.",
        "label_business_entity_type": "Type of Business Entity",
        "options_business_entity_type": ["Sole Proprietor", "Partnership", "Company (Ltd)", "Cooperative", "Informal Business / Micro-Enterprise", "Other"],
        "help_business_entity_type": "Your legal business structure impacts your tax obligations.",
        "label_sector": "Primary Business Sector",
        "options_sector": ["Retail", "Services", "Agriculture", "Manufacturing", "ICT", "Tourism", "Consulting", "Other"],
        "help_sector": "Some sectors may have specific tax treatments or incentives.",
        "label_registration_date": "Business Registration Date (if formal)",
        "section_key_tax_questions": "2. Key Tax-Related Questions",
        "label_estimated_annual_turnover": "Estimated Annual Turnover (RWF)",
        "help_estimated_annual_turnover": "Your estimated total sales/revenue for a full year. This helps determine VAT and Turnover Tax applicability.",
        "label_has_employees": "Do you have employees (paid salaries)?",
        "help_has_employees": "This determines if you need to pay PAYE and RSSB.",
        "label_is_vat_registered_onboard": "Are you currently VAT registered?",
        "help_is_vat_registered_onboard": "If your turnover is above RWF 20M annually or RWF 5M quarterly, you likely need to be VAT registered.",
        "info_informal_business": "As an informal business, understanding formalization steps is key to simplifying taxes. We'll guide you!",
        "section_contact_info": "3. Contact Information",
        "label_contact_person": "Main Contact Person",
        "label_phone_number": "Phone Number",
        "label_email_address": "Email Address",
        "label_address": "Business Address",
        "button_save_profile": "Save Profile and Determine Tax Obligations",
        "success_profile_saved": "Business Profile for '{business_name}' saved successfully!",
        "header_estimated_obligations": "Your Estimated Tax Obligations:",
        "info_preliminary_assessment": "Based on your profile, here are the taxes you **might** be obligated to comply with in Rwanda. This is a preliminary assessment; detailed calculations will be in the Tax Calculator.",
        "no_paye_rssb_info": "*(No PAYE/RSSB expected as you indicated no employees)*",
        "what_s_next": "What's Next?",
        "next_calc_guide": "1. **Go to the `Tax Calculator`**: Use your actual sales, expenses, and salaries to get precise estimates.",
        "next_explore_guides": "2. **Explore `Educational Guides`**: Learn more about each of your identified tax obligations in plain language.",
        "next_formalization": "3. **Consider Formalization (for informal businesses)**: Our guides can help you understand the benefits and steps.",
        "data_stored_info": "In a real application, this data would be stored in your backend database.",

        # Tax Calculator
        "calculator_title": "📊 User-Friendly Tax Calculator",
        "calculator_desc": "Input your actual financial data for a specific period to get an estimated tax liability. This aims to provide the key calculations a tax expert would perform.",
        "section_business_period": "1. Business & Reporting Period",
        "label_business_type_calc": "Type of Business",
        "help_business_type_calc": "Select if your business is formally registered or operates informally. This affects tax applicability.",
        "label_is_vat_registered_calc": "Is your business VAT registered?",
        "help_is_vat_registered_calc": "Check if your business is registered for Value Added Tax (VAT).",
        "label_has_employees_calc": "Do you have employees?",
        "help_has_employees_calc": "This influences PAYE and RSSB calculations.",
        "label_num_employees": "Number of Employees",
        "label_is_small_business_for_turnover_tax": "Is your business eligible for Turnover Tax (usually for small businesses not VAT registered)?",
        "help_is_small_business_for_turnover_tax": "This typically applies to small businesses below the VAT threshold. If VAT registered, Corporate Tax applies.",
        "header_reporting_period": "Reporting Period",
        "label_start_date": "Start Date",
        "label_end_date": "End Date",
        "section_financial_inputs": "2. Financial Inputs (All figures in RWF)",
        "label_turnover": "Total Business Turnover/Sales for Period",
        "help_turnover": "Total revenue generated from your sales of goods/services.",
        "label_vat_eligible_sales": "VAT Eligible Sales",
        "help_vat_eligible_sales": "The portion of your turnover that is subject to VAT.",
        "label_total_expenses": "Total Deductible Expenses for Period",
        "help_total_expenses": "All allowable business expenses that reduce your taxable income.",
        "label_salaries_paid_gross": "Total Gross Salaries Paid (for all employees for the period)",
        "help_salaries_paid_gross": "Sum of all gross salaries paid to your employees during this period.",
        "label_other_taxable_income": "Other Taxable Income (e.g., from investments)",
        "help_other_taxable_income": "Any other income subject to corporate tax that is not from core sales.",
        "label_depreciation_on_assets": "Depreciation on Assets (if applicable)",
        "help_depreciation_on_assets": "Deductible wear and tear on your business assets. Consult RRA for specific rates.",
        "button_calculate_taxes": "Calculate Estimated Taxes",
        "section_estimated_results": "3. Estimated Tax Results",
        "total_tax_due": "Total Estimated Tax Due:",
        "info_estimated_figures": "These are estimated figures based on your inputs and **simplified RRA rules** used in this prototype.",
        "view_detailed_breakdown": "View Detailed Breakdown",
        "breakdown_by_tax_type": "#### Breakdown by Tax Type:",
        "paye_amount": "PAYE (Pay As You Earn):",
        "vat_amount": "VAT (Value Added Tax):",
        "turnover_tax_amount": "Turnover Tax:",
        "corporate_tax_amount": "Corporate Tax:",
        "rssb_total_contribution": "RSSB Contributions (Total):",
        "rssb_employee_share": "Employee Share:",
        "rssb_employer_share": "Employer Share:",
        "calc_notes": "Notes: Calculations are based on highly simplified prototyping rules. Real RRA rules are significantly more complex and must be consulted. This tool is for estimation only.",
        "section_required_documents": "4. What Documents Do You Need to Prepare?",
        "documents_desc": "Based on the taxes calculated, you typically need the following documents for official RRA submission:",
        "doc_all_taxes": "* **For all taxes:** Financial records (Income & Expense Ledger), Bank Statements.",
        "doc_vat": "* **VAT:** Sales Invoices, Purchase Invoices, Input VAT credit notes, Output VAT debit notes.",
        "doc_paye_rssb": "* **PAYE & RSSB:** Payroll Register, Employee Contracts, Proof of RSSB contributions.",
        "doc_corporate_tax": "* **Corporate Tax:** Audited Financial Statements (for larger businesses), Income Statement, Balance Sheet, Expense Receipts.",
        "doc_turnover_tax": "* **Turnover Tax:** Records of Sales/Turnover.",
        "action_keep_records": "**Action:** Keep clear and organized records throughout the tax period.",
        "quick_links_info": "#### Quick Links for More Info:",

        # Smart Dashboard
        "dashboard_title": "📈 Smart Dashboard",
        "dashboard_desc": "Get a quick overview of your tax status, past filings, and upcoming deadlines. This aims to provide the key oversight a tax expert would give you.",
        "overview_obligations": "Overview of Current Obligations",
        "metric_upcoming_deadline": "Upcoming Deadline",
        "metric_last_filed_tax": "Last Filed Tax",
        "metric_compliance_score": "Overall Compliance Status (Dummy)",
        "header_compliance_calendar": "Your Tax Compliance Calendar",
        "info_deadlines": "**Key Deadlines in Rwanda (General Examples - always verify official RRA dates):**\n* **15th of each month:** PAYE & RSSB contributions for previous month.\n* **15th of each month:** VAT declaration & payment for previous month (if applicable).\n* **20th of the month following the quarter:** Turnover Tax declaration & payment (if applicable).\n* **March 31st (following year):** Annual Corporate Income Tax declaration.",
        "header_recent_declarations": "Recent Tax Declarations & Payments",
        "col_tax_type": "Tax Type", "col_period": "Period", "col_amount_due": "Amount Due (RWF)", "col_status": "Status", "col_filing_date": "Filing Date", "col_receipt": "Receipt", "col_amount_paid": "Amount Paid (RWF)",
        "header_alerts_reminders": "Actionable Alerts & Reminders",
        "alert_vat_due": "⚠️ **Action Required:** Your VAT declaration for Q2 2025 is due by July 20, 2025. Please complete the Tax Calculator and prepare your report.",
        "info_rssb_remitted": "✅ All employees' RSSB contributions for June have been remitted. Good job!",
        "alert_corporate_tax_upcoming": "🔔 **Upcoming:** Corporate Income Tax for 2025 will be due by March 31, 2026. Start gathering annual financial records.",
        "status_filed": 'Filed', "status_pending": 'Pending', "receipt_view": 'View', "receipt_na": 'N/A', "status_submitted_paid": 'Submitted & Paid', "receipt_download": 'Download',

        # Educational Guides
        "guides_title": "📚 Educational Guides: Simplify Tax Knowledge",
        "guides_desc": "Access simplified, plain-language explanations of Rwandan tax obligations and step-by-step filing instructions. Our goal is to make tax information so clear, you won't need a tax expert to understand your obligations.",
        "header_explore_guides": "Explore Key Rwandan Tax Types:",
        "guide_select_placeholder": "Select a Tax Topic",
        "info_guide_coming_soon": "Content for this guide is coming soon! Please select another guide.",
        "link_rra_website": "For official RRA guidelines, please visit the [Rwanda Revenue Authority website](https://www.rra.gov.rw).",
        "guide_vat_title": "Understanding VAT in Rwanda",
        "guide_vat_content": """
            #### What is VAT?
            Value Added Tax (VAT) is a consumption tax charged on taxable goods and services supplied in Rwanda and on taxable imports. It's an **indirect tax**, meaning businesses collect it from consumers on behalf of the Rwanda Revenue Authority (RRA).

            #### Who needs to register for VAT?
            Businesses whose **annual taxable turnover** (total sales of goods/services subject to VAT) exceeds **RWF 20,000,000** or **RWF 5,000,000** in a calendar quarter are generally required to register for VAT. You can also apply for voluntary registration if your turnover is lower but you deal with VAT-registered clients.

            #### How is VAT Calculated?
            VAT is calculated at **18%** of the value of taxable supplies.
            * **Output VAT:** VAT collected on your sales.
            * **Input VAT:** VAT paid on your business purchases.
            You remit the difference (Output VAT - Input VAT) to RRA. If Input VAT is higher, you might get a refund or carry forward the credit.

            #### Filing & Payment:
            VAT declarations and payments are typically done **monthly**, by the 15th day of the following month.

            *This is a simplified overview. Always consult RRA for comprehensive details and current legal texts.*
        """,
        "guide_paye_title": "How to Calculate PAYE",
        "guide_paye_content": """
            #### PAYE (Pay As You Earn)
            PAYE is **income tax deducted from employee salaries** by their employers. As an employer, you are responsible for calculating, deducting, and remitting PAYE to the RRA on a monthly basis.

            #### Simplified PAYE Bands (for illustrative purposes - consult RRA for current official rates):
            | Monthly Gross Salary (RWF) | Tax Rate |
            | :-------------------------- | :------- |
            | Up to 30,000                | 0%       |
            | 30,001 - 100,000            | 20%      |
            | 100,001 - 200,000           | 30%      |
            | Above 200,000               | 40%      |

            #### Employer's Role & Deadline:
            Employers must maintain proper records of employee salaries and PAYE deductions. The deducted PAYE must be declared and remitted to RRA by the **15th day of the following month**.

            *This is a simplified overview. Consult RRA for comprehensive details and current rates. The actual calculation often involves careful consideration of allowances and benefits.*
        """,
        "guide_turnover_tax_title": "SME Turnover Tax Explained",
        "guide_turnover_tax_content": """
            #### Turnover Tax (for Small Businesses)
            Turnover Tax is a simplified tax regime for **small businesses** that are generally **not VAT registered**. It's based on your gross annual turnover (sales).

            #### Who is eligible?
            Typically, businesses with an annual turnover below the VAT threshold (e.g., RWF 20,000,000) but above a certain lower threshold might be subject to Turnover Tax. This replaces Corporate Income Tax for these smaller entities.

            #### How is it Calculated?
            It's usually a **fixed percentage of your gross turnover**. In our prototype, we use a simplified 3% for demonstration. The actual rate and thresholds are defined by RRA.

            #### Filing & Payment:
            Turnover Tax is often declared and paid **quarterly**, by the 20th day of the month following the end of the quarter.

            *This is a simplified overview. Always verify the current thresholds and rates with RRA.*
        """,
        "guide_corporate_tax_title": "Corporate Tax Basics for Beginners",
        "guide_corporate_tax_content": """
            #### Corporate Income Tax (CIT)
            Corporate Tax is levied on the **taxable profits** (income minus deductible expenses) of formally registered companies and other legal entities.

            #### How is it Calculated?
            The standard Corporate Income Tax rate in Rwanda is **30%** of taxable profit.
            Taxable profit is generally calculated as: **Gross Income - Allowable Deductions**.
            Allowable deductions include business expenses, depreciation on assets, etc. Non-deductible expenses (e.g., penalties) cannot reduce your taxable income.

            #### Filing & Payment:
            CIT is typically declared and paid **annually**, by March 31st of the following year. Advance payments might be required quarterly.

            *This is a simplified overview. Corporate tax involves complex rules regarding deductions, capital allowances, losses, and specific incentives. Consulting RRA guidelines or a tax expert is highly recommended.*
        """,
        "guide_rssb_title": "Rwanda Social Security Board (RSSB) Contributions",
        "guide_rssb_content": """
            #### RSSB Contributions
            The Rwanda Social Security Board (RSSB) manages social security schemes in Rwanda, including pension and occupational hazards. Employers and employees both contribute to this fund.

            #### Contribution Rates (Simplified for Prototype):
            * **Employee Contribution:** 5% of gross salary.
            * **Employer Contribution:** 3% of gross salary.
            These contributions are typically subject to a **maximum contributory salary** (e.g., RWF 1,000,000 per month in our prototype).

            #### Employer's Responsibility:
            Employers are responsible for deducting the employee's share, adding the employer's share, and remitting the total amount to RSSB (often along with PAYE) by the **15th day of the following month**.

            *This is a simplified overview. Always refer to official RSSB guidelines for detailed information and current rates/caps.*
        """,
        "guide_registration_title": "Registering Your Business with RRA",
        "guide_registration_content": """
            #### Formalizing Your Business
            Registering your business with the Rwanda Development Board (RDB) and the Rwanda Revenue Authority (RRA) is the first step towards formal tax compliance.

            #### Key Benefits of Formalization:
            * Access to financing and government support.
            * Ability to tender for larger contracts.
            * Increased trust and credibility with customers and suppliers.
            * Protection under commercial laws.

            #### Basic Steps for Formalization:
            1.  **Business Name Reservation & Registration:** Usually done online via RDB portal.
            2.  **RRA Taxpayer Identification Number (TIN):** Obtained automatically during RDB registration or applied for separately.
            3.  **Specific Tax Registration:** Based on your business activity and turnover, you may need to register for VAT, PAYE, etc.
            4.  **Licensing:** Obtain necessary operational licenses from local government or regulatory bodies.

            *The process can vary based on your business type. RDB and RRA websites provide detailed guides.*
        """,

        # Declaration & Reporting
        "reporting_title": "📑 Declaration & Reporting: Your Filing Assistant",
        "reporting_desc": "This module is designed to simplify your tax declaration process, aiming to provide all the information and steps you need without an expert. It will allow you to generate pre-filled tax declaration forms and reports, and eventually facilitate direct submission to RRA (subject to API integration).",
        "section_generate_report": "1. Generate a New Report/Declaration",
        "info_auto_populate": "Imagine this section auto-populating based on your saved financial records and previous calculations from the 'Tax Calculator'.",
        "label_report_type": "Select Report Type",
        "options_report_type": ["VAT Declaration Form", "PAYE Declaration Form", "Annual Corporate Tax Report", "Turnover Tax Declaration", "RSSB Contribution Form"],
        "label_report_period": "Reporting Period (e.g., Q1 2025, May 2025, Annual 2024)",
        "button_generate_report": "Generate Report (Prototype)",
        "warning_report_placeholder": "Report generation is a placeholder in this prototype. In the full application, this would generate a downloadable, RRA-compliant PDF document.",
        "header_prototype_report": "#### Prototype Report: {report_type} for {report_period}",
        "generated_on": "Generated on:",
        "status": "Status:",
        "key_figures": "**Key Figures (Pre-filled from your data):**",
        "figure_sales": "Total Sales:", "figure_expenses": "Total Deductible Expenses:", "figure_tax_due": "Estimated Tax Due:",
        "imagine_pdf": "**Imagine a beautifully formatted, RRA-ready PDF document here, ready for your final review and submission.**",
        "download_prototype_report": "Download Prototype Report PDF",
        "download_dummy_data": "This is a dummy PDF content for demonstration. The real app will generate actual tax forms with your data.",
        "info_review_report": "You would typically review this report before submitting it to RRA.",
        "section_past_submissions": "2. Your Past Submissions History",
        "desc_past_submissions": "Here you would see a clear, organized history of all your submitted declarations, payments, and their status.",
        "info_rra_api_future": "Direct integration with RRA APIs for electronic submission is a future enhancement (Phase 3). For now, you would use the generated reports for manual filing.",
    },
    'fr': {
        "app_title": "SME TaxEase Rwanda - Prototype",
        "welcome_page_title": "Bienvenue sur le Prototype SME TaxEase Rwanda",
        "welcome_page_desc": "Ce prototype présente les fonctionnalités clés de l'application SME TaxEase Rwanda, conçue pour simplifier la conformité fiscale pour les petites et moyennes entreprises (PME) et réduire le besoin d'experts fiscaux. Notre objectif est de fournir **toutes les informations clés** dont vous avez besoin pour gérer vos impôts de manière autonome. Utilisez la barre de navigation à gauche pour explorer les différents modules.",
        "modules_included": "Modules inclus dans ce prototype :",
        "module_welcome": "Bienvenue",
        "module_onboarding": "Intégration & Profil",
        "module_calculator": "Calculateur d'Impôts",
        "module_dashboard": "Tableau de Bord Intelligent",
        "module_guides": "Guides Éducatifs",
        "module_reporting": "Déclaration & Rapports",
        "welcome_disclaimer": "**Avertissement :** Ceci est un prototype conceptuel. Tous les calculs et données présentés sont simplifiés à des fins de démonstration et **ne constituent pas un conseil fiscal réel**. Consultez toujours les directives officielles de la RRA ou un expert fiscal qualifié pour une conformité fiscale précise.",
        "welcome_start_info": "Commencez par naviguer vers 'Intégration & Profil' pour configurer votre entreprise et découvrir votre parcours fiscal !",
        "sidebar_nav_title": "Navigation SME TaxEase",
        "go_to": "Aller à",
        "about_app_title": "À Propos de SME TaxEase",
        "about_app_desc": "Ce prototype vise à montrer comment SME TaxEase Rwanda va :\n- **Simplifier la Conformité Fiscale :** En décomposant les concepts fiscaux complexes en étapes simples.\n- **Réduire les Coûts :** En minimisant la dépendance vis-à-vis des professionnels fiscaux externes en vous donnant les moyens.\n- **Accroître la Conformité :** En fournissant des outils et des informations clairs pour des déclarations précises et opportunes.",
        "developed_by": "Développé avec ❤️ pour les PME rwandaises.",
        "copyright": "SME TaxEase Rwanda © 2025",
        "onboarding_desc_short": "Configurez le profil de votre entreprise et comprenez vos obligations fiscales.",
        "calculator_desc_short": "Estimez vos obligations fiscales en fonction de vos données financières.",
        "dashboard_desc_short": "Visualisez un résumé de votre situation fiscale, des échéances à venir et des soumissions passées.",
        "guides_desc_short": "Accédez à des explications simplifiées des obligations fiscales rwandaises et des étapes de déclaration.",
        "reporting_desc_short": "Générez des rapports fiscaux pré-remplis et comprenez les procédures de soumission.",

        # Onboarding & Profile
        "onboarding_title": "👤 Intégration & Configuration du Profil d'Entreprise",
        "onboarding_desc": "Complétez le profil de votre entreprise pour nous aider à identifier vos obligations fiscales spécifiques au Rwanda. Cette étape est conçue pour imiter les questions qu'un expert fiscal poserait pour comprendre vos catégories fiscales.",
        "section_business_info": "1. Informations de Base sur l'Entreprise",
        "label_business_name": "Nom Officiel de l'Entreprise",
        "label_rra_tin": "NIF RRA (Numéro d'Identification Fiscale)",
        "help_rra_tin": "Si vous êtes une entreprise formelle, indiquez votre NIF RRA.",
        "label_business_entity_type": "Type d'Entité Commerciale",
        "options_business_entity_type": ["Entrepreneur Individuel", "Partenariat", "Société (Ltée)", "Coopérative", "Entreprise Informelle / Micro-entreprise", "Autre"],
        "help_business_entity_type": "La structure juridique de votre entreprise a un impact sur vos obligations fiscales.",
        "label_sector": "Secteur d'Activité Principal",
        "options_sector": ["Commerce de Détail", "Services", "Agriculture", "Fabrication", "TIC", "Tourisme", "Conseil", "Autre"],
        "help_sector": "Certains secteurs peuvent bénéficier de traitements fiscaux spécifiques ou d'incitations.",
        "label_registration_date": "Date d'Enregistrement de l'Entreprise (si formelle)",
        "section_key_tax_questions": "2. Questions Clés Liées à l'Impôt",
        "label_estimated_annual_turnover": "Chiffre d'Affaires Annuel Estimé (RWF)",
        "help_estimated_annual_turnover": "Votre chiffre d'affaires total estimé pour une année complète. Cela aide à déterminer l'applicabilité de la TVA et de l'Impôt sur le Chiffre d'Affaires.",
        "label_has_employees": "Avez-vous des employés (salariés) ?",
        "help_has_employees": "Ceci détermine si vous devez payer le PAYE et la RSSB.",
        "label_is_vat_registered_onboard": "Êtes-vous actuellement enregistré à la TVA ?",
        "help_is_vat_registered_onboard": "Si votre chiffre d'affaires dépasse 20 millions de RWF annuellement ou 5 millions de RWF trimestriellement, vous devez probablement être enregistré à la TVA.",
        "info_informal_business": "En tant qu'entreprise informelle, comprendre les étapes de la formalisation est essentiel pour simplifier les impôts. Nous vous guiderons !",
        "section_contact_info": "3. Coordonnées",
        "label_contact_person": "Personne de Contact Principale",
        "label_phone_number": "Numéro de Téléphone",
        "label_email_address": "Adresse E-mail",
        "label_address": "Adresse de l'Entreprise",
        "button_save_profile": "Enregistrer le Profil et Déterminer les Obligations Fiscales",
        "success_profile_saved": "Profil d'entreprise pour '{business_name}' enregistré avec succès !",
        "header_estimated_obligations": "Vos Obligations Fiscales Estimées :",
        "info_preliminary_assessment": "Sur la base de votre profil, voici les impôts auxquels vous pourriez être obligé de vous conformer au Rwanda. Il s'agit d'une évaluation préliminaire ; les calculs détaillés se trouvent dans le Calculateur d'Impôts.",
        "no_paye_rssb_info": "*(Aucun PAYE/RSSB attendu car vous avez indiqué ne pas avoir d'employés)*",
        "what_s_next": "Et après ?",
        "next_calc_guide": "1. **Allez au `Calculateur d'Impôts`** : Utilisez vos ventes réelles, vos dépenses et vos salaires pour obtenir des estimations précises.",
        "next_explore_guides": "2. **Explorez les `Guides Éducatifs`** : Apprenez-en davantage sur chacune de vos obligations fiscales identifiées en langage simple.",
        "next_formalization": "3. **Envisagez la Formalisation (pour les entreprises informelles)** : Nos guides peuvent vous aider à comprendre les avantages et les étapes.",
        "data_stored_info": "Dans une application réelle, ces données seraient stockées dans votre base de données backend.",

        # Tax Calculator (Partial Translation - full app needs full strings)
        "calculator_title": "📊 Calculateur d'Impôts Convivial",
        "calculator_desc": "Saisissez vos données financières réelles pour une période spécifique afin d'obtenir une estimation de votre charge fiscale. Ceci vise à fournir les calculs clés qu'un expert fiscal effectuerait.",
        "section_business_period": "1. Période Commerciale et de Déclaration",
        "label_business_type_calc": "Type d'Entreprise",
        "help_business_type_calc": "Sélectionnez si votre entreprise est formellement enregistrée ou opère de manière informelle. Cela affecte l'applicabilité fiscale.",
        "label_is_vat_registered_calc": "Votre entreprise est-elle enregistrée à la TVA ?",
        "help_is_vat_registered_calc": "Cochez si votre entreprise est enregistrée pour la Taxe sur la Valeur Ajoutée (TVA).",
        "label_has_employees_calc": "Avez-vous des employés ?",
        "help_has_employees_calc": "Cela influence les calculs du PAYE et de la RSSB.",
        "label_num_employees": "Nombre d'Employés",
        "label_is_small_business_for_turnover_tax": "Votre entreprise est-elle éligible à l'Impôt sur le Chiffre d'Affaires (généralement pour les petites entreprises non enregistrées à la TVA) ?",
        "help_is_small_business_for_turnover_tax": "Ceci s'applique généralement aux petites entreprises en dessous du seuil de TVA. Si vous êtes enregistré à la TVA, l'Impôt sur les Sociétés s'applique.",
        "header_reporting_period": "Période de Déclaration",
        "label_start_date": "Date de Début",
        "label_end_date": "Date de Fin",
        "section_financial_inputs": "2. Données Financières (Tous les chiffres en RWF)",
        "label_turnover": "Chiffre d'Affaires Total de l'Entreprise / Ventes pour la Période",
        "help_turnover": "Revenus totaux générés par vos ventes de biens/services.",
        "label_vat_eligible_sales": "Ventes Éligibles à la TVA",
        "help_vat_eligible_sales": "La partie de votre chiffre d'affaires soumise à la TVA.",
        "label_total_expenses": "Total des Dépenses Déductibles pour la Période",
        "help_total_expenses": "Toutes les dépenses d'entreprise autorisées qui réduisent votre revenu imposable.",
        "label_salaries_paid_gross": "Salaires Bruts Totaux Payés (pour tous les employés pour la période)",
        "help_salaries_paid_gross": "Somme de tous les salaires bruts payés à vos employés pendant cette période.",
        "label_other_taxable_income": "Autres Revenus Imposables (ex: des investissements)",
        "help_other_taxable_income": "Tout autre revenu soumis à l'impôt sur les sociétés qui ne provient pas des ventes principales.",
        "label_depreciation_on_assets": "Amortissement des Actifs (le cas échéant)",
        "help_depreciation_on_assets": "Usure déductible de vos actifs commerciaux. Consultez la RRA pour les taux spécifiques.",
        "button_calculate_taxes": "Calculer les Impôts Estimés",
        "section_estimated_results": "3. Résultats Fiscaux Estimés",
        "total_tax_due": "Total de l'Impôt Estimé Dû :",
        "info_estimated_figures": "Ces chiffres sont des estimations basées sur vos données et les **règles simplifiées de la RRA** utilisées dans ce prototype.",
        "view_detailed_breakdown": "Voir la Ventilation Détaillée",
        "breakdown_by_tax_type": "#### Ventilation par Type d'Impôt :",
        "paye_amount": "PAYE (Impôt sur les Salaires) :",
        "vat_amount": "TVA (Taxe sur la Valeur Ajoutée) :",
        "turnover_tax_amount": "Impôt sur le Chiffre d'Affaires :",
        "corporate_tax_amount": "Impôt sur les Sociétés :",
        "rssb_total_contribution": "Contributions RSSB (Total) :",
        "rssb_employee_share": "Part Salarié :",
        "rssb_employer_share": "Part Employeur :",
        "calc_notes": "Remarques : Les calculs sont basés sur des règles de prototypage très simplifiées. Les règles réelles de la RRA sont considérablement plus complexes et doivent être consultées. Cet outil est uniquement destiné à l'estimation.",
        "section_required_documents": "4. Quels Documents Devez-vous Préparer ?",
        "documents_desc": "Sur la base des impôts calculés, vous avez généralement besoin des documents suivants pour la soumission officielle à la RRA :",
        "doc_all_taxes": "* **Pour tous les impôts :** Registres financiers (Grand Livre des Revenus et Dépenses), Relevés Bancaires.",
        "doc_vat": "* **TVA :** Factures de Ventes, Factures d'Achats, Notes de crédit de TVA en amont, Notes de débit de TVA en aval.",
        "doc_paye_rssb": "* **PAYE & RSSB :** Registre de Paie, Contrats d'Employés, Preuve des contributions RSSB.",
        "doc_corporate_tax": "* **Impôt sur les Sociétés :** États Financiers Audités (pour les grandes entreprises), Compte de Résultat, Bilan, Reçus de Dépenses.",
        "doc_turnover_tax": "* **Impôt sur le Chiffre d'Affaires :** Registres des Ventes/Chiffre d'Affaires.",
        "action_keep_records": "**Action :** Conservez des registres clairs et organisés tout au long de la période fiscale.",
        "quick_links_info": "#### Liens Rapides pour Plus d'Infos :",

        # Smart Dashboard
        "dashboard_title": "📈 Tableau de Bord Intelligent",
        "dashboard_desc": "Obtenez un aperçu rapide de votre situation fiscale, de vos déclarations passées et de vos échéances à venir. Ceci vise à fournir la supervision clé qu'un expert fiscal vous donnerait.",
        "overview_obligations": "Aperçu des Obligations Actuelles",
        "metric_upcoming_deadline": "Prochaine Échéance",
        "metric_last_filed_tax": "Dernier Impôt Déclaré",
        "metric_compliance_score": "Statut Général de Conformité (Fictif)",
        "header_compliance_calendar": "Votre Calendrier de Conformité Fiscale",
        "info_deadlines": "**Dates Limites Clés au Rwanda (Exemples Généraux - toujours vérifier les dates officielles de la RRA) :**\n* **15 du mois :** Contributions PAYE & RSSB pour le mois précédent.\n* **15 du mois :** Déclaration & paiement TVA pour le mois précédent (si applicable).\n* **20 du mois suivant le trimestre :** Déclaration & paiement Impôt sur le Chiffre d'Affaires (si applicable).\n* **31 mars (année suivante) :** Déclaration Annuelle de l'Impôt sur les Sociétés.",
        "header_recent_declarations": "Déclarations et Paiements Récents",
        "col_tax_type": "Type d'Impôt", "col_period": "Période", "col_amount_due": "Montant Dû (RWF)", "col_status": "Statut", "col_filing_date": "Date de Déclaration", "col_receipt": "Reçu", "col_amount_paid": "Montant Payé (RWF)",
        "header_alerts_reminders": "Alertes et Rappels Actionnables",
        "alert_vat_due": "⚠️ **Action Requise :** Votre déclaration de TVA pour le T2 2025 est due le 20 juillet 2025. Veuillez compléter le Calculateur d'Impôts et préparer votre rapport.",
        "info_rssb_remitted": "✅ Toutes les contributions RSSB des employés pour juin ont été remises. Bon travail !",
        "alert_corporate_tax_upcoming": "🔔 **À Venir :** L'Impôt sur les Sociétés pour 2025 sera dû le 31 mars 2026. Commencez à rassembler les dossiers financiers annuels.",
        "status_filed": 'Déclaré', "status_pending": 'En attente', "receipt_view": 'Voir', "receipt_na": 'N/A', "status_submitted_paid": 'Soumis & Payé', "receipt_download": 'Télécharger',

        # Educational Guides (Partial Translation)
        "guides_title": "📚 Guides Éducatifs : Simplifier la Connaissance Fiscale",
        "guides_desc": "Accédez à des explications simplifiées et claires des obligations fiscales rwandaises et des instructions de dépôt pas à pas. Notre objectif est de rendre l'information fiscale si claire que vous n'aurez pas besoin d'un expert fiscal pour comprendre vos obligations.",
        "header_explore_guides": "Explorez les Types d'Impôts Rwandais Clés :",
        "guide_select_placeholder": "Sélectionnez un Sujet Fiscal",
        "info_guide_coming_soon": "Le contenu de ce guide arrive bientôt ! Veuillez sélectionner un autre guide.",
        "link_rra_website": "Pour les directives officielles de la RRA, veuillez visiter le [site web de l'Autorité Revenue Rwandaise](https://www.rra.gov.rw).",
        "guide_vat_title": "Comprendre la TVA au Rwanda", # Placeholder for content
        "guide_vat_content": "Contenu de la TVA en français... (Please expand with full content as provided in EN)",
        "guide_paye_title": "Comment Calculer le PAYE", # Placeholder for content
        "guide_paye_content": "Contenu du PAYE en français... (Please expand with full content as provided in EN)",
        "guide_turnover_tax_title": "L'Impôt sur le Chiffre d'Affaires pour PME Expliqué", # Placeholder for content
        "guide_turnover_tax_content": "Contenu de l'Impôt sur le Chiffre d'Affaires en français... (Please expand with full content as provided in EN)",
        "guide_corporate_tax_title": "Bases de l'Impôt sur les Sociétés pour Débutants", # Placeholder for content
        "guide_corporate_tax_content": "Contenu de l'Impôt sur les Sociétés en français... (Please expand with full content as provided in EN)",
        "guide_rssb_title": "Contributions au Conseil de Sécurité Sociale du Rwanda (RSSB)", # Placeholder for content
        "guide_rssb_content": "Contenu de la RSSB en français... (Please expand with full content as provided in EN)",
        "guide_registration_title": "Enregistrer votre entreprise auprès de la RRA", # Placeholder for content
        "guide_registration_content": "Contenu de l'enregistrement en français... (Please expand with full content as provided in EN)",

        # Declaration & Reporting (Partial Translation)
        "reporting_title": "📑 Déclaration & Rapports : Votre Assistant de Dépôt",
        "reporting_desc": "Ce module est conçu pour simplifier votre processus de déclaration fiscale, visant à fournir toutes les informations et les étapes dont vous avez besoin sans expert. Il vous permettra de générer des formulaires de déclaration fiscale pré-remplis et des rapports, et éventuellement de faciliter la soumission directe à la RRA (sous réserve d'intégration API).",
        "section_generate_report": "1. Générer un Nouveau Rapport/Déclaration",
        "info_auto_populate": "Imaginez cette section se remplissant automatiquement à partir de vos dossiers financiers enregistrés et des calculs précédents du 'Calculateur d'Impôts'.",
        "label_report_type": "Sélectionner le Type de Rapport",
        "options_report_type": ["Formulaire de Déclaration TVA", "Formulaire de Déclaration PAYE", "Rapport Annuel d'Impôt sur les Sociétés", "Déclaration d'Impôt sur le Chiffre d'Affaires", "Formulaire de Cotisation RSSB"],
        "label_report_period": "Période de Déclaration (ex: T1 2025, Mai 2025, Annuel 2024)",
        "button_generate_report": "Générer le Rapport (Prototype)",
        "warning_report_placeholder": "La génération de rapports est un placeholder dans ce prototype. Dans l'application complète, cela générerait un document PDF téléchargeable et conforme à la RRA.",
        "header_prototype_report": "#### Rapport Prototype : {report_type} pour {report_period}",
        "generated_on": "Généré le :",
        "status": "Statut :",
        "key_figures": "**Chiffres Clés (Pré-remplis à partir de vos données) :**",
        "figure_sales": "Ventes Totales :", "figure_expenses": "Dépenses Déductibles Totales :", "figure_tax_due": "Impôt Estimé Dû :",
        "imagine_pdf": "**Imaginez un document PDF magnifiquement formaté, prêt pour la RRA, prêt pour votre examen final et soumission.**",
        "download_prototype_report": "Télécharger le Rapport Prototype PDF",
        "download_dummy_data": "Ceci est un contenu PDF factice pour la démonstration. L'application réelle générera de vrais formulaires fiscaux avec vos données.",
        "info_review_report": "Vous devriez normalement examiner ce rapport avant de le soumettre à la RRA.",
        "section_past_submissions": "2. Historique de vos Soumissions Passées",
        "desc_past_submissions": "Ici, vous verriez un historique clair et organisé de toutes vos déclarations soumises, de vos paiements et de leur statut.",
        "info_rra_api_future": "L'intégration directe avec les API de la RRA pour la soumission électronique est une amélioration future (Phase 3). Pour l'instant, vous utiliseriez les rapports générés pour le dépôt manuel.",
    },
    'rw': {
        "app_title": "SME TaxEase Rwanda - Urugero rwa Mbere",
        "welcome_page_title": "Murakaza Neza kuri SME TaxEase Rwanda - Urugero rwa Mbere",
        "welcome_page_desc": "Uru rugero rwa mbere rugaragaza imikorere nyamukuru y'Ikoranabuhanga rya SME TaxEase Rwanda, ryashyizweho kugira ngo ryoroshye kubahiriza amategeko y'imisoro ku bigo bito n'ibiciriritse (SMEs) kandi rigabanye ikiguzi cyo gukoresha abahanga mu misoro. Intego yacu ni ugutanga **amakuru yose y'ingenzi** mukeneye kugira ngo muyobore imisoro yanyu ubwanyu. Koresha ububiko (sidebar) ibumoso kugira ngo murebe ibice bitandukanye by'iyi porogaramu.",
        "modules_included": "Ibice bigize uru rugero rwa mbere:",
        "module_welcome": "Murakaza Neza",
        "module_onboarding": "Kwandikisha & Konti y'Ubucuruzi",
        "module_calculator": "Ibaruramihigo ry'Imisoro",
        "module_dashboard": "Imiyoboro y'Ikoranabuhanga (Dashboard)",
        "module_guides": "Amabwiriza y'Uburezi",
        "module_reporting": "Itangazamisoro & Raporo",
        "welcome_disclaimer": "**Intangiriro:** Uru ni urugero rwa mbere rwa porogaramu gusa. Imibare yose n'amakuru agaragara hano byoroshye kugira ngo bigaragarizwe gusa, kandi **ntabwo bigize inama nyazo z'imisoro**. Buri gihe mugomba kugisha inama z'amategeko y'imisoro ku kigo cy'Igihugu cy'Imisoro (RRA) cyangwa umuhanga mu misoro wemewe kugira ngo mubahirize neza amategeko y'imisoro.",
        "welcome_start_info": "Tangira ugana ku 'Kwandikisha & Konti y'Ubucuruzi' kugira ngo mushyireho ubucuruzi bwanyu kandi mumenye urugendo rwanyu rw'imisoro!",
        "sidebar_nav_title": "Imikorere ya SME TaxEase",
        "go_to": "Jya kuri",
        "about_app_title": "Ibyerekeye SME TaxEase",
        "about_app_desc": "Uru rugero rwa mbere rugamije kwerekana uburyo SME TaxEase Rwanda izagira uruhare mu:\n- **Kworoshya kubahiriza imisoro:** Mu kumenya imisoro igoye mu buryo bworoshye.\n- **Kugabanya ibiciro:** Mu kugabanya gushingira ku bahanga mu misoro b'inyuma mukoresha ikoranabuhanga riyobora.\n- **Kongera kubahiriza amategeko:** Mu gutanga ibikoresho n'amakuru asobanutse kugira ngo murusheho kuzuza neza amategeko mu gihe gikwiye.",
        "developed_by": "Yateguwe na ❤️ ku bwa SMEs zo mu Rwanda.",
        "copyright": "SME TaxEase Rwanda © 2025",
        "onboarding_desc_short": "Shyiraho konti y'ubucuruzi bwawe kandi wumve inshingano zawe z'imisoro.",
        "calculator_desc_short": "Bara imisoro yawe ishingiye ku makuru y'amafaranga yawe.",
        "dashboard_desc_short": "Reba inshamake y'imisoro yawe, amatariki ntarengwa yegereje, n'imisoro yashize.",
        "guides_desc_short": "Bona ibisobanuro byoroshye by'imisoro mu Rwanda n'intambwe z'uburyo bwo kwishyura.",
        "reporting_desc_short": "Tanga raporo z'imisoro zikuzuwe n'uburyo bwo gutanga.",

        # Onboarding & Profile
        "onboarding_title": "👤 Kwandikisha & Konti y'Ubucuruzi",
        "onboarding_desc": "Uzuza imyirondoro y'ubucuruzi bwawe kugira ngo tubashe kumenya inshingano zawe z'imisoro mu Rwanda. Iri tsinda ryateguwe kugira ngo ryigane ibibazo umuhanga mu misoro yabaza kugira ngo asobanukirwe imisoro yawe.",
        "section_business_info": "1. Amakuru shingiro y'Ubucuruzi",
        "label_business_name": "Izina ry'Ubucuruzi bwemewe",
        "label_rra_tin": "NIF ya RRA (Nimero y'Ubucuruzi)",
        "help_rra_tin": "Niba uri ubucuruzi bwemewe, tunga NIF ya RRA.",
        "label_business_entity_type": "Ubwoko bw'Ikigo cy'Ubucuruzi",
        "options_business_entity_type": ["Ubucuruzi bw'Umuntu Ku Giti Cye", "Ubufatanye", "Sosiyete (Ltée)", "Koperative", "Ubucuruzi Butemewe / Ubucuruzi Bworoheje", "Ikindi"],
        "help_business_entity_type": "Uburyo ubucuruzi bwawe bushyizweho bugira ingaruka ku nshingano zawe z'imisoro.",
        "label_sector": "Urwego Nyamukuru rw'Ubucuruzi",
        "options_sector": ["Ubucuruzi bw'Ebyiri", "Serivisi", "Ubuhinzi", "Uruganda", "Ikoranabuhanga", "Ubukerarugendo", "Ubwunganizi", "Ikindi"],
        "help_sector": "Amwe mu nzego ashobora kugira imisoro yihariye cyangwa inkunga.",
        "label_registration_date": "Itariki y'Imeza ry'Ubucuruzi (niba bwemewe)",
        "section_key_tax_questions": "2. Ibibazo by'ingenzi bijyanye n'Imisoro",
        "label_estimated_annual_turnover": "Umuvuno w'Ubucuruzi witezwe ku mwaka (RWF)",
        "help_estimated_annual_turnover": "Umuvuno w'amafaranga witezwe mu mwaka wose. Ibi bifasha kumenya ko ubahiriza TVA n'imisoro y'Umuvuno.",
        "label_has_employees": "Ufite abakozi (bahemberwa)?",
        "help_has_employees": "Ibi bigena niba ugomba kwishyura PAYE na RSSB.",
        "label_is_vat_registered_onboard": "Uwanditse muri TVA?",
        "help_is_vat_registered_onboard": "Niba umuvuno w'ubucuruzi bwawe urenze Miliyoni 20 RWF ku mwaka cyangwa Miliyoni 5 RWF buri gihembwe, ushobora kuba ugomba kwandikwa muri TVA.",
        "info_informal_business": "Niba uri ubucuruzi butemewe, kumenya intambwe zo kumenyekana ni ingenzi kugira ngo woroshye imisoro. Tuzakuyobora!",
        "section_contact_info": "3. Amakuru y'Irangamuntu",
        "label_contact_person": "Uwegerwa Mukuru",
        "label_phone_number": "Nimero ya Telefone",
        "label_email_address": "Ibarufasha",
        "label_address": "Aho Ubucuruzi Bukorera",
        "button_save_profile": "Ongeramo Amakuru & Menya Inshingano z'Imisoro",
        "success_profile_saved": "Amakuru y'ubucuruzi ya '{business_name}' yashyizwemo neza!",
        "header_estimated_obligations": "Inshingano zawe z'Imisoro ziteganijwe :",
        "info_preliminary_assessment": "Hashingiwe ku makuru yawe, dore imisoro ushobora kuba ufite inshingano zo kubahiriza mu Rwanda. Iyi ni igenzura rya mbere; imibare irambuye izaboneka mu Ibaruramihigo ry'Imisoro.",
        "no_paye_rssb_info": "*(Nta PAYE/RSSB iteganijwe kubera ko wagaragaje ko nta bakozi ufite)*",
        "what_s_next": "Ibikurikira?",
        "next_calc_guide": "1. **Jya kuri `Ibaruramihigo ry'Imisoro`**: Koresha umuvuno wawe w'ukuri, ibyagombye n'imihembero kugira ngo ubone imibare nyayo.",
        "next_explore_guides": "2. **Reba `Amabwiriza y'Uburezi`**: Menya byinshi kuri buri nshingano yawe y'imisoro mu rurimi rworoshye.",
        "next_formalization": "3. **Tekereza kumenyekana (ku bucuruzi butemewe)**: Amabwiriza yacu ashobora kugufasha kumva inyungu n'intambwe.",
        "data_stored_info": "Muri porogaramu yuzuye, aya makuru yashyirwa mu bubiko bwanyu bwa backend.",

        # Tax Calculator (Partial Translation)
        "calculator_title": "📊 Ibaruramihigo ry'Imisoro Ryoroheje",
        "calculator_desc": "Shyiramo imibare y'amafaranga yawe y'ukuri mu gihe cyagenwe kugira ngo ubone imisoro iteganijwe. Ibi bigamije gutanga imibare nyamukuru umuhanga mu misoro yakora.",
        "section_business_period": "1. Ubucuruzi & Igihe cyo Gutangaza",
        "label_business_type_calc": "Ubwoko bw'Ubucuruzi",
        "help_business_type_calc": "Hitamo niba ubucuruzi bwawe bwemewe cyangwa bukora mu buryo butemewe. Ibi bigira ingaruka ku micungire y'imisoro.",
        "label_is_vat_registered_calc": "Ubucuruzi bwawe bwanditswe muri TVA?",
        "help_is_vat_registered_calc": "Kanda niba ubucuruzi bwawe bwanditswe muri Taxe sur la Valeur Ajoutée (TVA).",
        "label_has_employees_calc": "Ufite abakozi?",
        "help_has_employees_calc": "Ibi bigira ingaruka ku mibare ya PAYE na RSSB.",
        "label_num_employees": "Umubare w'Abakozi",
        "label_is_small_business_for_turnover_tax": "Ubucuruzi bwawe bushobora kwishyura imisoro y'Umuvuno (bisanzwe ku bigo bito bitanditse muri TVA)?",
        "help_is_small_business_for_turnover_tax": "Ibi bisanzwe bikoreshwa ku bigo bito biri munsi y'umuvuno w'imisoro ya TVA. Niba bwanditswe muri TVA, hagomba kuba imisoro y'isosiyete.",
        "header_reporting_period": "Igihe cyo Gutangaza",
        "label_start_date": "Itariki yo Gutangira",
        "label_end_date": "Itariki yo kurangira",
        "section_financial_inputs": "2. Amakuru y'Amafaranga (Imibare yose muri RWF)",
        "label_turnover": "Umuvuno w'Ubucuruzi Wose/Amagurishwe muri Igihe",
        "help_turnover": "Amafaranga yose yinjiye mu bucuruzi bwawe avuye mu kugurisha ibicuruzwa/serivisi.",
        "label_vat_eligible_sales": "Amagurishwe agomba VAT",
        "help_vat_eligible_sales": "Igice cy'umuvuno wawe kigomba VAT.",
        "label_total_expenses": "Ibiyagombwa Byose bigabanywa mu gihe",
        "help_total_expenses": "Amafaranga yose y'ubucuruzi yemewe agabanya umusoro.",
        "label_salaries_paid_gross": "Imihembero yose itavangiye yishyuwe (ku bakozi bose mu gihe)",
        "help_salaries_paid_gross": "Somme de tous les salaires bruts payés à vos employés pendant cette période.",
        "label_other_taxable_income": "Ayandi mafaranga agomba umusoro (urugero: avuye mu ishoramari)",
        "help_other_taxable_income": "Ayandi mafaranga yinjira agomba imisoro y'ubucuruzi atari ay'ubucuruzi bwibanze.",
        "label_depreciation_on_assets": "Kwangirika kw'Imitungo (niba bigaragara)",
        "help_depreciation_on_assets": "Igabanuka ry'agaciro k'imitungo yawe y'ubucuruzi ryemewe. Gisha inama RRA ku bijyanye n'imibare yihariye.",
        "button_calculate_taxes": "Bara Imisoro Itenganijwe",
        "section_estimated_results": "3. Ibisubizo by'Imisoro Itenganijwe",
        "total_tax_due": "Umusoro Wose Utenganijwe:",
        "info_estimated_figures": "Iyi mibare ni iy'icyitegererezo gusa ishingiye ku makuru mwashyizemo n'amategeko **yorohejwe ya RRA** yakoreshejwe muri uru rugero rwa mbere.",
        "view_detailed_breakdown": "Reba Imibare Irangije",
        "breakdown_by_tax_type": "#### Imibare irangije ku bwoko bw'Imisoro:",
        "paye_amount": "PAYE (Umusoro ku Mihembero):",
        "vat_amount": "TVA (Umusoro ku Gicuruzwa):",
        "turnover_tax_amount": "Umusoro ku Muvuno:",
        "corporate_tax_amount": "Umusoro ku Isosiyete:",
        "rssb_total_contribution": "Inkunga za RSSB (Umusoro Wose):",
        "rssb_employee_share": "Umusoro w'Umukozi:",
        "rssb_employer_share": "Umusoro w'Umukoresha:",
        "calc_notes": "Inyandiko: Imibare ishingiye ku mategeko yoroheje yo kugerageza. Amategeko nyayo ya RRA aragoye cyane kandi agomba kugisha inama. Iki gikoresho ni icya estimation gusa.",
        "section_required_documents": "4. Ni Iki Kigomba Gutegurwa?",
        "documents_desc": "Hashingiwe ku misoro yishyuwe, mukenera ibyangombwa bikurikira kugira ngo mutange raporo mu buryo bwemewe na RRA:",
        "doc_all_taxes": "* **Ku misoro yose:** Ibyangombwa by'imari (Ubwigenge bw'Amihembero n'Ibiyagombwa), Inyandiko z'amabanki.",
        "doc_vat": "* **TVA:** Inyandiko z'amagurishwe, Inyandiko z'ibicuruzwa byaguzwe, Inyandiko z'amafaranga ya TVA yishyurwa, Inyandiko z'amafaranga ya TVA yakiriwe.",
        "doc_paye_rssb": "* **PAYE & RSSB:** Inyandiko z'amihembero, Amasezerano y'abakozi, Ibigaragaza inkunga za RSSB.",
        "doc_corporate_tax": "* **Umusoro ku Isosiyete:** Ibyangombwa by'imari byagenzuwe (ku bigo binini), Inyandiko y'Urusaruro, Ifaranga rya Balance, Inyandiko z'Ibiyagombwa.",
        "doc_turnover_tax": "* **Umusoro ku Muvuno:** Inyandiko z'amagurishwe/Umuvuno.",
        "action_keep_records": "**Igikorwa:** Gukomeza inyandiko zisobanutse kandi zateguwe mu gihe cyose cy'imisoro.",
        "quick_links_info": "#### Amapfundo Yihuse kuri Amakuru Menshi:",

        # Smart Dashboard (Partial Translation)
        "dashboard_title": "📈 Imiyoboro y'Ikoranabuhanga (Dashboard)",
        "dashboard_desc": "Reba vuba ibyerekeye imisoro yawe, imyenda y'imbere, n'igihe gisigaye cyo gutangaza. Ibi bigamije gutanga ubugenzuzi nyamukuru umuhanga mu misoro yagutera.",
        "overview_obligations": "Amakuru Rusange ku Nshingano zawe z'Ubu",
        "metric_upcoming_deadline": "Igihe Gisigaye Cyegereje",
        "metric_last_filed_tax": "Umusoro Waherukaga Gutangazwa",
        "metric_compliance_score": "Umusaruro Rusange wo Kubahiriza (Urugero)",
        "header_compliance_calendar": "Kalendari yawe yo Kubahiriza Amategeko y'Imisoro",
        "info_deadlines": "**Amatariki ntarengwa y'ingenzi mu Rwanda (Ingero Rusange - buri gihe hamenya amatariki yemewe na RRA):**\n* **Tariki 15 buri kwezi:** Inkunga za PAYE & RSSB z'ukwezi kwashize.\n* **Tariki 15 buri kwezi:** Itangazamisoro rya TVA & kwishyura ukwezi kwashize (niba bikora).\n* **Tariki 20 z'ukwezi nyuma y'igihembwe:** Itangazamisoro ry'Umuvuno & kwishyura (niba bikora).\n* **31 Werurwe (umwaka ukurikira):** Itangazamisoro ry'Umusoro ku Sosiyete ku mwaka.",
        "header_recent_declarations": "Itangazamisoro & Kwishyura biheruka",
        "col_tax_type": "Ubwoko bw'Umusoro", "col_period": "Igihe", "col_amount_due": "Amafaranga agomba kwishyurwa (RWF)", "col_status": "Status", "col_filing_date": "Itariki yo Gutangaza", "col_receipt": "Inyemezabuguzi", "col_amount_paid": "Amafaranga Yishyuwe (RWF)",
        "header_alerts_reminders": "Indi Miburo & Ibyibutsa",
        "alert_vat_due": "⚠️ **Kugomba Gukorwa:** Itangazamisoro rya TVA ryawe rya Q2 2025 rigomba kuba ryatanzwe bitarenze tariki 20 Nyakanga 2025. Mugomba kuzuza Ibaruramihigo ry'Imisoro hanyuma mugategura raporo yanyu.",
        "info_rssb_remitted": "✅ Inkunga zose za RSSB z'abakozi za Kamena zashyizweho. Murakoze!",
        "alert_corporate_tax_upcoming": "🔔 **Biteganijwe:** Umusoro ku Sosiyete wa 2025 uzagomba kuba watanzwe bitarenze tariki 31 Werurwe 2026. Tangira gukusanya amakuru y'imari ya buri mwaka.",
        "status_filed": 'Yatanzwe', "status_pending": 'Iritegereje', "receipt_view": 'Reba', "receipt_na": 'Ntibireba', "status_submitted_paid": 'Yaratanzwe & Yishyuzwe', "receipt_download": 'Kukurura',

        # Educational Guides (Partial Translation)
        "guides_title": "📚 Amabwiriza y'Uburezi: Kworohesha Ubumenyi bw'Imisoro",
        "guides_desc": "Reba ibisobanuro byoroheje kandi byumvikana ku nshingano z'imisoro mu Rwanda n'amabwiriza y'intambwe ku yindi. Intego yacu ni ugutanga amakuru y'imisoro asobanutse cyane ku buryo utazagomba kugisha inama umuhanga mu misoro kugira ngo usobanukirwe inshingano zawe.",
        "header_explore_guides": "Reba Ubwoko bw'Imisoro y'Ingenzi mu Rwanda:",
        "guide_select_placeholder": "Hitamo Ingingo y'Imisoro",
        "info_guide_coming_soon": "Iby'ubu bwoko buracyategurwa! Nyamuneka hitamo ubundi bwoko.",
        "link_rra_website": "Kugira ngo ubone amabwiriza yemewe na RRA, nyamuneka sura [urubuga rwa Rwanda Revenue Authority](https://www.rra.gov.rw).",
        "guide_vat_title": "Kumenya TVA mu Rwanda", # Placeholder for content
        "guide_vat_content": "Amakuru y'umusoro kuri TVA mu Kinyarwanda... (Kwandika amakuru arambuye nk'ay'Icyongereza)",
        "guide_paye_title": "Uko Babara PAYE", # Placeholder for content
        "guide_paye_content": "Amakuru y'umusoro kuri PAYE mu Kinyarwanda... (Kwandika amakuru arambuye nk'ay'Icyongereza)",
        "guide_turnover_tax_title": "Umusoro ku Muvuno wa SME Urasobanutse", # Placeholder for content
        "guide_turnover_tax_content": "Amakuru y'umusoro ku muvuno mu Kinyarwanda... (Kwandika amakuru arambuye nk'ay'Icyongereza)",
        "guide_corporate_tax_title": "Ibanze ry'Umusoro ku Isosiyete ku Batangira", # Placeholder for content
        "guide_corporate_tax_content": "Amakuru y'umusoro ku sosiyete mu Kinyarwanda... (Kwandika amakuru arambuye nk'ay'Icyongereza)",
        "guide_rssb_title": "Inkunga z'Ikigo cy'Umutekano Rusange mu Rwanda (RSSB)", # Placeholder for content
        "guide_rssb_content": "Amakuru y'inkunga za RSSB mu Kinyarwanda... (Kwandika amakuru arambuye nk'ay'Icyongereza)",
        "guide_registration_title": "Kwandikisha Ubucuruzi bwawe muri RRA", # Placeholder for content
        "guide_registration_content": "Amakuru y'uburyo bwo kwandikisha mu Kinyarwanda... (Kwandika amakuru arambuye nk'ay'Icyongereza)",

        # Declaration & Reporting (Partial Translation)
        "reporting_title": "📑 Itangazamisoro & Raporo: Umufasha wawe mu Gutangaza",
        "reporting_desc": "Iki gice cyagenewe kworohesha uburyo bwo gutangaza imisoro, kigamije gutanga amakuru n'intambwe zose ukeneye nta muhanga. Kizagufasha gutanga imisoro yakuzuwa mbere n'amafunguro, kandi eventually kizatuma bishoboka gutanga raporo kuri RRA (bitewe n'iyinjizwa rya API).",
        "section_generate_report": "1. Gutanga Raporo/Itangazamisoro Rishya",
        "info_auto_populate": "Tekereza iki gice cyikuzamo amakuru ashingiye ku byanditswe by'amafaranga byawe byabitswe n'imibare y'imbere kuva muri 'Ibaruramihigo ry'Imisoro'.",
        "label_report_type": "Hitamo Ubwoko bwa Raporo",
        "options_report_type": ["Raporo y'Itangazamisoro rya TVA", "Raporo y'Itangazamisoro rya PAYE", "Raporo y'Umusoro ku Sosiyete ku Mwaka", "Raporo y'Umusoro ku Muvuno", "Inyandiko y'Inkunga za RSSB"],
        "label_report_period": "Igihe cyo Gutangaza (urugero: Q1 2025, Gicurasi 2025, Umwaka wa 2024)",
        "button_generate_report": "Gutanga Raporo (Urugero)",
        "warning_report_placeholder": "Gutanga raporo ni urugero muri porogaramu. Muri porogaramu yuzuye, ibi byazatuma haboneka PDF ishobora gukururwa, yujuje ibisabwa na RRA.",
        "header_prototype_report": "#### Raporo y'Urugero: {report_type} yo muri {report_period}",
        "generated_on": "Yashyizweho ku:",
        "status": "Status:",
        "key_figures": "**Imibare y'Ingenzi (Yakuzuwe mbere nawe):**",
        "figure_sales": "Umuvuno Wose:", "figure_expenses": "Ibiyagombwa Byose Byagabanywa:", "figure_tax_due": "Umusoro Utenganijwe:",
        "imagine_pdf": "**Tekereza inyandiko ya PDF yateguwe neza, yiteguye RRA, yiteguye gusubirwamo bwa nyuma no gutangazwa.**",
        "download_prototype_report": "Kukurura Raporo y'Urugero ya PDF",
        "download_dummy_data": "Iyi ni inyandiko ya PDF y'urugero gusa. Porogaramu nyayo izatanga amakuru y'imisoro y'ukuri n'amakuru yawe.",
        "info_review_report": "Wakwibushaho kugenzura iyi raporo mbere yo kuyishyira muri RRA.",
        "section_past_submissions": "2. Amateka y'Itangazamisoro yawe ya Kera",
        "desc_past_submissions": "Hano uzabona amateka asobanutse kandi ateguye y'itangazamisoro ryawe ryose ryatanzwe, amafaranga yishyuwe, n'imiterere yabyo.",
        "info_rra_api_future": "Ihuza ryigenga na API za RRA zo gutangaza mu buryo bw'ikoranabuhanga ni intego y'igihe kizaza (Icyiciro cya 3). Ku ikubitiro, uzakoresha raporo zatanzwe mu buryo bw'intoki.",
    }
}

# --- Streamlit Session State for Language ---
if 'language' not in st.session_state:
    st.session_state.language = 'en' # Default language

def get_text(key):
    """Retrieves the text string for the current language."""
    return TRANSLATIONS[st.session_state.language].get(key, f"_{key}_") # Fallback to key if not found

# --- Language Selector in Sidebar ---
st.sidebar.header(get_text("sidebar_nav_title"))
language_options = {'en': 'English', 'fr': 'Français', 'rw': 'Kinyarwanda'}
selected_lang_display = st.sidebar.selectbox(
    "Select Language | Hitamo Ururimi",
    options=list(language_options.keys()),
    format_func=lambda x: language_options[x],
    index=list(language_options.keys()).index(st.session_state.language),
    key="language_selector"
)
if selected_lang_display != st.session_state.language:
    st.session_state.language = selected_lang_display
    st.rerun() # Corrected: Use st.rerun() instead of st.experimental_rerun()

# --- Simplified Tax Rules (Re-define based on locale if needed, but for prototype, fixed) ---
# (The rates themselves usually don't change by language, only their explanation)
VAT_RATE = D('0.18')
TURNOVER_TAX_RATE = D('0.03')
CORPORATE_TAX_RATE = D('0.30')
PAYE_BANDS = [
    (D('0'), D('30000'), D('0.00')),
    (D('30001'), D('100000'), D('0.20')),
    (D('100001'), D('200000'), D('0.30')),
    (D('200001'), None, D('0.40'))
]
RSSB_EMPLOYEE_RATE = D('0.05')
RSSB_EMPLOYER_RATE = D('0.03')
RSSB_MAX_CONTRIBUTION_SALARY = D('1000000')

# --- Tax Calculation Function (No change to logic, just uses inputs) ---
def calculate_sme_taxes(business_data: dict) -> dict:
    """Calculates estimated taxes for an SME based on provided business data. (Simplified rules for prototyping)"""
    paye = D('0'); vat = D('0'); turnover_tax = D('0'); corporate_tax = D('0')
    rssb_employee_contribution = D('0'); rssb_employer_contribution = D('0'); total_rssb = D('0')

    turnover = D(str(business_data.get('turnover', 0.0)))
    vat_eligible_sales = D(str(business_data.get('vat_eligible_sales', 0.0)))
    total_expenses = D(str(business_data.get('total_expenses', 0.0)))
    salaries_paid_gross = D(str(business_data.get('salaries_paid_gross', 0.0)))
    is_vat_registered = business_data.get('is_vat_registered', False)
    is_small_business_for_turnover_tax = business_data.get('is_small_business_for_turnover_tax', True)
    number_of_employees = business_data.get('number_of_employees', 0)

    if is_vat_registered: vat = vat_eligible_sales * VAT_RATE
    else: vat = D('0')

    if not is_vat_registered and is_small_business_for_turnover_tax: turnover_tax = turnover * TURNOVER_TAX_RATE
    else: turnover_tax = D('0')

    if salaries_paid_gross > 0 and number_of_employees > 0:
        average_monthly_salary_per_employee = salaries_paid_gross / number_of_employees if number_of_employees > 0 else D('0')
        if average_monthly_salary_per_employee > 0:
            paye_calculated_for_one_employee_monthly = D('0')
            remaining_salary_for_paye = average_monthly_salary_per_employee
            for lower_bound, upper_bound, rate in PAYE_BANDS:
                if remaining_salary_for_paye <= D('0'): break
                current_band_upper = upper_bound if upper_bound is not None else remaining_salary_for_paye + D('1')
                band_range = current_band_upper - lower_bound + D('1')
                amount_in_band = min(remaining_salary_for_paye, band_range)
                if amount_in_band > D('0'):
                    paye_calculated_for_one_employee_monthly += (amount_in_band * rate)
                    remaining_salary_for_paye -= amount_in_band
            paye = paye_calculated_for_one_employee_monthly * number_of_employees
    else: paye = D('0')

    if salaries_paid_gross > 0 and number_of_employees > 0:
        capped_total_salary_for_rssb = min(salaries_paid_gross, RSSB_MAX_CONTRIBUTION_SALARY * number_of_employees)
        rssb_employee_contribution = capped_total_salary_for_rssb * RSSB_EMPLOYEE_RATE
        rssb_employer_contribution = capped_total_salary_for_rssb * RSSB_EMPLOYER_RATE
        total_rssb = rssb_employee_contribution + rssb_employer_contribution
    else: total_rssb = D('0')

    taxable_income = turnover - total_expenses
    if taxable_income > D('0') and business_data.get('business_type') == 'Formal (Registered)': corporate_tax = taxable_income * CORPORATE_TAX_RATE
    else: corporate_tax = D('0')

    total_tax_due = D('0')
    total_tax_due += vat
    total_tax_due += turnover_tax
    total_tax_due += paye
    total_tax_due += corporate_tax
    total_tax_due += total_rssb


    return {
        'paye_amount': paye.quantize(D('0.01')),
        'vat_amount': vat.quantize(D('0.01')),
        'turnover_tax_amount': turnover_tax.quantize(D('0.01')),
        'corporate_tax_amount': corporate_tax.quantize(D('0.01')),
        'rssb_employee_contribution': rssb_employee_contribution.quantize(D('0.01')),
        'rssb_employer_contribution': rssb_employer_contribution.quantize(D('0.01')),
        'rssb_total_contribution': total_rssb.quantize(D('0.01')),
        'total_tax_due': total_tax_due.quantize(D('0.01')),
        'notes': get_text("calc_notes")
    }

# --- Streamlit App Sections ---

# Sidebar Navigation (now uses translated strings)
page_options = {
    "Welcome": get_text("module_welcome"),
    "Onboarding & Profile": get_text("module_onboarding"),
    "Tax Calculator": get_text("module_calculator"),
    "Smart Dashboard": get_text("module_dashboard"),
    "Educational Guides": get_text("module_guides"),
    "Declaration & Reporting": get_text("module_reporting")
}

page = st.sidebar.radio(
    get_text("go_to"),
    options=list(page_options.keys()),
    format_func=lambda x: page_options[x]
)

# --- Welcome Page ---
if page == "Welcome":
    st.title(get_text("welcome_page_title"))
    st.markdown(get_text("welcome_page_desc"))
    st.markdown(get_text("modules_included"))
    st.markdown(f"""
        - **{get_text("module_onboarding")}**: {get_text("onboarding_desc_short")}
        - **{get_text("module_calculator")}**: {get_text("calculator_desc_short")}
        - **{get_text("module_dashboard")}**: {get_text("dashboard_desc_short")}
        - **{get_text("module_guides")}**: {get_text("guides_desc_short")}
        - **{get_text("module_reporting")}**: {get_text("reporting_desc_short")}
    """)
    st.markdown(get_text("welcome_disclaimer"))
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Flag_of_Rwanda.svg/1200px-Flag_of_Rwanda.svg.png", width=200) # Placeholder image
    st.info(get_text("welcome_start_info"))

# --- Onboarding & Business Profile Setup ---
elif page == "Onboarding & Profile":
    st.title(get_text("onboarding_title"))
    st.markdown(get_text("onboarding_desc"))

    with st.form("business_profile_form"):
        st.subheader(get_text("section_business_info"))
        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input(get_text("label_business_name"), "My Rwandan Enterprise")
            rra_tin = st.text_input(get_text("label_rra_tin"), "123456789", help=get_text("help_rra_tin"))
            business_type_options = get_text("options_business_entity_type")
            business_type = st.selectbox(get_text("label_business_entity_type"), business_type_options, help=get_text("help_business_entity_type"))
        with col2:
            sector_options = get_text("options_sector")
            sector = st.selectbox(get_text("label_sector"), sector_options, help=get_text("help_sector"))
            registration_date = st.date_input(get_text("label_registration_date"), value=date(2023, 1, 1))
            st.write("") # Spacer

        st.subheader(get_text("section_key_tax_questions"))
        col_tax1, col_tax2 = st.columns(2)
        with col_tax1:
            estimated_annual_turnover = st.number_input(
                get_text("label_estimated_annual_turnover"),
                min_value=0.0,
                value=5000000.0,
                step=100000.0,
                help=get_text("help_estimated_annual_turnover")
            )
            has_employees = st.checkbox(get_text("label_has_employees"), False, help=get_text("help_has_employees"))

        with col_tax2:
            is_vat_registered_onboard = st.checkbox(get_text("label_is_vat_registered_onboard"), False, help=get_text("help_is_vat_registered_onboard"))
            # Check for selected option across languages for informal business
            if any(bt in business_type for bt in ["Informal Business", "Ubucuruzi Butemewe", "Entreprise Informelle"]):
                st.info(get_text("info_informal_business"))


        st.subheader(get_text("section_contact_info"))
        col_contact1, col_contact2 = st.columns(2)
        with col_contact1:
            contact_person = st.text_input(get_text("label_contact_person"), "John Doe")
            phone_number = st.text_input(get_text("label_phone_number"), "+250 7XX XXX XXX")
        with col_contact2:
            email = st.text_input(get_text("label_email_address"), "contact@mybusiness.com")
            address = st.text_area(get_text("label_address"), "Kigali, Rwanda")

        submitted = st.form_submit_button(get_text("button_save_profile"))
        if submitted:
            st.success(get_text("success_profile_saved").format(business_name=business_name))
            st.markdown(get_text("header_estimated_obligations"))
            st.info(get_text("info_preliminary_assessment"))

            tax_obligations = []
            # Simplified logic for identifying obligations
            if estimated_annual_turnover >= D('20000000') or is_vat_registered_onboard:
                tax_obligations.append("VAT (Value Added Tax)")
            elif estimated_annual_turnover < D('20000000') and any(bt in business_type for bt in ["Informal Business", "Ubucuruzi Butemewe", "Entreprise Informelle"]):
                tax_obligations.append("Presumptive Tax (Simplified or Turnover Tax)")
            elif estimated_annual_turnover < D('50000000') and not is_vat_registered_onboard: # Example threshold for Turnover Tax
                tax_obligations.append("Turnover Tax") # Small businesses
            else:
                tax_obligations.append("Corporate Income Tax") # Default for formal if not turnover tax

            if has_employees:
                tax_obligations.append("PAYE (Pay As You Earn)")
                tax_obligations.append("RSSB (Rwanda Social Security Board) Contributions")
            else:
                st.write(get_text("no_paye_rssb_info"))

            if any(bt in business_type for bt in ["Formal (Registered)", "Company (Ltd)", "Société (Ltée)", "Koperative"]):
                 tax_obligations.append("Annual Corporate Income Tax (for formal businesses)")


            for tax in set(tax_obligations): # Use set to avoid duplicates
                st.write(f"- **{tax}**")

            st.write("---")
            st.markdown(get_text("what_s_next"))
            st.markdown(get_text("next_calc_guide"))
            st.markdown(get_text("next_explore_guides"))
            st.markdown(get_text("next_formalization"))
            st.info(get_text("data_stored_info"))

# --- User-Friendly Tax Calculator ---
elif page == "Tax Calculator":
    st.title(get_text("calculator_title"))
    st.markdown(get_text("calculator_desc"))

    st.subheader(get_text("section_business_period"))

    col1, col2 = st.columns(2)
    with col1:
        calc_business_type = st.selectbox(
            get_text("label_business_type_calc"),
            get_text("options_business_entity_type"), # Use full list of entity types
            key="calc_business_type",
            help=get_text("help_business_type_calc")
        )
        is_vat_registered = st.checkbox(get_text("label_is_vat_registered_calc"), False, key="calc_vat_registered", help=get_text("help_is_vat_registered_calc"))
        has_employees_calc = st.checkbox(get_text("label_has_employees_calc"), False, key="calc_has_employees", help=get_text("help_has_employees_calc"))
        if has_employees_calc:
            number_of_employees = st.number_input(get_text("label_num_employees"), min_value=0, value=1, step=1, key="num_employees")
        else:
            number_of_employees = 0

    with col2:
        is_small_business_for_turnover_tax = st.checkbox(
            get_text("label_is_small_business_for_turnover_tax"),
            True,
            key="calc_turnover_tax_eligible",
            help=get_text("help_is_small_business_for_turnover_tax")
        )
        st.markdown("---")
        st.write(get_text("header_reporting_period"))
        period_start = st.date_input(get_text("label_start_date"), value=date(2025, 1, 1), key="calc_start_date")
        period_end = st.date_input(get_text("label_end_date"), value=date(2025, 3, 31), key="calc_end_date")


    st.subheader(get_text("section_financial_inputs"))

    col3, col4 = st.columns(2)
    with col3:
        turnover = st.number_input(get_text("label_turnover"), min_value=0.0, value=1500000.0, step=10000.0, key="calc_turnover", help=get_text("help_turnover"))
        if is_vat_registered:
            vat_eligible_sales = st.number_input(get_text("label_vat_eligible_sales"), min_value=0.0, value=turnover, step=10000.0, key="calc_vat_sales", help=get_text("help_vat_eligible_sales"))
        else:
            vat_eligible_sales = D('0')

        total_expenses = st.number_input(get_text("label_total_expenses"), min_value=0.0, value=500000.0, step=10000.0, key="calc_expenses", help=get_text("help_total_expenses"))

    with col4:
        if has_employees_calc:
            salaries_paid_gross = st.number_input(get_text("label_salaries_paid_gross"), min_value=0.0, value=200000.0, step=10000.0, key="calc_salaries", help=get_text("help_salaries_paid_gross"))
        else:
            salaries_paid_gross = D('0')
        other_taxable_income = st.number_input(get_text("label_other_taxable_income"), min_value=0.0, value=0.0, step=1000.0, help=get_text("help_other_taxable_income"))
        depreciation_on_assets = st.number_input(get_text("label_depreciation_on_assets"), min_value=0.0, value=0.0, step=1000.0, help=get_text("help_depreciation_on_assets"))

    st.markdown("---")

    if st.button(get_text("button_calculate_taxes"), key="calc_button"):
        business_data_for_calc = {
            'business_type': calc_business_type,
            'sector': '', # Not used in prototype calculation
            'period_start_date': period_start,
            'period_end_date': period_end,
            'turnover': D(str(turnover)),
            'vat_eligible_sales': D(str(vat_eligible_sales)),
            'total_expenses': D(str(total_expenses + depreciation_on_assets)), # Add depreciation to expenses for calculation
            'salaries_paid_gross': D(str(salaries_paid_gross)),
            'is_vat_registered': is_vat_registered,
            'is_small_business_for_turnover_tax': is_small_business_for_turnover_tax,
            'number_of_employees': number_of_employees
        }

        calculated_results = calculate_sme_taxes(business_data_for_calc)

        st.subheader(get_text("section_estimated_results"))

        st.success(f"**{get_text('total_tax_due')} RWF {calculated_results['total_tax_due']:,}**")
        st.info(get_text("info_estimated_figures"))

        with st.expander(get_text("view_detailed_breakdown")):
            st.write("---")
            st.markdown(get_text("breakdown_by_tax_type"))
            st.write(f"**{get_text('paye_amount')}** RWF {calculated_results['paye_amount']:,}")
            st.write(f"**{get_text('vat_amount')}** RWF {calculated_results['vat_amount']:,}")
            st.write(f"**{get_text('turnover_tax_amount')}** RWF {calculated_results['turnover_tax_amount']:,}")
            st.write(f"**{get_text('corporate_tax_amount')}** RWF {calculated_results['corporate_tax_amount']:,}")
            st.write(f"**{get_text('rssb_total_contribution')}** RWF {calculated_results['rssb_total_contribution']:,} "
                     f"({get_text('rssb_employee_share')} {calculated_results['rssb_employee_contribution']:,}, {get_text('rssb_employer_share')} {calculated_results['rssb_employer_contribution']:,})")
            st.write("---")
            st.write(f"**{get_text('calc_notes')}**")

        st.subheader(get_text("section_required_documents"))
        st.markdown(get_text("documents_desc"))
        st.markdown(get_text("doc_all_taxes"))
        if calculated_results['vat_amount'] > 0: st.markdown(get_text("doc_vat"))
        if calculated_results['paye_amount'] > 0: st.markdown(get_text("doc_paye_rssb"))
        if calculated_results['corporate_tax_amount'] > 0: st.markdown(get_text("doc_corporate_tax"))
        if calculated_results['turnover_tax_amount'] > 0: st.markdown(get_text("doc_turnover_tax"))
        st.markdown(get_text("action_keep_records"))
        st.markdown("---")
        st.markdown(get_text("quick_links_info"))

        # Guide options for direct linking
        guide_link_base = "?page=Educational+Guides&guide="
        english_guide_keys = {
            "Understanding VAT in Rwanda": "guide_vat_title",
            "How to Calculate PAYE": "guide_paye_title",
            "SME Turnover Tax Explained": "guide_turnover_tax_title",
            "Corporate Tax Basics for Beginners": "guide_corporate_tax_title",
            "Rwanda Social Security Board (RSSB) Contributions": "guide_rssb_title",
            "Registering Your Business with RRA": "guide_registration_title"
        }

        # Dynamically create links using translated guide titles
        if calculated_results['vat_amount'] > 0:
            st.markdown(f"- [{get_text('guide_vat_title')}]({guide_link_base}Understanding+VAT+in+Rwanda)")
        if calculated_results['paye_amount'] > 0:
            st.markdown(f"- [{get_text('guide_paye_title')}]({guide_link_base}How+to+Calculate+PAYE)")
        if calculated_results['turnover_tax_amount'] > 0:
            st.markdown(f"- [{get_text('guide_turnover_tax_title')}]({guide_link_base}SME+Turnover+Tax+Explained)")
        if calculated_results['corporate_tax_amount'] > 0:
            st.markdown(f"- [{get_text('guide_corporate_tax_title')}]({guide_link_base}Corporate+Tax+Basics+for+Beginners)")
        st.markdown(f"- [{get_text('guide_rssb_title')}]({guide_link_base}Rwanda+Social+Security+Board+(RSSB)+Contributions)")
        st.markdown(f"- [{get_text('guide_registration_title')}]({guide_link_base}Registering+Your+Business+with+RRA)")


# --- Smart Dashboard ---
elif page == "Smart Dashboard":
    st.title(get_text("dashboard_title"))
    st.markdown(get_text("dashboard_desc"))

    st.subheader(get_text("overview_obligations"))
    col1, col2, col3 = st.columns(3)
    col1.metric(get_text("metric_upcoming_deadline"), "June 30, 2025", "VAT Declaration (Q2)")
    col2.metric(get_text("metric_last_filed_tax"), "RWF 150,000", "PAYE for May")
    col3.metric(get_text("metric_compliance_score"), "85%", "Good")

    st.subheader(get_text("header_compliance_calendar"))
    st.info(get_text("info_deadlines"))
    st.write("---")
    st.write(get_text("header_recent_declarations"))
    # Dummy data for demonstration (uses translated headers)
    data = {
        get_text('col_tax_type'): [get_text('guide_vat_title'), get_text('guide_paye_title'), get_text('guide_corporate_tax_title'), get_text('guide_turnover_tax_title')],
        get_text('col_period'): ['Q1 2025', 'May 2025', '2024 Annual', 'Q4 2024'],
        get_text('col_amount_paid'): [270000, 150000, 1200000, 24000],
        get_text('col_status'): [get_text('status_filed'), get_text('status_filed'), get_text('status_pending'), get_text('status_filed')],
        get_text('col_filing_date'): ['2025-04-20', '2025-06-15', '-', '2025-01-18'],
        get_text('col_receipt'): [get_text('receipt_view'), get_text('receipt_view'), get_text('receipt_na'), get_text('receipt_view')]
    }

    df = pd.DataFrame(data)
    st.dataframe(df.style.highlight_max(axis=0))

    st.subheader(get_text("header_alerts_reminders"))
    st.warning(get_text("alert_vat_due"))
    st.info(get_text("info_rssb_remitted"))
    st.warning(get_text("alert_corporate_tax_upcoming"))


# --- Educational Guides ---
elif page == "Educational Guides":
    st.title(get_text("guides_title"))
    st.markdown(get_text("guides_desc"))

    st.subheader(get_text("header_explore_guides"))
    guide_options = {
        get_text("guide_vat_title"): get_text("guide_vat_content"),
        get_text("guide_paye_title"): get_text("guide_paye_content"),
        get_text("guide_turnover_tax_title"): get_text("guide_turnover_tax_content"),
        get_text("guide_corporate_tax_title"): get_text("guide_corporate_tax_content"),
        get_text("guide_rssb_title"): get_text("guide_rssb_content"),
        get_text("guide_registration_title"): get_text("guide_registration_content")
    }

    # Get guide from URL parameter if available, otherwise default
    query_params = st.query_params
    # Mapping from English query parameter key to the translated display title
    english_key_to_translated_title = {
        "Understanding+VAT+in+Rwanda": get_text("guide_vat_title"),
        "How+to+Calculate+PAYE": get_text("guide_paye_title"),
        "SME+Turnover+Tax+Explained": get_text("guide_turnover_tax_title"),
        "Corporate+Tax+Basics+for+Beginners": get_text("guide_corporate_tax_title"),
        "Rwanda+Social+Security+Board+(RSSB)+Contributions": get_text("guide_rssb_title"),
        "Registering+Your+Business+with+RRA": get_text("guide_registration_title")
    }

    initial_guide_display_name = None
    query_guide_value = query_params.get("guide", [None])[0]
    if query_guide_value in english_key_to_translated_title:
        initial_guide_display_name = english_key_to_translated_title[query_guide_value]
    
    selectbox_options_display = list(guide_options.keys())
    initial_index = 0
    if initial_guide_display_name and initial_guide_display_name in selectbox_options_display:
        initial_index = selectbox_options_display.index(initial_guide_display_name)

    selected_guide_display = st.selectbox(get_text("guide_select_placeholder"), selectbox_options_display, index=initial_index)

    if selected_guide_display in guide_options:
        st.markdown(guide_options[selected_guide_display])
    else:
        st.info(get_text("info_guide_coming_soon"))

    st.markdown("---")
    st.write(get_text("link_rra_website"))


# --- Declaration & Reporting ---
elif page == "Declaration & Reporting":
    st.title(get_text("reporting_title"))
    st.markdown(get_text("reporting_desc"))

    st.subheader(get_text("section_generate_report"))
    st.info(get_text("info_auto_populate"))
    report_type_options = get_text("options_report_type")
    report_type = st.selectbox(get_text("label_report_type"), report_type_options)
    report_period = st.text_input(get_text("label_report_period"), "Q1 2025")
    st.markdown("---")

    if st.button(get_text("button_generate_report")):
        st.warning(get_text("warning_report_placeholder"))
        st.markdown(get_text("header_prototype_report").format(report_type=report_type, report_period=report_period))
        st.markdown(f"""
            * **{get_text('generated_on')}** {date.today()}
            * **{get_text('status')}** {get_text('status_draft')}
            ---
            **{get_text('key_figures')}**
            - {get_text('figure_sales')} RWF 5,000,000
            - {get_text('figure_expenses')} RWF 1,500,000
            - {get_text('figure_tax_due')} RWF 345,000 ({get_text('based_on_calculator')})
            {get_text('imagine_pdf')}
        """)
        st.download_button(
            label=get_text("download_prototype_report"),
            data=get_text("download_dummy_data"),
            file_name=f"{report_type.replace(' ', '_')}_{report_period.replace(' ', '')}_Prototype.pdf",
            mime="application/pdf"
        )
        st.info(get_text("info_review_report"))

    st.subheader(get_text("section_past_submissions"))
    st.markdown(get_text("desc_past_submissions"))
    # Dummy data for past submissions (uses translated headers)
    past_submissions_data = {
        get_text('col_report_type'): [get_text('guide_vat_title') + ' Q4 2024', get_text('guide_paye_title') + ' Dec 2024', get_text('guide_turnover_tax_title') + ' Q3 2024'],
        get_text('col_submission_date'): ['2025-01-20', '2025-01-15', '2024-10-22'],
        get_text('col_amount_paid'): [250000, 145000, 22000],
        get_text('col_status'): [get_text('status_submitted_paid'), get_text('status_submitted_paid'), get_text('status_submitted_paid')],
        get_text('col_receipt'): [get_text('receipt_download'), get_text('receipt_download'), get_text('receipt_download')]
    }

    df_past = pd.DataFrame(past_submissions_data)
    st.dataframe(df_past)

    st.markdown("---")
    st.info(get_text("info_rra_api_future"))


# --- About the App (Sidebar content) ---
st.sidebar.markdown("---")
st.sidebar.header(get_text("about_app_title"))
st.sidebar.markdown(get_text("about_app_desc"))
st.sidebar.info(get_text("developed_by"))
st.sidebar.markdown("---")
st.sidebar.caption(get_text("copyright"))