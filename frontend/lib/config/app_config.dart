class AppConfig {
  const AppConfig._();

  static const apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:28000',
  );

  static const requestTimeout = Duration(seconds: 15);
}