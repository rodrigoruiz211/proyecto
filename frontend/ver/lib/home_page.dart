import 'dart:async';

import 'package:flutter/material.dart';
import 'second_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _controller = TextEditingController();
  String _patientName = '';

  @override
  void initState() {
    super.initState();
    _controller.addListener(() {
      setState(() => _patientName = _controller.text.trim());
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Ocular'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  'Bienvenido familiar de:',
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 12),

                // Input for patient name
                TextField(
                  controller: _controller,
                  decoration: InputDecoration(
                    hintText: 'Escribe el nombre del paciente',
                    filled: true,
                    fillColor: Colors.white,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    suffixIcon: const Icon(Icons.person),
                  ),
                ),

                const SizedBox(height: 18),

                // Large animated eye
                const AnimatedBlinkingEye(size: 120),
                const SizedBox(height: 18),

                // Row with two eye icons
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.remove_red_eye, size: 36),
                    SizedBox(width: 20),
                    Icon(Icons.visibility_off, size: 36),
                  ],
                ),

                const SizedBox(height: 20),
                Text(
                  _patientName.isEmpty
                    ? 'Una app simple e intuitiva. Pulsa "Iniciar" para continuar.'
                    : 'Paciente: $_patientName',
                  textAlign: TextAlign.center,
                ),

                const SizedBox(height: 18),

                ElevatedButton(
                  onPressed: _patientName.isEmpty
                    ? null
                    : () {
                      Navigator.of(context).push(
                        MaterialPageRoute(builder: (_) => SecondPage(patientName: _patientName)),
                      );
                    },
                  child: const Text('Iniciar', style: TextStyle(fontSize: 18)),
                ),

                const SizedBox(height: 12),

                // Small hint
                SizedBox(
                  width: size.width * 0.7,
                  child: const Text(
                    'Iconos claros, diseño espacioso y colores suaves para reducir la fatiga visual.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 12, color: Colors.black54),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class AnimatedBlinkingEye extends StatefulWidget {
  final double size;
  const AnimatedBlinkingEye({super.key, this.size = 80});

  @override
  State<AnimatedBlinkingEye> createState() => _AnimatedBlinkingEyeState();
}

class _AnimatedBlinkingEyeState extends State<AnimatedBlinkingEye> {
  bool _open = true;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _startBlinkTimer();
  }

  void _startBlinkTimer() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 3), (Timer t) {
      setState(() => _open = false);
      // small delay to simulate blink
      Future.delayed(const Duration(milliseconds: 220), () {
        if (mounted) setState(() => _open = true);
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        // Tap to toggle immediately
        setState(() => _open = !_open);
        _startBlinkTimer();
      },
      child: AnimatedSwitcher(
        duration: const Duration(milliseconds: 200),
        transitionBuilder: (child, animation) {
          return ScaleTransition(scale: animation, child: child);
        },
        child: _open
            ? Icon(Icons.remove_red_eye, key: const ValueKey('open'), size: widget.size)
            : Icon(Icons.visibility_off, key: const ValueKey('closed'), size: widget.size),
      ),
    );
  }
}
