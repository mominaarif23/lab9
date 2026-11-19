using Microsoft.Data.SqlClient;

namespace pms_mvc_example.Data
{
    public static class DbInitializer
    {
        public static async Task InitializeAsync(IConfiguration configuration, ILogger logger)
        {
            var connectionString = configuration.GetConnectionString("DefaultConnection");
            if (string.IsNullOrWhiteSpace(connectionString))
            {
                logger.LogWarning("No DefaultConnection string configured for database initialization.");
                return;
            }

            try
            {
                var builder = new SqlConnectionStringBuilder(connectionString);
                var targetDb = builder.InitialCatalog;

                // Ensure target database exists by connecting to master
                builder.InitialCatalog = "master";
                await using (var masterConn = new SqlConnection(builder.ConnectionString))
                {
                    await masterConn.OpenAsync();
                    var checkDbSql = $"""
                        IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{targetDb}')
                        BEGIN
                            CREATE DATABASE [{targetDb}];
                        END
                        """;
                    await using var checkDbCmd = new SqlCommand(checkDbSql, masterConn);
                    await checkDbCmd.ExecuteNonQueryAsync();
                }

                // Connect to target database and ensure products table and seed data exist
                await using (var conn = new SqlConnection(connectionString))
                {
                    await conn.OpenAsync();

                    const string createTableSql = """
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

                            INSERT INTO [dbo].[products] ([Title], [description], [image], [price], [quantity], [status])
                            VALUES 
                            ('Classic Denim Jacket', 'Premium indigo denim outerwear', 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=300', 4500, 15, 'Active'),
                            ('Silk Evening Gown', 'Tailored elegant emerald gown', 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300', 12500, 8, 'Active'),
                            ('Minimalist White Sneaker', 'Full-grain calfskin leather sneaker', 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300', 6200, 25, 'Active');
                        END
                        """;

                    await using var tableCmd = new SqlCommand(createTableSql, conn);
                    await tableCmd.ExecuteNonQueryAsync();
                }

                logger.LogInformation("Database and products table initialization verified successfully.");
            }
            catch (Exception ex)
            {
                logger.LogWarning(ex, "DbInitializer non-blocking notice: Ensure SQL Server LocalDB is running if testing database features locally.");
            }
        }
    }
}
