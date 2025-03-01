package games.apolion.webInterfaceVenmito.webInterfaceVenmito.security.config;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import org.springframework.context.annotation.Configuration;


@Converter
public class StringArrayConverter implements AttributeConverter<String[], String> {

    @Override
    public String convertToDatabaseColumn(String[] attribute) {
        return attribute == null ? null : String.join(",", attribute);
    }

    @Override
    public String[] convertToEntityAttribute(String dbData) {
        return dbData == null ? null : dbData.split(",");
    }
}
