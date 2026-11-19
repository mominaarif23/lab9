using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Moq;
using pms_mvc_example.Controllers;
using pms_mvc_example.Data;
using pms_mvc_example.Models;
using Xunit;

namespace pms_mvc_example.Tests
{
    public class ProductsControllerTests
    {
        private static ProductsController CreateControllerWithMockRepo(out Mock<ProductRepository> mockRepo)
        {
            mockRepo = new Mock<ProductRepository>();

            var httpContext = new DefaultHttpContext();
            var tempData = new TempDataDictionary(httpContext, Mock.Of<ITempDataProvider>());

            var controller = new ProductsController(mockRepo.Object)
            {
                TempData = tempData
            };

            return controller;
        }

        [Fact]
        public async Task Index_ReturnsViewResult_WithListOfProducts()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var testProducts = new List<Product>
            {
                new() { Id = 1, Title = "Product 1", Price = 100, Quantity = 2, Status = "Active" },
                new() { Id = 2, Title = "Product 2", Price = 200, Quantity = 5, Status = "Active" }
            };

            mockRepo.Setup(r => r.GetAllAsync()).ReturnsAsync(testProducts);

            // Act
            var result = await controller.Index();

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            var model = Assert.IsAssignableFrom<IEnumerable<Product>>(viewResult.Model);
            Assert.Equal(2, model.Count());
        }

