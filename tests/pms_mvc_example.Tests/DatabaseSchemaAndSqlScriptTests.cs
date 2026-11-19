using Xunit;

namespace pms_mvc_example.Tests
{
    public class DatabaseSchemaAndSqlScriptTests
    {
        [Fact]
        public void SqlScript_ContainsProductsTableCreation()
        {
            var possiblePaths = new[]
            {
                Path.Combine(AppContext.BaseDirectory, "../../../../sql_script.sql"),
                Path.Combine(AppContext.BaseDirectory, "../../../../sql_script.txt"),
                Path.Combine(Directory.GetCurrentDirectory(), "sql_script.sql"),
                Path.Combine(Directory.GetCurrentDirectory(), "sql_script.txt"),
                Path.Combine(Directory.GetCurrentDirectory(), "../../sql_script.sql"),
                Path.Combine(Directory.GetCurrentDirectory(), "../../sql_script.txt"),
                @"d:\ASE-2nd-Brain\Brain\Projects\lab9\sql_script.sql",
                @"d:\ASE-2nd-Brain\Brain\Projects\lab9\sql_script.txt"
            };

            var filePath = possiblePaths.FirstOrDefault(File.Exists);
            Assert.True(filePath != null, "sql_script.sql or sql_script.txt must exist in project root");

            var scriptContent = File.ReadAllText(filePath);

            Assert.Contains("CREATE TABLE", scriptContent, StringComparison.OrdinalIgnoreCase);
            Assert.Contains("products", scriptContent, StringComparison.OrdinalIgnoreCase);
            Assert.Contains("[Id]", scriptContent);
            Assert.Contains("[Title]", scriptContent);
            Assert.Contains("[description]", scriptContent);
            Assert.Contains("[image]", scriptContent);
            Assert.Contains("[price]", scriptContent);
            Assert.Contains("[quantity]", scriptContent);
            Assert.Contains("[status]", scriptContent);
        }
    }
}
