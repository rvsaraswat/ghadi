import 'package:flutter/material.dart';

import '../screens/home_screen.dart';
import '../screens/login_screen.dart';
import '../services/api_client.dart';

class GhadiApp extends StatefulWidget {
  const GhadiApp({super.key});

  @override
  State<GhadiApp> createState() => _GhadiAppState();
}

class _GhadiAppState extends State<GhadiApp> {
  final ApiClient _api = ApiClient();
  bool _authenticated = false;

  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'GHADI', debugShowCheckedModeBanner: false,
        theme: ThemeData(useMaterial3: true, fontFamily: 'Georgia', colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xffa83c22), primary: const Color(0xff8e2f1d), secondary: const Color(0xff146b63), surface: const Color(0xfffffbf5)), scaffoldBackgroundColor: const Color(0xfff7f0e5), appBarTheme: const AppBarTheme(centerTitle: false, elevation: 0)),
        home: _authenticated ? HomeScreen(api: _api, onLogout: () => setState(() { _api.clearSession(); _authenticated = false; })) : LoginScreen(api: _api, onAuthenticated: () => setState(() => _authenticated = true)),
      );
}
