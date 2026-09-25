class ApiException implements Exception {
  const ApiException(this.message, {this.statusCode});

  final String message;
  final int? statusCode;
}

class VedicTime {
  const VedicTime({
    required this.currentTime,
    required this.tithi,
    required this.nakshatra,
    required this.yoga,
    required this.karana,
    this.sunrise,
    this.sunset,
  });

  final DateTime currentTime;
  final String tithi;
  final String nakshatra;
  final String yoga;
  final String karana;
  final DateTime? sunrise;
  final DateTime? sunset;

  factory VedicTime.fromJson(Map<String, dynamic> json) => VedicTime(
        currentTime: DateTime.parse(json['current_time'] as String),
        tithi: json['tithi_name'] as String? ?? 'Unavailable',
        nakshatra: json['nakshatra_name'] as String? ?? 'Unavailable',
        yoga: json['yoga_name'] as String? ?? 'Unavailable',
        karana: json['karana_name'] as String? ?? 'Unavailable',
        sunrise: _date(json['sunrise']),
        sunset: _date(json['sunset']),
      );
}

class Panchanga {
  const Panchanga({
    required this.date,
    required this.tithi,
    required this.nakshatra,
    required this.yoga,
    required this.karana,
    required this.paksha,
    this.sunrise,
    this.sunset,
    this.rahuStart,
    this.rahuEnd,
  });

  final DateTime date;
  final String tithi;
  final String nakshatra;
  final String yoga;
  final String karana;
  final String paksha;
  final DateTime? sunrise;
  final DateTime? sunset;
  final DateTime? rahuStart;
  final DateTime? rahuEnd;

  factory Panchanga.fromJson(Map<String, dynamic> json) {
    final lunar = json['lunar'] as Map<String, dynamic>? ?? const {};
    final solar = json['solar'] as Map<String, dynamic>? ?? const {};
    final windows = json['time_windows'] as Map<String, dynamic>? ?? const {};
    return Panchanga(
      date: DateTime.parse(json['date'] as String),
      tithi: lunar['tithi_name'] as String? ?? 'Unavailable',
      nakshatra: lunar['nakshatra_name'] as String? ?? 'Unavailable',
      yoga: lunar['yoga_name'] as String? ?? 'Unavailable',
      karana: lunar['karana_name'] as String? ?? 'Unavailable',
      paksha: lunar['paksha'] as String? ?? '',
      sunrise: _date(solar['sunrise']),
      sunset: _date(solar['sunset']),
      rahuStart: _date(windows['rahu_kaal_start']),
      rahuEnd: _date(windows['rahu_kaal_end']),
    );
  }
}

class Festival {
  const Festival({required this.name, required this.date, this.significance});

  final String name;
  final DateTime date;
  final String? significance;

  factory Festival.fromJson(Map<String, dynamic> json) => Festival(
        name: json['name'] as String,
        date: DateTime.parse(json['date'] as String),
        significance: json['significance'] as String?,
      );
}

DateTime? _date(Object? value) => value is String ? DateTime.tryParse(value) : null;