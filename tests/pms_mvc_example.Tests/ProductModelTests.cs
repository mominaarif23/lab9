using System.ComponentModel.DataAnnotations;
using pms_mvc_example.Models;
using Xunit;

namespace pms_mvc_example.Tests
{
    public class ProductModelTests
    {
        private static IList<ValidationResult> ValidateModel(object model)
        {
            var results = new List<ValidationResult>();
            var context = new ValidationContext(model, serviceProvider: null, items: null);
            Validator.TryValidateObject(model, context, results, validateAllProperties: true);
            return results;
        }

        [Fact]
        public void Product_WithValidAttributes_PassesValidation()
        {
            // Arrange
            var product = new Product
            {
                Id = 1,
                Title = "Tailored Denim Jacket",
                Description = "High quality denim jacket for everyday wear",
                Image = "https://example.com/images/jacket.jpg",
                Price = 4500,
                Quantity = 12,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Empty(validationResults);
        }

        [Fact]
        public void Product_MissingTitle_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "", // Required
                Description = "A product description",
                Image = "/img/prod.png",
                Price = 100,
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Title)));
        }

        [Fact]
        public void Product_TitleExceeding50Chars_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = new string('A', 51), // Max length is 50
                Description = "Valid Description",
                Image = "/img/test.png",
                Price = 100,
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Title)));
        }

        [Fact]
        public void Product_MissingDescription_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = "", // Required
                Image = "/img/prod.png",
                Price = 100,
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Description)));
        }

        [Fact]
        public void Product_DescriptionExceeding50Chars_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = new string('D', 51), // Max length is 50
                Image = "/img/prod.png",
                Price = 100,
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Description)));
        }

        [Fact]
        public void Product_MissingImage_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = "Valid Description",
                Image = "", // Required
                Price = 100,
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Image)));
        }

        [Fact]
        public void Product_ImageExceeding255Chars_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = "Valid Description",
                Image = new string('i', 256), // Max length is 255
                Price = 100,
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Image)));
        }

        [Fact]
        public void Product_NegativePrice_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = "Valid Description",
                Image = "/img/prod.png",
                Price = -10, // Must be >= 0
                Quantity = 5,
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Price)));
        }

        [Fact]
        public void Product_NegativeQuantity_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = "Valid Description",
                Image = "/img/prod.png",
                Price = 100,
                Quantity = -5, // Must be >= 0
                Status = "Active"
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Quantity)));
        }

        [Fact]
        public void Product_MissingStatus_FailsValidation()
        {
            // Arrange
            var product = new Product
            {
                Title = "Valid Title",
                Description = "Valid Description",
                Image = "/img/prod.png",
                Price = 100,
                Quantity = 5,
                Status = "" // Required
            };

            // Act
            var validationResults = ValidateModel(product);

            // Assert
            Assert.Contains(validationResults, v => v.MemberNames.Contains(nameof(Product.Status)));
        }
    }
}
