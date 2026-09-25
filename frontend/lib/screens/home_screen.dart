import 'package:flutter/material.dart';
import '../models/domain.dart';
import '../services/api_client.dart';
import '../widgets/async_state.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key, required this.api, required this.onLogout});
  final ApiClient api;
  final VoidCallback onLogout;
  @override State<HomeScreen> createState() => _HomeScreenState();
}
class _HomeScreenState extends State<HomeScreen> {
  int _tab = 0;
  late Future<_Data> _data;
  @override void initState() { super.initState(); _reload(); }
  void _reload() => setState(() => _data = Future.wait([widget.api.getVedicTime(), widget.api.getPanchanga(), widget.api.getFestivals()]).then((v) => _Data(v[0] as VedicTime, v[1] as Panchanga, v[2] as List<Festival>)));
  @override Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Ayanm'), actions: [IconButton(tooltip: 'Refresh', onPressed: _reload, icon: const Icon(Icons.refresh)), IconButton(tooltip: 'Sign out', onPressed: widget.onLogout, icon: const Icon(Icons.logout))]),
    body: FutureBuilder<_Data>(future: _data, builder: (context, snapshot) { if (snapshot.connectionState != ConnectionState.done) return const LoadingState(); if (snapshot.hasError) return ErrorState(message: snapshot.error.toString().replaceFirst('Exception: ', ''), onRetry: _reload); final data = snapshot.data!; return IndexedStack(index: _tab, children: [_Dashboard(data: data), _PanchangaView(data: data.panchanga), _FestivalView(festivals: data.festivals), _Settings(api: widget.api)]); }),
    bottomNavigationBar: NavigationBar(selectedIndex: _tab, onDestinationSelected: (v) => setState(() => _tab = v), destinations: const [NavigationDestination(icon: Icon(Icons.wb_sunny_outlined), label: 'Today'), NavigationDestination(icon: Icon(Icons.calendar_month_outlined), label: 'Panchanga'), NavigationDestination(icon: Icon(Icons.celebration_outlined), label: 'Festivals'), NavigationDestination(icon: Icon(Icons.tune), label: 'Settings')]),
  );
}
class _Data { const _Data(this.vedic, this.panchanga, this.festivals); final VedicTime vedic; final Panchanga panchanga; final List<Festival> festivals; }
class _Dashboard extends StatelessWidget { const _Dashboard({required this.data}); final _Data data; @override Widget build(BuildContext context) => RefreshIndicator(onRefresh: () async {}, child: ListView(padding: const EdgeInsets.all(20), children: [Text('Today in Vedic time', style: Theme.of(context).textTheme.headlineSmall), const SizedBox(height: 6), Text('${data.panchanga.tithi} ${data.panchanga.paksha} Paksha'), const SizedBox(height: 20), _HeroCard(vedic: data.vedic), const SizedBox(height: 20), LayoutBuilder(builder: (context, c) { final width = c.maxWidth > 700 ? (c.maxWidth - 12) / 2 : c.maxWidth; return Wrap(spacing: 12, runSpacing: 12, children: [_FactCard(width, 'Tithi', data.panchanga.tithi), _FactCard(width, 'Nakshatra', data.panchanga.nakshatra), _FactCard(width, 'Yoga', data.panchanga.yoga), _FactCard(width, 'Karana', data.panchanga.karana)]); }), const SizedBox(height: 28), Text('Coming up', style: Theme.of(context).textTheme.titleLarge), const SizedBox(height: 10), if (data.festivals.isEmpty) const Text('No festivals in the next 30 days.') else ...data.festivals.take(3).map((f) => ListTile(contentPadding: EdgeInsets.zero, leading: const CircleAvatar(child: Icon(Icons.celebration_outlined)), title: Text(f.name), subtitle: Text(_date(f.date)))),])); }
class _HeroCard extends StatelessWidget { const _HeroCard({required this.vedic}); final VedicTime vedic; @override Widget build(BuildContext context) => Card(color: Theme.of(context).colorScheme.primaryContainer, child: Padding(padding: const EdgeInsets.all(22), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text('Current alignment', style: Theme.of(context).textTheme.titleMedium), const SizedBox(height: 8), Text(vedic.tithi, style: Theme.of(context).textTheme.headlineMedium), const SizedBox(height: 8), Text('${vedic.nakshatra} · ${vedic.yoga} · ${vedic.karana}')]))); }
class _FactCard extends StatelessWidget { const _FactCard(this.width, this.label, this.value); final double width; final String label, value; @override Widget build(BuildContext context) => SizedBox(width: width, child: Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(label, style: Theme.of(context).textTheme.labelLarge), const SizedBox(height: 8), Text(value, style: Theme.of(context).textTheme.titleMedium)])))); }
class _PanchangaView extends StatelessWidget { const _PanchangaView({required this.data}); final Panchanga data; @override Widget build(BuildContext context) => ListView(padding: const EdgeInsets.all(20), children: [Text('Panchanga', style: Theme.of(context).textTheme.headlineSmall), const SizedBox(height: 18), _FactCard(double.infinity, 'Tithi', '${data.tithi} · ${data.paksha}'), const SizedBox(height: 12), _FactCard(double.infinity, 'Nakshatra', data.nakshatra), const SizedBox(height: 12), _FactCard(double.infinity, 'Yoga', data.yoga), const SizedBox(height: 12), _FactCard(double.infinity, 'Karana', data.karana), const SizedBox(height: 22), Text('Solar rhythm', style: Theme.of(context).textTheme.titleLarge), ListTile(title: const Text('Sunrise'), trailing: Text(_time(data.sunrise))), ListTile(title: const Text('Sunset'), trailing: Text(_time(data.sunset))), ListTile(title: const Text('Rahu Kaal'), trailing: Text('${_time(data.rahuStart)} - ${_time(data.rahuEnd)}'))]); }
class _FestivalView extends StatelessWidget {
  const _FestivalView({required this.festivals});

