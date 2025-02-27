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
