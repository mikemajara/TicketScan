using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Threading.Tasks;
using TicketScan.Models;

namespace TicketScan.Services
{
    public class MockDataStore : IDataStore<Item>
    {
        List<Item> items;
        List<Product> products;
        CultureInfo culture = CultureInfo.CreateSpecificCulture("es-ES");


        public MockDataStore()
        {
            items = new List<Item>();
            products = new List<Product>
            {
                new Product
                {
                    Id = Guid.NewGuid().ToString(),
                    Text = "B, ALMENDRA S/A",
                    Price = 8.40,
                    Description = "Almendra de la buena, pelá y escupía"
                },
                new Product
                {
                    Id = Guid.NewGuid().ToString(),
                    Text = "L SEMI S/LACTO",
                    Price = 4.50,
                    Description = "Leche de dudosa procedencia"
                },
                new Product
                {
                    Id = Guid.NewGuid().ToString(),
                    Text = "PEPINO",
                    Price = 1.89,
                    Description = "Pepino que no cabe ni en chumino"
                }
            };
            var mockItems = new List<Item>
            {
                new Ticket {
                    Id = Guid.NewGuid().ToString(),
                    Company = "MERCADONA S.A.",
                    Address = "C/ MAYOR, 7 - ESPINARDO",
                    Location = "MURCIA",
                    Telephone = "968280708",
                    TaxNumber = "A46103834",
                    DateTime = DateTime.Parse("07/03/2019 19:51", culture),
                    OpNumber = "105936",
                    ReceiptNumber = "2308-011-043010",
                    Lines = new List<Line>
                    {
                        new Line
                        {
                            Id = Guid.NewGuid().ToString(),
                            Units = 1,
                            Item = products[0],
                        },
                        new Line
                        {
                            Id = Guid.NewGuid().ToString(),
                            Units = 4,
                            Item = products[1],
                        },
                    },
                    Price = 100.0
                },
                new Ticket {
                    Id = Guid.NewGuid().ToString(),
                    Company = "CARREFOUR S.A.",
                    Address = "A/ MIGUEL DE CERVANTES, 1",
                    Location = "MURCIA",
                    Telephone = "968280708",
                    TaxNumber = "A46103834",
                    DateTime = DateTime.Parse("07/03/2019 19:51", culture),
                    OpNumber = "105936",
                    ReceiptNumber = "2308-011-043010",
                    Lines = new List<Line>
                    {
                        new Line
                        {
                            Id = Guid.NewGuid().ToString(),
                            Units = 1,
                            Item = products[0],
                        },
                        new Line
                        {
                            Id = Guid.NewGuid().ToString(),
                            Units = 4,
                            Item = products[1],
                        },
                    },
                    Price = 100.0
                },
            };

            foreach (var item in mockItems)
            {
                items.Add(item);
            }
        }

        public async Task<bool> AddItemAsync(Item item)
        {
            items.Add(item);

            return await Task.FromResult(true);
        }

        public async Task<bool> UpdateItemAsync(Item item)
        {
            var oldItem = items.Where((Item arg) => arg.Id == item.Id).FirstOrDefault();
            items.Remove(oldItem);
            items.Add(item);

            return await Task.FromResult(true);
        }

        public async Task<bool> DeleteItemAsync(string id)
        {
            var oldItem = items.Where((Item arg) => arg.Id == id).FirstOrDefault();
            items.Remove(oldItem);

            return await Task.FromResult(true);
        }

        public async Task<Item> GetItemAsync(string id)
        {
            return await Task.FromResult(items.FirstOrDefault(s => s.Id == id));
        }

        public async Task<IEnumerable<Item>> GetItemsAsync(string type, bool forceRefresh = false)
        {
            List<Item> its;
            if (type == "tickets")
            {
                its = new List<Item>( this.items );
            }
            else
            {
                its = new List<Item>((this.items[0] as Ticket).Lines);
            }
            
            return await Task.FromResult(its);
        }
    }
}