# SMT Lab 09: Product Management System (PMS) ASP.NET Core MVC

> Enterprise-grade ASP.NET Core MVC web application with raw ADO.NET data persistence, Microsoft SQL Server relational integration, declarative validation, Bootstrap 5 UI, and 25 automated xUnit tests.

---

## 📌 Project Overview

**SMT Lab 09** advances web engineering capabilities from single-page in-line GridView operations into a modular **ASP.NET Core MVC (Model-View-Controller)** architecture. Built on **.NET 8.0**, this system manages apparel and product inventories through structured CRUD lifecycles backed by low-level, high-throughput **raw ADO.NET (`Microsoft.Data.SqlClient`)** parameterized database queries against **Microsoft SQL Server (MSSQL / LocalDB)**.

### Architectural Highlights
- **Decoupled 3-Tier Pattern**: Strict separation between data access (`ProductRepository`), presentation (`Razor Views`), domain validation (`Product`), and request coordination (`ProductsController`).
- **Raw ADO.NET Core Engine**: Direct connection lifecycle handling (`SqlConnection`), parameterized queries (`SqlCommand`), and forward-only sequential streaming (`SqlDataReader`).
- **Declarative Domain Integrity**: Data annotations (`[Required]`, `[StringLength]`, `[Range]`) ensuring cross-tier validation consistency across client and server.
- **Zero-Friction Startup (`DbInitializer`)**: Automatic database detection, table verification, and sample seed initialization upon application startup.
- **Automated Verification**: Complete xUnit test suite (25 tests) verifying model rules, controller actions, and database schemas with 100% pass rate.

---

## 🏗 System Architecture & Class Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Browser                        │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP (GET / POST)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Controllers Layer (ASP.NET Core MVC)           │
│   - ProductsController (Index, Create, Edit, Delete)        │
│   - HomeController (Index, Privacy, Error)                  │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               │ Passes Model to View         │ Delegates Data Operations
               ▼                              ▼
┌──────────────────────────────┐ ┌────────────────────────────┐
│      Views (Razor / HTML5)   │ │  Data Access Layer         │
│   - Products/Index.cshtml    │ │   - ProductRepository      │
│   - Products/Create.cshtml   │ │   - DbInitializer          │
│   - Products/Edit.cshtml     │ └──────────────┬─────────────┘
│   - Products/Delete.cshtml   │                │
└──────────────────────────────┘                │ Parameterized SQL
                                                ▼
                                 ┌────────────────────────────┐
                                 │ Database Layer (MSSQL)     │
                                 │   - Table: dbo.products    │
                                 └────────────────────────────┘
```

---

## 💾 Relational Database Schema (`dbo.products`)

The application persists records into Microsoft SQL Server database `pmsdb` (or `Lab9_ProductDB`). The table is defined in [`sql_script.sql`](file:///d:/ASE-2nd-Brain/Brain/Projects/lab9/sql_script.sql):

```sql
CREATE TABLE [dbo].[products] (
    [Id]          INT           IDENTITY (1, 1) NOT NULL,
    [Title]       VARCHAR (50)  NOT NULL,
    [description] VARCHAR (50)  NOT NULL,
    [image]       VARCHAR (255) NOT NULL,
    [price]       INT           NOT NULL,
    [quantity]    INT           NOT NULL,
    [status]      VARCHAR (150) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);
