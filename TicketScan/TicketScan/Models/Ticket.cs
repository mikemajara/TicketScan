using System;
using System.Collections.Generic;

namespace TicketScan.Models
{
    public class Ticket : Item
    {
        public string Company { get; set; }
        public string Address { get; set; }
        public string Location { get; set; }
        public string Telephone { get; set; }
        public string TaxNumber { get; set; }
        public DateTime DateTime { get; set; }
        public string OpNumber { get; set; }
        public string ReceiptNumber { get; set; }
        public override string Description { get { return this.Company + this.Location; } }

        public List<Line> Lines { get; set; }

        public double Price { get; set; }

        public Ticket() { }

    }
}