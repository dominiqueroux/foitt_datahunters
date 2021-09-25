import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:flutter_svg/flutter_svg.dart' as svg;

import 'dart:async';
import 'dart:convert';

Future<ValueNetResponse> fetchValueNetResponse() async {
  return ValueNetResponse(
      beams: "",
      potential_values_found_in_db: "",
      question: "",
      question_tokenized: "",
      result: "",
      sem_ql: "",
      sql: "");
}

Future<ValueNetResponse> updateValueNetResponse_foitt(String query) async {
  var url = Uri.parse(
      'https://inference.hackzurich2021.hack-with-admin.ch/api/question/hack_zurich');

  var headers = {
    'Content-Type': 'application/json',
    "X-API-KEY": "sjNmaCtviYzXWlS"
  };
  if (query == "") {
    query = "What is the share of electric cars in 2016 for Wetzikon?";
  }
  // String query_hardcoded = "What is the share of electric cars in 2016 for Wetzikon?";

  final body = {"question": query};

  final response = await put(
    url,
    headers: headers,
    body: jsonEncode(body), // use jsonEncode()
  );

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return ValueNetResponse.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to update ValueNetResponse.');
  }
}

Future<ValueNetResponse> updateValueNetResponse_team(String query) async {
  var headers = {
    'Content-Type': 'text/plain',
    'Accept': '*/*',
    'Host': 'localhost:5000',
  };
  if (query == "") {
    query = "What is the share of electric cars in 2016 for Wetzikon?";
  }
  var query_json = {'question': query};

  final uri = 'http://localhost:5000' + '/ask?question=' + query;

  Response response = await get(Uri.parse(uri));
  // var encoded = Uri('http://localhost:5000/hello');
  // print(encoded);

  // final response = await http.get(url);
  print('\n\n\n\n\n');
  print(response);
  print(response.statusCode);
  print('\n\n\n\n\n');

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return ValueNetResponse.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to update ValueNetResponse.');
  }
}

class ValueNetResponse {
  final String beams;
  final String potential_values_found_in_db;
  final String question;
  final String question_tokenized;
  final String result;
  final String sem_ql;
  final String sql;

  ValueNetResponse(
      {required this.beams,
      required this.potential_values_found_in_db,
      required this.question,
      required this.question_tokenized,
      required this.result,
      required this.sem_ql,
      required this.sql});

  factory ValueNetResponse.fromJson(Map<String, dynamic> json) {
    return ValueNetResponse(
      beams: json['beams'].toString(),
      potential_values_found_in_db:
          json['potential_values_found_in_db'].toString(),
      question: json['question'].toString(),
      question_tokenized: json['question_tokenized'].toString(),
      result: json['result'].toString(),
      sem_ql: json['sem_ql'].toString(),
      sql: json['sql'].toString(),
    );
  }
}

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  _MyAppState createState() {
    return _MyAppState();
  }
}

class _MyAppState extends State<MyApp> {
  final TextEditingController _controller = TextEditingController();
  late Future<ValueNetResponse> _futureValueNetResponse;

  @override
  void initState() {
    super.initState();
    _futureValueNetResponse = fetchValueNetResponse();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Update Data Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Data Hunters finding insights about Switzerland'),
        ),
        body: Container(
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8.0),
          child: FutureBuilder<ValueNetResponse>(
            future: _futureValueNetResponse,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                if (snapshot.hasData) {
                  return Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text(snapshot.data!.sql),
                      TextField(
                        controller: _controller,
                        decoration: const InputDecoration(
                          hintText: 'Enter Query for ValueNet',
                        ),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          setState(() {
                            _futureValueNetResponse =
                                updateValueNetResponse_team(_controller.text);
                          });
                        },
                        child: const Text('Run Query'),
                      ),
                    ],
                  );
                } else if (snapshot.hasError) {
                  return Text('${snapshot.error}');
                }
              }

              return const CircularProgressIndicator();
            },
          ),
        ),
      ),
    );
  }
}