```

### Initial Seed Records
- **Classic Denim Jacket** (Price: 4,500, Qty: 15, Status: Active)
- **Silk Evening Gown** (Price: 12,500, Qty: 8, Status: Active)
- **Minimalist White Sneaker** (Price: 6,200, Qty: 25, Status: Active)

---

## 🌐 Endpoints & Controller Actions

| Route | HTTP Verb | Action Method | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | `Home.Index()` | System dashboard hero with direct links to management consoles |
| `/Products` | `GET` | `Products.Index()` | Displays the full product catalog table with thumbnail images and action buttons |
| `/Products/Create` | `GET` | `Products.Create()` | Renders the product creation form with client-side validation |
| `/Products/Create` | `POST` | `Products.Create(Product)` | Validates model state, inserts record via ADO.NET, and redirects to catalog |
| `/Products/Edit/{id}` | `GET` | `Products.Edit(int id)` | Pre-loads existing product specifications into editable form |
| `/Products/Edit/{id}` | `POST` | `Products.Edit(int id, Product)` | Enforces route consistency and updates record in SQL database |
| `/Products/Delete/{id}` | `GET` | `Products.Delete(int id)` | Displays safety confirmation view summarizing item details |
| `/Products/Delete/{id}` | `POST` | `Products.DeleteConfirmed(int id)` | Permanently removes record from database with `[ActionName("Delete")]` |

---

## 🧪 Automated Testing Suite (`tests/pms_mvc_example.Tests`)

The test suite validates the system using **xUnit** and **Moq**:

1. **`ProductModelTests` (10 Tests)**:
   - Evaluates `[Required]` validation on Title, Description, Image, and Status.
   - Verifies character string bounds (`[StringLength(50)]`, `[StringLength(255)]`).
   - Ensures non-negative numeric constraints on Price and Quantity.
2. **`ProductsControllerTests` (14 Tests)**:
   - `Index` returns view with enumerable product list.
   - `Create` GET and POST flows with valid and invalid model states.
   - `Edit` GET and POST flows with mismatch detection and 404 handling.
   - `Delete` GET and POST confirmation with redirection and TempData alerts.
3. **`DatabaseSchemaAndSqlScriptTests` (1 Test)**:
   - Validates that `sql_script.sql` contains correct table definitions and primary key constraints.

### Test Execution
```bash
dotnet test Lab9.slnx
```
```
Passed!  - Failed: 0, Passed: 25, Skipped: 0, Total: 25
```

---

## 🚀 Getting Started & Execution Runbook

### Prerequisites
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later
- [Microsoft SQL Server LocalDB](https://learn.microsoft.com/sql/database-engine/configure-windows/sql-server-express-localdb) (`(localdb)\MSSQLLocalDB`)

### 1. Clone the Repository
```bash
git clone https://github.com/mominaarif23/lab9.git
cd lab9
```

### 2. Configure Database Connection (Optional)
The connection string is preset in `Lab9/appsettings.json`:
```json
"ConnectionStrings": {
  "DefaultConnection": "Data Source=(LocalDB)\\MSSQLLocalDB;Initial Catalog=pmsdb;Integrated Security=True;Pooling=False;Encrypt=True;Trust Server Certificate=True"
}
```
*Note: `DbInitializer` will automatically create the database and seed the products table on your first run.*

### 3. Run the Application
```bash
dotnet run --project Lab9/pms_mvc_example.csproj
```
Open your browser and navigate to:
```
http://localhost:5000/Products
```

---

## 📄 Deliverables & Laboratory Manual

- **Formal Lab 09 Manual (.docx)**: [`docs/Lab_09_Product_Management_System_MVC_ASP_NET_Core.docx`](file:///d:/ASE-2nd-Brain/Brain/Projects/lab9/docs/Lab_09_Product_Management_System_MVC_ASP_NET_Core.docx)
- **High-Resolution UML Class Diagram**: [`docs/diagrams/Lab09_Class_Diagram.png`](file:///d:/ASE-2nd-Brain/Brain/Projects/lab9/docs/diagrams/Lab09_Class_Diagram.png)
- **High-Resolution Sequence Diagram**: [`docs/diagrams/Lab09_Sequence_Diagram.png`](file:///d:/ASE-2nd-Brain/Brain/Projects/lab9/docs/diagrams/Lab09_Sequence_Diagram.png)
- **Transact-SQL Initialization Script**: [`sql_script.sql`](file:///d:/ASE-2nd-Brain/Brain/Projects/lab9/sql_script.sql)

---

## 📜 License
Academic and open-source demonstration under the MIT License.
