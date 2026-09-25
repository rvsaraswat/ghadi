import 'package:flutter_test/flutter_test.dart';

import '../lib/models/domain.dart';

void main() {
  test('parses complete Panchanga payloads with optional solar values', () {
    final panchanga = Panchanga.fromJson({
      'date': '2026-09-24T08:00:00',
      'solar': {'sunrise': '2026-09-24T06:00:00', 'sunset': '2026-09-24T18:00:00'},
      'lunar': {'tithi_name': 'Ekadashi', 'paksha': 'Shukla', 'nakshatra_name': 'Rohini', 'yoga_name': 'Shubha', 'karana_name': 'Bava'},
      'time_windows': {'rahu_kaal_start': '2026-09-24T10:30:00', 'rahu_kaal_end': '2026-09-24T12:00:00'},
    });
    expect(panchanga.tithi, 'Ekadashi');
    expect(panchanga.sunrise, isNotNull);
    expect(panchanga.rahuEnd, isNotNull);
  });
}