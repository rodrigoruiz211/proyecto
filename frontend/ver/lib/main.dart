import 'package:flutter/material.dart';
import 'home_page.dart';

void main() {
	runApp(const MyApp());
}

class MyApp extends StatelessWidget {
	const MyApp({super.key});

	static const Color mintGreen = Color(0xFF98FFB3);

	@override
	Widget build(BuildContext context) {
		final colorScheme = ColorScheme.fromSeed(seedColor: mintGreen);

		return MaterialApp(
			title: 'Ocular - Demo',
			theme: ThemeData(
				colorScheme: colorScheme,
				useMaterial3: true,
			scaffoldBackgroundColor: colorScheme.surface,
				appBarTheme: AppBarTheme(
					backgroundColor: mintGreen,
					foregroundColor: Colors.black87,
					elevation: 0,
				),
				elevatedButtonTheme: ElevatedButtonThemeData(
					style: ElevatedButton.styleFrom(
						backgroundColor: Colors.white,
						foregroundColor: Colors.black87,
						shape: RoundedRectangleBorder(
							borderRadius: BorderRadius.circular(12),
						),
						elevation: 6,
						padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 14),
					),
				),
			),
			home: const HomePage(),
		);
	}
}
