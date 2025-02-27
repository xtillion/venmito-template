package games.apolion.webInterfaceVenmito.webInterfaceVenmito.utils;

import java.time.ZoneId;
import java.time.ZonedDateTime;

public class TimeZoneConverter {
    public ZonedDateTime convertFromUTC(ZonedDateTime utcDateTime, String targetTimeZone) {
        return utcDateTime.withZoneSameInstant(ZoneId.of(targetTimeZone));

    }
}
