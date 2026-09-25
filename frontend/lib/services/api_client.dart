import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/app_config.dart';
import '../models/domain.dart';

class ApiClient {
  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;
  String? _token;

  bool get isAuthenticated => _token != null;

  void clearSession() => _token = null;

  Future<void> login(String email, String password) async {
    final response = await _send(
      'POST',
      '/auth/login',
      body: {'email': email, 'password': password},
      authenticated: false,
    );
    _token = response['access_token'] as String?;
    if (_token == null || _token!.isEmpty) {
      throw const ApiException('The server did not return a session token.');
    }
  }

  Future<void> register(String email, String password, String fullName) async {
    await _send(
      'POST',
      '/auth/register',
      body: {'email': email, 'password': password, 'full_name': fullName},
      authenticated: false,
    );
    await login(email, password);
  }

  Future<VedicTime> getVedicTime() async =>
      VedicTime.fromJson(await _send('GET', '/vedic-time'));

  Future<Panchanga> getPanchanga() async =>
      Panchanga.fromJson(await _send('GET', '/panchanga'));

  Future<List<Festival>> getFestivals() async {
    final response = await _send('GET', '/festival/upcoming?days_ahead=30');
    final festivals = response['festivals'] as List<dynamic>? ?? const [];
    return festivals
        .map((item) => Festival.fromJson(item as Map<String, dynamic>))
        .toList(growable: false);
  }

  Future<void> updatePreferences({
    required double latitude,
    required double longitude,
    required String timezone,
    required String theme,
  }) =>
      _send(
        'PUT',
        '/user/preferences',
        body: {
          'location': {'latitude': latitude, 'longitude': longitude, 'timezone': timezone},
          'theme': theme,
        },
      );

  Future<Map<String, dynamic>> _send(
    String method,
    String path, {
    Map<String, dynamic>? body,
    bool authenticated = true,
  }) async {
    final uri = Uri.parse('${AppConfig.apiBaseUrl}$path');
    final headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};
    if (authenticated && _token != null) headers['Authorization'] = 'Bearer $_token';
    late http.Response response;
    try {
      response = switch (method) {
        'GET' => await _client.get(uri, headers: headers).timeout(AppConfig.requestTimeout),
        'POST' => await _client.post(uri, headers: headers, body: jsonEncode(body)).timeout(AppConfig.requestTimeout),
        'PUT' => await _client.put(uri, headers: headers, body: jsonEncode(body)).timeout(AppConfig.requestTimeout),
        _ => throw UnsupportedError('Unsupported request method: $method'),
      };
    } on Exception {
      throw const ApiException('Unable to reach Ayanm. Check your connection and try again.');
    }
    final decoded = response.body.isEmpty ? <String, dynamic>{} : jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode < 200 || response.statusCode >= 300) {
      final error = decoded['error'] as Map<String, dynamic>?;
      final detail = error?['message'] ?? decoded['detail'] ?? 'Request failed.';
      throw ApiException(detail.toString(), statusCode: response.statusCode);
    }
    return decoded;
  }
}