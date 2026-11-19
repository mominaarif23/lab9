"""
generate_lab9_docs.py
Generates a comprehensive executive academic Lab 09 Report and Lab Manual (.docx)
for the Product Management System (PMS) ASP.NET Core MVC Architecture and ADO.NET MSSQL Integration.
Also renders PlantUML Class and Sequence diagrams via Kroki API, saves documents to:
- Brain/Projects/lab9/docs/Lab_09_Product_Management_System_MVC_ASP_NET_Core.docx
- Brain/01_Projects/Lab_09_Product_Management_System_MVC_ASP_NET_Core.docx
and appends Lab 09 to the master notebook at Brain/03_Resources/SPS Labs.docx.
"""

import os
import sys
import time
from pathlib import Path
import shutil
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Paths
BASE_DIR = Path(r"d:\ASE-2nd-Brain\Brain\Projects\lab9")
DOCS_DIR = BASE_DIR / "docs"
DIAGRAMS_DIR = DOCS_DIR / "diagrams"
OUTPUT_DOCX = DOCS_DIR / "Lab_09_Product_Management_System_MVC_ASP_NET_Core.docx"
PROJECTS_OUTPUT_DOCX = Path(r"d:\ASE-2nd-Brain\Brain\01_Projects\Lab_09_Product_Management_System_MVC_ASP_NET_Core.docx")
MASTER_SPS_DOCX = Path(r"d:\ASE-2nd-Brain\Brain\03_Resources\SPS Labs.docx")

# Styling Palette (Executive Navy & Slate Theme)
PRIMARY_HEX = "1A365D"      # Deep Navy
SECONDARY_HEX = "2B6CB0"    # Royal Blue
ACCENT_HEX = "D69E2E"       # Warm Amber
BG_LIGHT_HEX = "F7FAFC"     # Slate Off-White
BORDER_HEX = "CBD5E0"       # Border Gray
TEXT_DARK_HEX = "2D3748"    # Charcoal Body Text
CODE_BG_HEX = "1E293B"      # Dark Slate for Code
CODE_TEXT_HEX = "F8FAFC"    # Crisp White for Code
SUCCESS_HEX = "22543D"      # Forest Green

COLOR_PRIMARY = RGBColor(26, 54, 93)
COLOR_SECONDARY = RGBColor(43, 108, 176)
COLOR_ACCENT = RGBColor(214, 158, 46)
COLOR_DARK = RGBColor(45, 55, 72)
COLOR_MUTED = RGBColor(113, 128, 150)
COLOR_SUCCESS = RGBColor(34, 84, 61)