        [Fact]
        public void Create_Get_ReturnsViewResult()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out _);

            // Act
            var result = controller.Create();

            // Assert
            Assert.IsType<ViewResult>(result);
        }

        [Fact]
        public async Task Create_Post_InvalidModelState_ReturnsViewWithProduct()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            controller.ModelState.AddModelError("Title", "Title is required");

            var invalidProduct = new Product { Price = 100 };

            // Act
            var result = await controller.Create(invalidProduct);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.Same(invalidProduct, viewResult.Model);
            mockRepo.Verify(r => r.CreateAsync(It.IsAny<Product>()), Times.Never);
        }

        [Fact]
        public async Task Create_Post_ValidModel_RedirectsToIndex_AndSetsTempData()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var validProduct = new Product
            {
                Id = 10,
                Title = "Silk Scarf",
                Description = "Floral printed silk scarf",
                Image = "/img/scarf.jpg",
                Price = 1500,
                Quantity = 20,
                Status = "Active"
            };

            mockRepo.Setup(r => r.CreateAsync(validProduct)).Returns(Task.CompletedTask);

            // Act
            var result = await controller.Create(validProduct);

            // Assert
            var redirectResult = Assert.IsType<RedirectToActionResult>(result);
            Assert.Equal(nameof(ProductsController.Index), redirectResult.ActionName);
            Assert.Equal("Product created successfully.", controller.TempData["Success"]);
            mockRepo.Verify(r => r.CreateAsync(validProduct), Times.Once);
        }

        [Fact]
        public async Task Edit_Get_ExistingId_ReturnsViewWithProduct()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var product = new Product { Id = 5, Title = "Leather Boots", Price = 8000, Quantity = 4, Status = "Active" };

            mockRepo.Setup(r => r.GetByIdAsync(5)).ReturnsAsync(product);

            // Act
            var result = await controller.Edit(5);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.Same(product, viewResult.Model);
        }

        [Fact]
        public async Task Edit_Get_NonExistingId_ReturnsNotFound()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            mockRepo.Setup(r => r.GetByIdAsync(999)).ReturnsAsync((Product?)null);

            // Act
            var result = await controller.Edit(999);

            // Assert
            Assert.IsType<NotFoundResult>(result);
        }

        [Fact]
        public async Task Edit_Post_IdMismatch_ReturnsBadRequest()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var product = new Product { Id = 10, Title = "Test Product" };

            // Act (route id is 5, but product.Id is 10)
            var result = await controller.Edit(5, product);

            // Assert
            Assert.IsType<BadRequestResult>(result);
            mockRepo.Verify(r => r.UpdateAsync(It.IsAny<Product>()), Times.Never);
        }

        [Fact]
        public async Task Edit_Post_InvalidModelState_ReturnsViewWithProduct()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            controller.ModelState.AddModelError("Price", "Invalid price");
            var product = new Product { Id = 7, Title = "Wool Sweater" };

            // Act
            var result = await controller.Edit(7, product);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.Same(product, viewResult.Model);
            mockRepo.Verify(r => r.UpdateAsync(It.IsAny<Product>()), Times.Never);
        }

        [Fact]
        public async Task Edit_Post_NonExistingProduct_ReturnsNotFound()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var product = new Product { Id = 42, Title = "Nonexistent" };
            mockRepo.Setup(r => r.GetByIdAsync(42)).ReturnsAsync((Product?)null);

            // Act
            var result = await controller.Edit(42, product);

            // Assert
            Assert.IsType<NotFoundResult>(result);
            mockRepo.Verify(r => r.UpdateAsync(It.IsAny<Product>()), Times.Never);
        }

        [Fact]
        public async Task Edit_Post_ValidProduct_UpdatesAndRedirectsToIndex()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var existing = new Product { Id = 12, Title = "Old Title" };
            var updated = new Product { Id = 12, Title = "New Title", Price = 250, Quantity = 10, Status = "Active" };

            mockRepo.Setup(r => r.GetByIdAsync(12)).ReturnsAsync(existing);
            mockRepo.Setup(r => r.UpdateAsync(updated)).Returns(Task.CompletedTask);

            // Act
            var result = await controller.Edit(12, updated);

            // Assert
            var redirectResult = Assert.IsType<RedirectToActionResult>(result);
            Assert.Equal(nameof(ProductsController.Index), redirectResult.ActionName);
            Assert.Equal("Product updated successfully.", controller.TempData["Success"]);
            mockRepo.Verify(r => r.UpdateAsync(updated), Times.Once);
        }

        [Fact]
        public async Task Delete_Get_ExistingId_ReturnsViewWithProduct()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var product = new Product { Id = 8, Title = "Cotton Tee", Status = "Active" };

            mockRepo.Setup(r => r.GetByIdAsync(8)).ReturnsAsync(product);

            // Act
            var result = await controller.Delete(8);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.Same(product, viewResult.Model);
        }

        [Fact]
        public async Task Delete_Get_NonExistingId_ReturnsNotFound()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            mockRepo.Setup(r => r.GetByIdAsync(404)).ReturnsAsync((Product?)null);

            // Act
            var result = await controller.Delete(404);

            // Assert
            Assert.IsType<NotFoundResult>(result);
        }

        [Fact]
        public async Task DeleteConfirmed_Post_ExistingId_DeletesAndRedirectsToIndex()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            var existing = new Product { Id = 15, Title = "Linen Trousers" };

            mockRepo.Setup(r => r.GetByIdAsync(15)).ReturnsAsync(existing);
            mockRepo.Setup(r => r.DeleteAsync(15)).Returns(Task.CompletedTask);

            // Act
            var result = await controller.DeleteConfirmed(15);

            // Assert
            var redirectResult = Assert.IsType<RedirectToActionResult>(result);
            Assert.Equal(nameof(ProductsController.Index), redirectResult.ActionName);
            Assert.Equal("Product deleted successfully.", controller.TempData["Success"]);
            mockRepo.Verify(r => r.DeleteAsync(15), Times.Once);
        }

        [Fact]
        public async Task DeleteConfirmed_Post_NonExistingId_ReturnsNotFound()
        {
            // Arrange
            var controller = CreateControllerWithMockRepo(out var mockRepo);
            mockRepo.Setup(r => r.GetByIdAsync(999)).ReturnsAsync((Product?)null);

            // Act
            var result = await controller.DeleteConfirmed(999);

            // Assert
            Assert.IsType<NotFoundResult>(result);
            mockRepo.Verify(r => r.DeleteAsync(It.IsAny<int>()), Times.Never);
        }
    }
}
