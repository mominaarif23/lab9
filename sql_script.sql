-- =========================================================================
-- SMT Lab 09: Product Management System (PMS) ASP.NET Core MVC with ADO.NET
-- Database Creation & Schema Definition Script
-- Target DBMS: Microsoft SQL Server (MSSQL / LocalDB)
-- =========================================================================

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'pmsdb')
BEGIN
    CREATE DATABASE [pmsdb];
END
GO

USE [pmsdb];
GO

-- -------------------------------------------------------------------------
-- Table: products
-- -------------------------------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'products')
BEGIN
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
END
GO

-- -------------------------------------------------------------------------
-- Seed Data: Sample Products for Verification & Catalog Browsing
-- -------------------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[products])
BEGIN
    INSERT INTO [dbo].[products] ([Title], [description], [image], [price], [quantity], [status])
    VALUES 
    ('Classic Denim Jacket', 'Premium indigo denim outerwear', 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=300', 4500, 15, 'Active'),
    ('Silk Evening Gown', 'Tailored elegant emerald gown', 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300', 12500, 8, 'Active'),
    ('Minimalist White Sneaker', 'Full-grain calfskin leather sneaker', 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300', 6200, 25, 'Active');
END
GO

SELECT * FROM [dbo].[products];
GO
