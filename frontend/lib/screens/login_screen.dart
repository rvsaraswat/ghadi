import 'package:flutter/material.dart';

import '../models/domain.dart';
import '../services/api_client.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key, required this.api, required this.onAuthenticated});
  final ApiClient api;
  final VoidCallback onAuthenticated;
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _form = GlobalKey<FormState>();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _name = TextEditingController();
  bool _register = false;
  bool _busy = false;
  String? _error;
  @override
  void dispose() { _email.dispose(); _password.dispose(); _name.dispose(); super.dispose(); }
  Future<void> _submit() async {
    if (!_form.currentState!.validate()) return;
    setState(() { _busy = true; _error = null; });
    try {
      if (_register) await widget.api.register(_email.text.trim(), _password.text, _name.text.trim()); else await widget.api.login(_email.text.trim(), _password.text);
      if (mounted) widget.onAuthenticated();
    } on ApiException catch (error) { setState(() => _error = error.message); }
    finally { if (mounted) setState(() => _busy = false); }
  }
  @override
  Widget build(BuildContext context) => Scaffold(body: SafeArea(child: Center(child: SingleChildScrollView(child: ConstrainedBox(constraints: const BoxConstraints(maxWidth: 440), child: Padding(padding: const EdgeInsets.all(28), child: Form(key: _form, child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
    Text('Ayanm', style: Theme.of(context).textTheme.displayMedium?.copyWith(color: Theme.of(context).colorScheme.primary, fontWeight: FontWeight.bold)), const SizedBox(height: 8), Text('Your living Vedic calendar', style: Theme.of(context).textTheme.titleMedium), const SizedBox(height: 36),
    if (_register) Padding(padding: const EdgeInsets.only(bottom: 14), child: TextFormField(controller: _name, decoration: const InputDecoration(labelText: 'Name', border: OutlineInputBorder()), validator: (v) => _register && (v == null || v.trim().isEmpty) ? 'Enter your name' : null)),
    TextFormField(controller: _email, keyboardType: TextInputType.emailAddress, decoration: const InputDecoration(labelText: 'Email', border: OutlineInputBorder()), validator: (v) => v != null && v.contains('@') ? null : 'Enter a valid email'), const SizedBox(height: 14),
    TextFormField(controller: _password, obscureText: true, onFieldSubmitted: (_) => _submit(), decoration: InputDecoration(labelText: 'Password', helperText: _register ? '12+ characters with upper/lowercase, number, symbol' : null, border: const OutlineInputBorder()), validator: (v) => v != null && v.isNotEmpty ? null : 'Enter your password'),
    if (_error != null) Padding(padding: const EdgeInsets.only(top: 14), child: Semantics(liveRegion: true, child: Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error))),), const SizedBox(height: 22),
    FilledButton(onPressed: _busy ? null : _submit, child: Padding(padding: const EdgeInsets.all(12), child: _busy ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator()) : Text(_register ? 'Create account' : 'Sign in'))),
    TextButton(onPressed: _busy ? null : () => setState(() { _register = !_register; _error = null; }), child: Text(_register ? 'Already have an account? Sign in' : 'New here? Create an account')),
  ]))))));
}