  final List<Festival> festivals;

  @override
  Widget build(BuildContext context) => ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text('Festivals', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 18),
          if (festivals.isEmpty)
            const Padding(
              padding: EdgeInsets.only(top: 48),
              child: Center(child: Text('No upcoming festivals yet.')),
            )
          else
            ...festivals.map(
              (festival) => Card(
                margin: const EdgeInsets.only(bottom: 10),
                child: ListTile(
                  leading: const Icon(Icons.celebration_outlined),
                  title: Text(festival.name),
                  subtitle: Text(festival.significance ?? _date(festival.date)),
                  trailing: Text(_date(festival.date)),
                ),
              ),
            ),
        ],
      );
}
class _Settings extends StatefulWidget { const _Settings({required this.api}); final ApiClient api; @override State<_Settings> createState() => _SettingsState(); }
class _SettingsState extends State<_Settings> { final _lat = TextEditingController(text: '28.6139'); final _lng = TextEditingController(text: '77.2090'); bool _busy = false; String? _message; @override void dispose() { _lat.dispose(); _lng.dispose(); super.dispose(); } Future<void> _save() async { final lat = double.tryParse(_lat.text); final lng = double.tryParse(_lng.text); if (lat == null || lng == null) { setState(() => _message = 'Enter valid coordinates.'); return; } setState(() { _busy = true; _message = null; }); try { await widget.api.updatePreferences(latitude: lat, longitude: lng, timezone: 'Asia/Kolkata', theme: 'light'); setState(() => _message = 'Location saved.'); } on ApiException catch (e) { setState(() => _message = e.message); } finally { if (mounted) setState(() => _busy = false); } } @override Widget build(BuildContext context) => ListView(padding: const EdgeInsets.all(20), children: [Text('Settings', style: Theme.of(context).textTheme.headlineSmall), const SizedBox(height: 20), TextField(controller: _lat, keyboardType: const TextInputType.numberWithOptions(decimal: true, signed: true), decoration: const InputDecoration(labelText: 'Latitude', border: OutlineInputBorder())), const SizedBox(height: 12), TextField(controller: _lng, keyboardType: const TextInputType.numberWithOptions(decimal: true, signed: true), decoration: const InputDecoration(labelText: 'Longitude', border: OutlineInputBorder())), const SizedBox(height: 12), const Text('Timezone: Asia/Kolkata'), const SizedBox(height: 18), FilledButton(onPressed: _busy ? null : _save, child: Text(_busy ? 'Saving...' : 'Save location')), if (_message != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_message!))]); }
String _time(DateTime? value) => value == null ? 'Unavailable' : '${value.hour.toString().padLeft(2, '0')}:${value.minute.toString().padLeft(2, '0')}';
String _date(DateTime value) => '${value.day.toString().padLeft(2, '0')}/${value.month.toString().padLeft(2, '0')}/${value.year}';
