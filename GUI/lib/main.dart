// @dart=2.9
import 'dart:async';

import 'package:flutter/material.dart';

import 'package:goktasgui/components/controller.dart';

import 'package:goktasgui/components/constants.dart';

import 'package:goktasgui/components/senario.dart';

import 'components/emergency.dart';
import 'components/mapping.dart';

void main() async {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // if (mappingState) {
    //   haritaBaslik = "Harita Oluşturuluyor...";
    //} else {
    //  haritaBaslik = "Harita oluşturuldu";
    // }
    return MaterialApp(
      title: 'Goktas AGV Control Panel',
      theme: ThemeData(
        backgroundColor: Colors.blueGrey,
        primarySwatch: Colors.lime,
      ),
      home: const MyHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var _focusNode = FocusNode();
  String _timeString;
  @override
  void initState() {
    _timeString = _formatDateTime(DateTime.now());
    Timer.periodic(Duration(seconds: 1), (Timer t) => _getTime());
    super.initState();
  }

  void _getTime() {
    final DateTime now = DateTime.now();
    final String formattedDateTime = _formatDateTime(now);
    setState(() {
      _timeString = formattedDateTime;
    });
  }

  String _formatDateTime(DateTime dateTime) {
    return "${dateTime.hour % 12}:${dateTime.minute.toString().padLeft(2, '0')}:${dateTime.second.toString().padLeft(2, '0')} ${dateTime.hour < 12 ? '' : ''}";
  }

  int keydirection = 1;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
              image: AssetImage("assets/images/background.png"),
              fit: BoxFit.cover),
        ),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(
                  "assets/images/goktas.png",
                  height: MediaQuery.of(context).size.height / 8,
                  width: MediaQuery.of(context).size.width / 10,
                )
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                MainButtons(),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Row(
                  children: [
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Row(
                          // ignore: prefer_const_literals_to_create_immutables
                          children: [
                            DataComponent(
                              contentData: EmergencyStop(),
                              subTitle: "Acil Durdurma Butonu",
                              widthSize:
                                  MediaQuery.of(context).size.width / 4 + 20,
                              heightSize:
                                  MediaQuery.of(context).size.height / 6,
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            DataComponent(
                              contentData: DataComponentContent(text: "2 m/s"),
                              subTitle: "Hız",
                              widthSize: MediaQuery.of(context).size.width / 8,
                              heightSize:
                                  MediaQuery.of(context).size.height / 6,
                            ),
                            DataComponent(
                              contentData: DataComponentContent(text: "%87"),
                              subTitle: "Batarya",
                              widthSize: MediaQuery.of(context).size.width / 8,
                              heightSize:
                                  MediaQuery.of(context).size.height / 6,
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            DataComponent(
                              subTitle: "Manuel Kontrol",
                              contentData: const Controller(),
                              widthSize:
                                  MediaQuery.of(context).size.width / 4 + 20,
                              heightSize:
                                  MediaQuery.of(context).size.height / 6,
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            Row(children: [
                              DataComponent(
                                subTitle: "Geçen Süre",
                                contentData:
                                    DataComponentContent(text: _timeString),
                                widthSize:
                                    MediaQuery.of(context).size.width / 8,
                                heightSize:
                                    MediaQuery.of(context).size.height / 6,
                              ),
                              DataComponent(
                                subTitle: "Araç Durumu",
                                contentData: VehicleStatus(),
                                widthSize:
                                    MediaQuery.of(context).size.width / 8,
                                heightSize:
                                    MediaQuery.of(context).size.height / 6,
                              ),
                            ]),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
                Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    DataComponent(
                      subTitle: "Harita",
                      contentData: Mapper(),
                      widthSize: MediaQuery.of(context).size.width / 1.8,
                      heightSize: MediaQuery.of(context).size.height / 2 + 40,
                    ),
                    DataComponent(
                      subTitle: "Senaryo",
                      contentData: EntrySenario(),
                      widthSize: MediaQuery.of(context).size.width / 1.8,
                      heightSize: MediaQuery.of(context).size.height / 6,
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
