using System;
namespace TicketScan.Models
{
    public class Line : Item
    {
        public int Units { get; set; }
        public Product Item { get; set; }
        public double Weight { get; set; }
        public double Price { get { return Item.Price * Units; } }
        public override string Description { get { return Units + " " + Item.Text + " " + Price + "€"; } }

        public Line() { }
    }
}
