using System;
using System.Collections.Generic;

namespace Tabler.Docs.Data
{
    public static class SampleData
    {
        public static List<Order> GeneratedOrders(int count)
        {
            var rnd = new Random();
            var orders = new List<Order>();
            var customer = new Customer("Ani Vent");

            for (int i = 1; i <= count; i++)
            {
                orders.Add(new Order
                {
                    Customer = customer,
                    Country = "Sweden",
                    OrderDate = DateTimeOffset.Now.AddDays(-12),
                    GrossValue = rnd.Next(2000, 50000),
                    DiscountPercentage = rnd.Next(10, 50),
                    OrderType = (OrderType)rnd.Next(0, 4)
                });
            }

            return orders;
        }

        public static List<Customer> GetCustomers()
        {
            return new List<Customer>
            {
                new Customer { CustomerName = "Odio Corporation", Percentage = 30, Visits = 5402 },
                new Customer { CustomerName = "Nascetur AB", Percentage = 15, Visits = 1134 },
                new Customer { CustomerName = "Justo Eu Institute", Percentage = 23, Visits = 26431 },
                new Customer { CustomerName = "Ani Vent", Percentage = 88, Visits = 97654 },
                new Customer { CustomerName = "Cali Inc", Percentage = 77, Visits = 43543 },
                new Customer { CustomerName = "Kalle Anka", Percentage = 77, Visits = 43543 },
                new Customer { CustomerName = "Anna Anka", Percentage = 77, Visits = 43543 }
            };
        }

        public static List<Order> GetOrders()
        {
            var odio = new Customer("Odio Corporation");
            var nascetur = new Customer("Nascetur AB");
            var justo = new Customer("Justo Eu Institute");
            var ani = new Customer("Ani Vent");
            var cali = new Customer("Cali Inc");

            var orders = new List<Order>();

            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-1),
                GrossValue = 23456,
                DiscountPercentage = 18,
                OrderType = OrderType.Web
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = odio,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-1),
                GrossValue = 12345,
                DiscountPercentage = 11,
                OrderType = OrderType.Contract
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-7),
                GrossValue = 1456,
                DiscountPercentage = 24,
                OrderType = OrderType.Contract
            });


            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = ani,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-12),
                GrossValue = 34531,
                DiscountPercentage = 21,
                OrderType = OrderType.Contract
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = odio,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-100),
                GrossValue = 2800,
                DiscountPercentage = 12,
                OrderType = OrderType.Mail
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = odio,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-128),
                GrossValue = 12532,
                DiscountPercentage = 24,
                OrderType = OrderType.Contract
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.OnHold,
                Customer = odio,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-232),
                GrossValue = 1400,
                DiscountPercentage = 12,
                OrderType = OrderType.Mail
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = odio,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-321),
                GrossValue = 22000,
                DiscountPercentage = 10,
                OrderType = OrderType.Contract
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Cancelled,
                Customer = odio,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-400),
                GrossValue = 3000,
                DiscountPercentage = 17,
                OrderType = OrderType.Web
            });

            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-17),
                GrossValue = 2134,
                DiscountPercentage = 10,
                OrderType = OrderType.Phone
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-27),
                GrossValue = 11345,
                DiscountPercentage = 12,
                OrderType = OrderType.Phone,
                OrderExternalId = Guid.Parse("D8F8F68F-AD6B-4D94-8F2F-A7D31BC36CFB")
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-124),
                GrossValue = 63400,
                DiscountPercentage = 32,
                OrderType = OrderType.Mail
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Cancelled,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-299),
                GrossValue = 1235,
                DiscountPercentage = 12,
                OrderType = OrderType.Mail,
                OrderExternalId = Guid.Parse("D8F8F68F-AD6B-4D94-8F2F-A7D31BC36CFB")
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Cancelled,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-372),
                GrossValue = 44000,
                DiscountPercentage = 11,
                OrderType = OrderType.Phone
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = nascetur,
                Country = "Sweden",
                OrderDate = DateTimeOffset.Now.AddDays(-410),
                GrossValue = 17000,
                DiscountPercentage = 5,
                OrderType = OrderType.Phone
            });

            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = justo,
                Country = "Spain",
                OrderDate = DateTimeOffset.Now.AddDays(-13),
                GrossValue = 2800,
                DiscountPercentage = 12,
                OrderType = OrderType.Mail,
                OrderExternalId = Guid.Parse("6DF56C0E-9BF6-467B-B416-47B8CA52D9F5")
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = ani,
                Country = "Spain",
                OrderDate = DateTimeOffset.Now.AddDays(-45),
                GrossValue = 12532,
                DiscountPercentage = 24,
                OrderType = OrderType.Web
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = justo,
                Country = "Spain",
                OrderDate = DateTimeOffset.Now.AddDays(-60),
                GrossValue = 1400,
                DiscountPercentage = 12,
                OrderType = OrderType.Mail
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = justo,
                Country = "Spain",
                OrderDate = DateTimeOffset.Now.AddDays(-150),
                GrossValue = 22000,
                DiscountPercentage = 10,
                OrderType = OrderType.Web,
                OrderExternalId = Guid.Parse("73A179F4-175B-40C7-BD3D-F394A9B1FCF5")
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = justo,
                Country = "Spain",
                OrderDate = DateTimeOffset.Now.AddDays(-200),
                GrossValue = 3000,
                DiscountPercentage = 17,
                OrderType = OrderType.Web
            });

            orders.Add(new Order
            {
                OrderStatus = OrderStatus.OnHold,
                Customer = ani,
                Country = "France",
                OrderDate = DateTimeOffset.Now.AddDays(-17),
                GrossValue = 2134,
                DiscountPercentage = 10,
                OrderType = OrderType.Phone
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = ani,
                Country = "France",
                OrderDate = DateTimeOffset.Now.AddDays(-27),
                GrossValue = 11345,
                DiscountPercentage = 12,
                OrderType = OrderType.Phone
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = ani,
                Country = "France",
                OrderDate = DateTimeOffset.Now.AddDays(-124),
                GrossValue = 17002,
                DiscountPercentage = 32,
                OrderType = OrderType.Mail
            });

            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = cali,
                Country = "France",
                OrderDate = DateTimeOffset.Now.AddDays(-10),
                GrossValue = 77000,
                DiscountPercentage = 17,
                OrderType = OrderType.Web
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Shipped,
                Customer = cali,
                Country = "France",
                OrderDate = DateTimeOffset.Now.AddDays(-110),
                GrossValue = 120000,
                DiscountPercentage = 23,
                OrderType = OrderType.Web
            });
            orders.Add(new Order
            {
                OrderStatus = OrderStatus.Active,
                Customer = cali,
                Country = "France",
                OrderDate = DateTimeOffset.Now.AddDays(-243),
                GrossValue = 44000,
                DiscountPercentage = 8,
                OrderType = OrderType.Web
            });

            return orders;
        }
    }
}