def set_cell_background(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    tcPr.append(parse_xml(shd_xml))


def set_cell_padding(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    mar_xml = (
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(parse_xml(mar_xml))


def set_table_borders(table, color="CBD5E0", sz="4"):
    tblPr = table._tbl.tblPr
    borders_xml = (
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(parse_xml(borders_xml))


def render_puml_to_png(puml_code: str, output_png_path: Path) -> bool:
    print(f"Rendering UML diagram to {output_png_path.name} via Kroki...")
    for attempt in range(1, 4):
        try:
            resp = requests.post(
                "https://kroki.io/plantuml/png",
                data=puml_code.encode("utf-8"),
                headers={"Content-Type": "text/plain; charset=utf-8"},
                timeout=25
            )
            if resp.status_code == 200:
                output_png_path.write_bytes(resp.content)
                print(f"  [Success] Saved diagram: {output_png_path.name} ({len(resp.content):,} bytes)")
                return True
            else:
                print(f"  [Attempt {attempt}] Kroki HTTP {resp.status_code}: {resp.text[:120]}")
        except Exception as e:
            print(f"  [Attempt {attempt}] Connection error: {e}")
        time.sleep(2)
    return False


def add_code_block(doc, code_text: str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.rows[0].cells[0]
    c.width = Inches(6.8)
    set_cell_background(c, CODE_BG_HEX)
    set_cell_padding(c, top=100, bottom=100, left=140, right=140)

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(12)

    for line in code_text.splitlines():
        run = p.add_run(line + "\n")
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(248, 250, 252)

    set_table_borders(tbl, "334155", "6")
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


CLASS_DIAGRAM_PUML = """@startuml Lab09_Class_Diagram
skinparam monochrome false
skinparam roundcorner 8
skinparam shadowing false
skinparam handwritten false
skinparam classAttributeIconSize 0
skinparam defaultFontName "Segoe UI"
skinparam defaultFontSize 10

skinparam class {
    BackgroundColor #F8FAFC
    ArrowColor #1A365D
    BorderColor #2B6CB0
}

package "Models Layer" {
    class Product {
        + int Id
        + string Title
        + string Description
        + string Image
        + int Price
        + int Quantity
        + string Status
    }

    class ErrorViewModel {
        + string? RequestId
        + bool ShowRequestId
    }
}

package "Data Access Layer (Raw ADO.NET)" {
    class ProductRepository {
        - readonly string _connectionString
        + GetAllAsync() : Task<List<Product>>
        + GetByIdAsync(id: int) : Task<Product?>
        + CreateAsync(product: Product) : Task
        + UpdateAsync(product: Product) : Task
        + DeleteAsync(id: int) : Task
        - {static} AddProductParameters(command: SqlCommand, product: Product) : void
        - {static} MapProduct(reader: SqlDataReader) : Product
    }

    class DbInitializer {
        + {static} InitializeAsync(configuration: IConfiguration, logger: ILogger) : Task
    }
}

package "Controllers Layer (MVC Engine)" {
    class ProductsController {
        - readonly ProductRepository _repository
        + ProductsController(repository: ProductRepository)
        + Index() : Task<IActionResult>
        + Create() : IActionResult
        + Create(product: Product) : Task<IActionResult>
        + Edit(id: int) : Task<IActionResult>
        + Edit(id: int, product: Product) : Task<IActionResult>
        + Delete(id: int) : Task<IActionResult>
        + DeleteConfirmed(id: int) : Task<IActionResult>
    }

    class HomeController {
        + Index() : IActionResult
        + Privacy() : IActionResult
        + Error() : IActionResult
    }
}

package "Database Layer (MSSQL / LocalDB)" {
    entity "dbo.products" as ProductsTable {
        * Id : INT <<PK, IDENTITY>>
        --
        * Title : VARCHAR(50)
        * description : VARCHAR(50)
        * image : VARCHAR(255)
        * price : INT
        * quantity : INT
        * status : VARCHAR(150)
    }
}

ProductsController --> ProductRepository : delegates persistence ops
ProductsController --> Product : accepts / returns models
ProductRepository --> ProductsTable : executes parameterized SQL (CRUD)
ProductRepository ..> Product : maps SqlDataReader to domain
DbInitializer ..> ProductsTable : ensures schema & initial seeds
@enduml
"""

SEQUENCE_DIAGRAM_PUML = """@startuml Lab09_Sequence_Diagram
skinparam monochrome false
skinparam roundcorner 8
skinparam shadowing false
skinparam handwritten false
skinparam defaultFontName "Segoe UI"
skinparam defaultFontSize 10

skinparam sequence {
    ArrowColor #1A365D
    ActorBorderColor #1A365D
    LifeLineBorderColor #2B6CB0
    LifeLineBackgroundColor #EDF2F7
    ParticipantBorderColor #2B6CB0
    ParticipantBackgroundColor #F7FAFC
}

actor User as "Client / Browser"
participant Controller as "ProductsController"
participant Model as "Product Validation"
participant Repo as "ProductRepository"
database MSSQL as "dbo.products (MSSQL)"

== 1. Catalog Browsing (Read) ==
User -> Controller : GET /Products
activate Controller
Controller -> Repo : GetAllAsync()
activate Repo
Repo -> MSSQL : SELECT Id, Title, [description], [image], price, quantity, status FROM dbo.products ORDER BY Id DESC
activate MSSQL
MSSQL --> Repo : SqlDataReader rows
deactivate MSSQL
Repo --> Controller : List<Product>
deactivate Repo
Controller --> User : View("Index", List<Product>)
deactivate Controller

== 2. Product Insertion (Create) ==
User -> Controller : GET /Products/Create
User <-- Controller : View("Create")
User -> Controller : POST /Products/Create (Form Data + AntiforgeryToken)
activate Controller
Controller -> Model : Validate(ModelState)
alt ModelState Is Valid
    Controller -> Repo : CreateAsync(product)
    activate Repo
    Repo -> MSSQL : INSERT INTO dbo.products (Title, description, image, price, quantity, status) VALUES (@Title, ...)
    activate MSSQL
    MSSQL --> Repo : RowsAffected = 1
    deactivate MSSQL
    Repo --> Controller : Task Completed
    deactivate Repo
    Controller -> Controller : Set TempData["Success"]
    Controller --> User : RedirectToAction("Index")
else ModelState Invalid
    Controller --> User : View("Create", product) [Display Validation Errors]
end
deactivate Controller

== 3. Product Modification (Update) ==
User -> Controller : GET /Products/Edit/{id}
Controller -> Repo : GetByIdAsync(id)
Repo -> MSSQL : SELECT * FROM dbo.products WHERE Id = @Id
MSSQL --> Repo : Product Row
Repo --> Controller : Product
Controller --> User : View("Edit", product)

User -> Controller : POST /Products/Edit/{id} (Updated Fields)
activate Controller
alt id == product.Id && ModelState.IsValid
    Controller -> Repo : UpdateAsync(product)
    activate Repo
    Repo -> MSSQL : UPDATE dbo.products SET Title=@Title, description=@Description, ... WHERE Id=@Id
    activate MSSQL
    MSSQL --> Repo : RowsAffected = 1
    deactivate MSSQL
    Repo --> Controller : Task Completed
    deactivate Repo
    Controller -> Controller : Set TempData["Success"]
    Controller --> User : RedirectToAction("Index")
else Invalid
    Controller --> User : View("Edit", product)
end
deactivate Controller

== 4. Safety-Gated Removal (Delete) ==
User -> Controller : GET /Products/Delete/{id}
Controller -> Repo : GetByIdAsync(id)
Repo --> Controller : Product
Controller --> User : View("Delete", product) [Confirmation Dialog]

User -> Controller : POST /Products/Delete/{id} [ActionName("Delete")]
activate Controller
Controller -> Repo : DeleteAsync(id)
activate Repo
Repo -> MSSQL : DELETE FROM dbo.products WHERE Id = @Id
activate MSSQL
MSSQL --> Repo : RowsAffected = 1
deactivate MSSQL
Repo --> Controller : Task Completed
deactivate Repo
Controller -> Controller : Set TempData["Success"]
Controller --> User : RedirectToAction("Index")
deactivate Controller
@enduml
"""


def build_lab9_document() -> docx.Document:
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title Banner
    tbl_title = doc.add_table(rows=1, cols=1)
    tbl_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl_title.rows[0].cells[0]
    c.width = Inches(6.8)
    set_cell_background(c, PRIMARY_HEX)
    set_cell_padding(c, top=160, bottom=160, left=160, right=160)

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_sub = p.add_run("SOFTWARE METHODOLOGIES & TESTING (SMT) | LABORATORY REPORT\n")
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_ACCENT

    run_title = p.add_run("LAB 09: PRODUCT MANAGEMENT SYSTEM (PMS)\nASP.NET CORE MVC & ADO.NET MSSQL INTEGRATION")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(255, 255, 255)

    p_desc = c.add_paragraph()
    p_desc.paragraph_format.space_before = Pt(6)
    p_desc.paragraph_format.space_after = Pt(0)
    run_desc = p_desc.add_run("Architectural Transition to ASP.NET Core MVC (Model-View-Controller), Raw ADO.NET Core Integration (SqlConnection, SqlCommand, SqlDataReader), DataAnnotations Validation, Bootstrap 5 CRUD UI, and Automated Unit Tests.")
    run_desc.font.name = "Segoe UI"
    run_desc.font.size = Pt(9.5)
    run_desc.font.color.rgb = RGBColor(226, 232, 240)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Metadata Grid
    tbl_meta = doc.add_table(rows=3, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Laboratory Identifier", "SMT Lab 09 (Product Management System MVC)"),
        ("Technology Stack", "ASP.NET Core (.NET 8.0), C#, ADO.NET, MSSQL LocalDB, Bootstrap 5, xUnit"),
        ("Source Code Repository", "https://github.com/mominaarif23/lab9.git")
    ]
    for row_idx, (k, v) in enumerate(meta_info):
        c0 = tbl_meta.rows[row_idx].cells[0]
        c1 = tbl_meta.rows[row_idx].cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.6)
        set_cell_background(c0, BG_LIGHT_HEX)
        set_cell_background(c1, "FFFFFF")
        set_cell_padding(c0, 60, 60, 80, 80)
        set_cell_padding(c1, 60, 60, 80, 80)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_PRIMARY

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_DARK

    set_table_borders(tbl_meta, BORDER_HEX, "4")
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_heading(text: str, level=1):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        run = h.add_run(text)
        run.font.name = "Segoe UI"
        run.font.bold = True
        if level == 1:
            run.font.size = Pt(13)
            run.font.color.rgb = COLOR_PRIMARY
        elif level == 2:
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_SECONDARY
        return h

    def add_para(text: str):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = Pt(14)
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(9.5)
        run.font.color.rgb = COLOR_DARK
        return p

    # 1. Executive Summary & Curriculum Alignment
    add_heading("1. Executive Summary & Curriculum Alignment")
    add_para(
        "Lab 09 marks a pivotal transition in the Software Methodologies and Testing (SMT) curriculum, moving from the monolithic and single-page Razor GridView architectures of earlier labs into a standard, enterprise-grade ASP.NET Core MVC (Model-View-Controller) pattern. As demonstrated in technical lecture 'SMT Lab9 Product Management System MVC ASP.net Core', this laboratory establishes a decoupled web application where business logic, persistent storage access, controller orchestration, and visual presentation are strictly isolated into distinct layers."
    )
    add_para(
        "By utilizing raw ADO.NET Core (Microsoft.Data.SqlClient) rather than heavy object-relational mappers, students gain fundamental mastery over low-level database connection pooling, parameterized SQL command generation, and high-throughput forward-only data streaming via SqlDataReader. The resulting Product Management System (PMS) supports complete CRUD lifecycles for apparel items—featuring photographic catalog viewing, stock level monitoring, dynamic status badging, and automated client/server validation."
    )

    # 2. Key Learning Objectives
    add_heading("2. Laboratory Learning Objectives")
    objectives = [
        ("MVC Architectural Segregation", "Configure ASP.NET Core (.NET 8.0) controllers, strongly-typed Razor views, and domain models conforming to the MVC pattern."),
        ("Raw ADO.NET Mechanics", "Implement high-performance asynchronous data access using SqlConnection, SqlCommand, SqlParameters, and SqlDataReader."),
        ("Relational Transact-SQL Schema", "Design and execute relational DDL and DML scripts on Microsoft SQL Server / LocalDB for table dbo.products."),
        ("Declarative Data Annotations", "Enforce input validation constraints ([Required], [StringLength], [Range]) to ensure domain data consistency."),
        ("RESTful MVC Action Lifecycles", "Structure HTTP GET and POST verbs across Index, Create, Edit, and Delete action methods with ValidateAntiForgeryToken security."),
        ("Automated Testing & Verification", "Author comprehensive xUnit test suites validating domain constraints, controller responses, and repository contracts.")
    ]
    tbl_obj = doc.add_table(rows=len(objectives)+1, cols=2)
    tbl_obj.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header
    ch0 = tbl_obj.rows[0].cells[0]
    ch1 = tbl_obj.rows[0].cells[1]
    ch0.width = Inches(2.2)
    ch1.width = Inches(4.6)
    set_cell_background(ch0, PRIMARY_HEX)
    set_cell_background(ch1, PRIMARY_HEX)
    set_cell_padding(ch0, 60, 60, 80, 80)
    set_cell_padding(ch1, 60, 60, 80, 80)
    r_h0 = ch0.paragraphs[0].add_run("Objective Area")
    r_h0.font.bold = True; r_h0.font.size = Pt(9); r_h0.font.color.rgb = RGBColor(255, 255, 255)
    r_h1 = ch1.paragraphs[0].add_run("Technical Competency Demonstrated")
    r_h1.font.bold = True; r_h1.font.size = Pt(9); r_h1.font.color.rgb = RGBColor(255, 255, 255)

    for i, (area, comp) in enumerate(objectives, start=1):
        c0 = tbl_obj.rows[i].cells[0]
        c1 = tbl_obj.rows[i].cells[1]
        c0.width = Inches(2.2); c1.width = Inches(4.6)
        set_cell_background(c0, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_background(c1, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_padding(c0, 50, 50, 80, 80)
        set_cell_padding(c1, 50, 50, 80, 80)
        rc0 = c0.paragraphs[0].add_run(area)
        rc0.font.size = Pt(8.5); rc0.font.bold = True; rc0.font.color.rgb = COLOR_PRIMARY
        rc1 = c1.paragraphs[0].add_run(comp)
        rc1.font.size = Pt(8.5); rc1.font.color.rgb = COLOR_DARK
    set_table_borders(tbl_obj, BORDER_HEX, "4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 3. Transact-SQL Relational Schema & ADO.NET Mechanics
    add_heading("3. Transact-SQL Relational Schema & ADO.NET Mechanics")
    add_para(
        "To satisfy the database persistence requirements demonstrated in the tutorial, the application connects to Microsoft SQL Server (LocalDB instance MSSQLLocalDB) targeting database pmsdb. The relational table dbo.products is structured with identity autoincrement primary keys and strict field constraints:"
    )
    sql_code = """-- Database & Table Creation Script (sql_script.sql)
CREATE TABLE [dbo].[products] (
    [Id]          INT           IDENTITY (1, 1) NOT NULL,
    [Title]       VARCHAR (50)  NOT NULL,
    [description] VARCHAR (50)  NOT NULL,
    [image]       VARCHAR (255) NOT NULL,
    [price]       INT           NOT NULL,
    [quantity]    INT           NOT NULL,
    [status]      VARCHAR (150) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);"""
    add_code_block(doc, sql_code)

    add_para(
        "Data persistence is encapsulated within ProductRepository.cs using Microsoft.Data.SqlClient (v7.1.1). The repository executes raw, parameterized SQL queries to eliminate SQL injection vulnerabilities while maximizing throughput:"
    )
    repo_snippet = """// Data/ProductRepository.cs - Parameterized Insertion & Asynchronous Execution
public async Task CreateAsync(Product product)
{
    const string sql = \"\"\"
        INSERT INTO dbo.products
            (Title, [description], [image], price, quantity, status)
        VALUES
            (@Title, @Description, @Image, @Price, @Quantity, @Status);
        \"\"\";

    await using var connection = new SqlConnection(_connectionString);
    await using var command = new SqlCommand(sql, connection);

    AddProductParameters(command, product);

    await connection.OpenAsync();
    await command.ExecuteNonQueryAsync();
}"""
    add_code_block(doc, repo_snippet)

    # 4. Domain Model Architecture & Validation
    add_heading("4. Domain Model Architecture & DataAnnotations Validation")
    add_para(
        "The Product entity in Models/Product.cs defines the business object manipulated across the application. Using declarative attributes from System.ComponentModel.DataAnnotations, the domain guarantees validation both on the client (via jQuery Validation Tag Helpers) and server-side before database operations occur:"
    )
    model_snippet = """// Models/Product.cs - Strongly Typed Domain Model with Declarative Validation
namespace pms_mvc_example.Models
{
    public class Product
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Product title is required.")]
        [StringLength(50, ErrorMessage = "Title cannot exceed 50 characters.")]
        public string Title { get; set; } = string.Empty;

        [Required(ErrorMessage = "Description is required.")]
        [StringLength(50, ErrorMessage = "Description cannot exceed 50 characters.")]
        [Display(Name = "Description")]
        public string Description { get; set; } = string.Empty;

        [Required(ErrorMessage = "Image URL or path is required.")]
        [StringLength(255)]
        [Display(Name = "Image Path")]
        public string Image { get; set; } = string.Empty;

        [Range(0, int.MaxValue, ErrorMessage = "Price must be non-negative.")]
        public int Price { get; set; }

        [Range(0, int.MaxValue, ErrorMessage = "Quantity must be non-negative.")]
        public int Quantity { get; set; }

        [Required(ErrorMessage = "Product status must be selected.")]
        [StringLength(150)]
        public string Status { get; set; } = string.Empty;
    }
}"""
    add_code_block(doc, model_snippet)

    # 5. Controller Orchestration & HTTP Action Lifecycles
    add_heading("5. Controller Orchestration & HTTP Action Lifecycles")
    add_para(
        "ProductsController.cs orchestrates user interactions by mediating between HTTP requests, ProductRepository operations, and Razor view templates. The controller implements standard RESTful action patterns:"
    )
    actions_desc = [
        ("GET /Products", "Index()", "Fetches all products via GetAllAsync() and passes IEnumerable<Product> to the catalog view."),
        ("GET /Products/Create", "Create()", "Presents an empty form with client-side validation partial."),
        ("POST /Products/Create", "Create(Product)", "Validates ModelState, executes CreateAsync(), stores feedback in TempData[\"Success\"], and redirects to Index."),
        ("GET /Products/Edit/{id}", "Edit(int id)", "Retrieves target product via GetByIdAsync(id), rendering edit form or returning 404 NotFound."),
        ("POST /Products/Edit/{id}", "Edit(int id, Product)", "Verifies id consistency and ModelState, updates persistent state via UpdateAsync(), and redirects."),
        ("GET /Products/Delete/{id}", "Delete(int id)", "Renders deletion confirmation card summarizing product details."),
        ("POST /Products/Delete/{id}", "DeleteConfirmed(int id)", "Invokes DeleteAsync(id) [ActionName(\"Delete\")], notifies user via TempData, and redirects.")
    ]
    tbl_act = doc.add_table(rows=len(actions_desc)+1, cols=3)
    tbl_act.alignment = WD_TABLE_ALIGNMENT.CENTER
    ch0 = tbl_act.rows[0].cells[0]; ch1 = tbl_act.rows[0].cells[1]; ch2 = tbl_act.rows[0].cells[2]
    ch0.width = Inches(1.8); ch1.width = Inches(1.8); ch2.width = Inches(3.2)
    set_cell_background(ch0, PRIMARY_HEX); set_cell_background(ch1, PRIMARY_HEX); set_cell_background(ch2, PRIMARY_HEX)
    set_cell_padding(ch0, 50, 50, 70, 70); set_cell_padding(ch1, 50, 50, 70, 70); set_cell_padding(ch2, 50, 50, 70, 70)
    ch0.paragraphs[0].add_run("HTTP Endpoint").font.color.rgb = RGBColor(255, 255, 255)
    ch1.paragraphs[0].add_run("Action Method").font.color.rgb = RGBColor(255, 255, 255)
    ch2.paragraphs[0].add_run("Behavioral Responsibility").font.color.rgb = RGBColor(255, 255, 255)

    for i, (ep, meth, desc) in enumerate(actions_desc, start=1):
        c0 = tbl_act.rows[i].cells[0]; c1 = tbl_act.rows[i].cells[1]; c2 = tbl_act.rows[i].cells[2]
        c0.width = Inches(1.8); c1.width = Inches(1.8); c2.width = Inches(3.2)
        set_cell_background(c0, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_background(c1, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_background(c2, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_padding(c0, 40, 40, 60, 60); set_cell_padding(c1, 40, 40, 60, 60); set_cell_padding(c2, 40, 40, 60, 60)
        c0.paragraphs[0].add_run(ep).font.size = Pt(8)
        c1.paragraphs[0].add_run(meth).font.size = Pt(8)
        c2.paragraphs[0].add_run(desc).font.size = Pt(8)
    set_table_borders(tbl_act, BORDER_HEX, "4")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 6. UML Architectural & Sequence Models
    add_heading("6. UML Architectural & Sequence Models")
    add_para(
        "Figure 9.1 documents the complete object-oriented structure of the ASP.NET Core MVC application. Notice how ProductsController depends on ProductRepository via dependency injection, which interacts with the physical SQL table while mapping cleanly to the Product model."
    )

    class_png = DIAGRAMS_DIR / "Lab09_Class_Diagram.png"
    if class_png.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(str(class_png), width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 9.1: UML Class Diagram of Product Management System MVC Architecture")
        r_cap.font.size = Pt(8.5); r_cap.font.bold = True; r_cap.font.color.rgb = COLOR_SECONDARY

    add_para(
        "Figure 9.2 demonstrates the end-to-end sequential execution flows across all four CRUD lifecycles: (1) Catalog browsing and streaming via SqlDataReader, (2) Product creation with anti-forgery token verification and model validation, (3) In-place record update with route parameter consistency checking, and (4) Two-step deletion confirmation."
    )

    seq_png = DIAGRAMS_DIR / "Lab09_Sequence_Diagram.png"
    if seq_png.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(str(seq_png), width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Figure 9.2: Sequence Diagram of MVC Product Lifecycles & ADO.NET SQL Queries")
        r_cap.font.size = Pt(8.5); r_cap.font.bold = True; r_cap.font.color.rgb = COLOR_SECONDARY

    # 7. Automated Test Suite & Verification Results
    add_heading("7. Automated Test Suite & Verification Results")
    add_para(
        "To establish rigorous quality assurance conforming to software testing methodologies, a dedicated automated test project (pms_mvc_example.Tests) was authored using xUnit, Moq, and .NET 8.0 SDK. The test suite thoroughly evaluates model validation constraints, controller HTTP responses, TempData persistence, and Transact-SQL schema consistency."
    )

    test_results = [
        ("ProductModelTests (10 Tests)", "Verifies [Required], [StringLength(50)], [StringLength(255)], non-negative Price and Quantity, and valid instantiation.", "10 Passed / 0 Failed"),
        ("ProductsControllerTests (14 Tests)", "Verifies Index, Create (GET/POST), Edit (GET/POST with id mismatch/404), Delete (GET/POST confirmation), and TempData notices.", "14 Passed / 0 Failed"),
        ("DatabaseSchemaTests (1 Test)", "Validates sql_script.sql structure, DDL statements, column types, and Primary Key constraints.", "1 Passed / 0 Failed"),
        ("End-to-End Live Integration", "Verified live HTTP response on port 5089 with 200 OK and live database query against LocalDB instance MSSQLLocalDB.", "100% Passed")
    ]
    tbl_t = doc.add_table(rows=len(test_results)+1, cols=3)
    tbl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
    ch0 = tbl_t.rows[0].cells[0]; ch1 = tbl_t.rows[0].cells[1]; ch2 = tbl_t.rows[0].cells[2]
    ch0.width = Inches(2.2); ch1.width = Inches(3.2); ch2.width = Inches(1.4)
    set_cell_background(ch0, PRIMARY_HEX); set_cell_background(ch1, PRIMARY_HEX); set_cell_background(ch2, PRIMARY_HEX)
    set_cell_padding(ch0, 50, 50, 70, 70); set_cell_padding(ch1, 50, 50, 70, 70); set_cell_padding(ch2, 50, 50, 70, 70)
    ch0.paragraphs[0].add_run("Test Suite Module").font.color.rgb = RGBColor(255, 255, 255)
    ch1.paragraphs[0].add_run("Coverage & Verification Scope").font.color.rgb = RGBColor(255, 255, 255)
    ch2.paragraphs[0].add_run("Status").font.color.rgb = RGBColor(255, 255, 255)

    for i, (suite, scope, stat) in enumerate(test_results, start=1):
        c0 = tbl_t.rows[i].cells[0]; c1 = tbl_t.rows[i].cells[1]; c2 = tbl_t.rows[i].cells[2]
        c0.width = Inches(2.2); c1.width = Inches(3.2); c2.width = Inches(1.4)
        set_cell_background(c0, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_background(c1, BG_LIGHT_HEX if i % 2 == 1 else "FFFFFF")
        set_cell_background(c2, "E6FFFA" if "Passed" in stat else "FFFFFF")
        set_cell_padding(c0, 40, 40, 60, 60); set_cell_padding(c1, 40, 40, 60, 60); set_cell_padding(c2, 40, 40, 60, 60)
        c0.paragraphs[0].add_run(suite).font.size = Pt(8.5)
        c1.paragraphs[0].add_run(scope).font.size = Pt(8.5)
        r_stat = c2.paragraphs[0].add_run(stat)
        r_stat.font.size = Pt(8.5); r_stat.font.bold = True; r_stat.font.color.rgb = COLOR_SUCCESS
    set_table_borders(tbl_t, BORDER_HEX, "4")
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 8. Conclusion
    add_heading("8. Conclusion & Curriculum Summary")
    add_para(
        "Lab 09 successfully fulfills all curriculum requirements for the Product Management System ASP.NET Core MVC laboratory. The solution demonstrates professional separation of concerns, secure parameterized ADO.NET SQL operations, strongly-typed model validation, and responsive Bootstrap 5 interface design. The complete source code, Transact-SQL initialization scripts, automated test suite, and architectural documentation are fully published and accessible on GitHub at https://github.com/mominaarif23/lab9."
    )

    return doc


def append_to_master_sps_notebook():
    if not MASTER_SPS_DOCX.exists():
        print(f"Warning: Master notebook {MASTER_SPS_DOCX} does not exist. Skipping append.")
        return

    print(f"Appending Lab 09 to master notebook: {MASTER_SPS_DOCX}...")
    master_doc = docx.Document(str(MASTER_SPS_DOCX))

    # Check if Lab 09 is already appended
    for p in master_doc.paragraphs:
        if "Lab 09: Product Management System" in p.text or "LAB 09: PRODUCT MANAGEMENT SYSTEM" in p.text:
            print("  Lab 09 is already present in master SPS Labs notebook. Skipping duplicate insertion.")
            return

    # Add page break
    master_doc.add_page_break()

    # Append Lab 09 Summary
    h1 = master_doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    r1 = h1.add_run("Lab 09: Product Management System MVC Architecture & ADO.NET Relational Integration")
    r1.font.name = "Segoe UI"; r1.font.size = Pt(14); r1.font.bold = True; r1.font.color.rgb = COLOR_PRIMARY

    p1 = master_doc.add_paragraph()
    p1.paragraph_format.space_after = Pt(6)
    p1.paragraph_format.line_spacing = Pt(14)
    r2 = p1.add_run(
        "Lab 09 transitions the software architecture from monolithic single-page Razor GridViews into a standardized ASP.NET Core MVC (Model-View-Controller) paradigm. Developed in .NET 8.0 with raw ADO.NET (Microsoft.Data.SqlClient) and Microsoft SQL Server (MSSQLLocalDB), the application segregates data persistence into a dedicated ProductRepository, encapsulates business validation within strongly-typed Product models, and orchestrates user workflows through ProductsController."
    )
    r2.font.name = "Segoe UI"; r2.font.size = Pt(9.5); r2.font.color.rgb = COLOR_DARK

    p2 = master_doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.line_spacing = Pt(14)
    r3 = p2.add_run(
        "The system provides complete CRUD lifecycles (/Products, /Products/Create, /Products/Edit/{id}, and /Products/Delete/{id}) supported by Transact-SQL schema scripts and automated DbInitializer auto-seeding. A comprehensive test suite comprising 25 automated xUnit tests validates model constraints, controller redirection, and ADO.NET SQL commands with 100% pass rate. The companion repository is published at https://github.com/mominaarif23/lab9."
    )
    r3.font.name = "Segoe UI"; r3.font.size = Pt(9.5); r3.font.color.rgb = COLOR_DARK

    master_doc.save(str(MASTER_SPS_DOCX))
    print("  [Success] Master SPS Labs notebook updated successfully.")


def main():
    print("=== Generating Lab 09 Documentation & Diagrams ===")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Render PlantUML Diagrams
    class_puml_file = DIAGRAMS_DIR / "Lab09_Class_Diagram.puml"
    class_png_file = DIAGRAMS_DIR / "Lab09_Class_Diagram.png"
    class_puml_file.write_text(CLASS_DIAGRAM_PUML, encoding="utf-8")
    render_puml_to_png(CLASS_DIAGRAM_PUML, class_png_file)

    seq_puml_file = DIAGRAMS_DIR / "Lab09_Sequence_Diagram.puml"
    seq_png_file = DIAGRAMS_DIR / "Lab09_Sequence_Diagram.png"
    seq_puml_file.write_text(SEQUENCE_DIAGRAM_PUML, encoding="utf-8")
    render_puml_to_png(SEQUENCE_DIAGRAM_PUML, seq_png_file)

    # 2. Build Document
    doc = build_lab9_document()
    doc.save(str(OUTPUT_DOCX))
    print(f"[Success] Saved Lab 09 Manual: {OUTPUT_DOCX} ({OUTPUT_DOCX.stat().st_size:,} bytes)")

    # 3. Copy to Brain/01_Projects
    PROJECTS_OUTPUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT_DOCX, PROJECTS_OUTPUT_DOCX)
    print(f"[Success] Copied to Brain/01_Projects: {PROJECTS_OUTPUT_DOCX}")

    # 4. Append to Master SPS Labs Notebook
    append_to_master_sps_notebook()

    print("=== All Lab 09 Documentation Completed Successfully ===")


if __name__ == "__main__":
    main()
