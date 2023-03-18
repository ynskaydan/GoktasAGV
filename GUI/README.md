void addImage(int id, double x, double y) {
  String imagePath = '';
  if (id == 1) {
    imagePath = 'images/car.png';
  } else if (id == 2) {
    imagePath = 'images/flower.png';
  }
  AssetImage image = AssetImage(imagePath);
  ImageConfiguration configuration = createLocalImageConfiguration(context);
  Size imageSize = getSize(image, configuration);
  Rect rect = Rect.fromLTWH(x, y, imageSize.width, imageSize.height);
  points.add(rect.topLeft);
  setState(() {});
}# goktasgui

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

