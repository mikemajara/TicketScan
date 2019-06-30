using System;

namespace TicketScan.Models
{
    public class Item
    {
        public string Id { get; set; }
        public virtual string Text { get; set; }
        public virtual string Description { get; set; }

        public Item() { }
    }
}