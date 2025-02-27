package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class ItemListEntry {
    @Id
    @GeneratedValue(strategy= GenerationType.UUID)
    private String id;
    private float valueAtPurchase;
    private SaleItem item;
    private int quantity;
    private double totalValue;

    public double getTotalValue() {
        return totalValue;
    }

    public void setTotalValue(double totalValue) {
        this.totalValue = totalValue;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public float getValueAtPurchase() {
        return valueAtPurchase;
    }

    public void setValueAtPurchase(float valueAtPurchase) {
        this.valueAtPurchase = valueAtPurchase;
    }

    public SaleItem getItem() {
        return item;
    }

    public void setItem(SaleItem item) {
        this.item = item;
    }
}
