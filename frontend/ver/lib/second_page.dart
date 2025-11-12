import 'package:flutter/material.dart';

class SecondPage extends StatelessWidget {
  final String patientName;
  const SecondPage({super.key, required this.patientName});

  @override
  Widget build(BuildContext context) {
    // Cambia esta URL a la IP de tu PC si usas un dispositivo físico
    // Para Android Emulator usa 10.0.2.2
    // Para iOS Simulator usa localhost
    const backendUrl = 'http://10.0.2.2:8000/video_feed';

    return Scaffold(
      appBar: AppBar(
        title: const Text('Streaming de Mirada'),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Paciente: $patientName',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 16),

            // Contenedor para el stream
            AspectRatio(
              aspectRatio: 4 / 3,
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.black12,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.black26),
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Image.network(
                    backendUrl,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      return const Center(
                        child: Text(
                          'No se pudo cargar el stream',
                          style: TextStyle(color: Colors.red),
                        ),
                      );
                    },
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'Si la imagen no carga, revisa que tu backend esté corriendo y que la IP sea accesible.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 12, color: Colors.black54),
            ),
          ],
        ),
      ),
    );
  }
}
