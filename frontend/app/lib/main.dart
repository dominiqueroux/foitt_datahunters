import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'dart:async';
import 'dart:convert';

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

class SQLResponse {
  final String result;
  final String further_information;
  SQLResponse({
    required this.result,
    required this.further_information,
  });

  factory SQLResponse.fromJson(Map<String, dynamic> json) {
    return SQLResponse(
      result: json['standard_data'].toString(),
      further_information: json['further_information'].toString(),
    );
  }
}

Future<SQLResponse> fetchSQLResponse() async {
  return SQLResponse(
    result: "",
    further_information: "",
  );
}

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

Future<ValueNetResponse> updateValueNetResponse_FOITT(String query) async {
  var url = Uri.parse(
      'https://inference.hackzurich2021.hack-with-admin.ch/api/question/hack_zurich');

  var headers = {
    'Content-Type': 'application/json',
    "X-API-KEY": "sjNmaCtviYzXWlS"
  };
  if (query == "") {
    query = "What is the share of electric cars in 2017 for Kloten?";
  }
  // String query_hardcoded = "What is the share of electric cars in 2016 for Wetzikon?";

  final body = {"question": query};

  final response = await http.put(
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
  };
  if (query == "") {
    query = "What is the share of electric cars in 2017 for Kloten?";
  }

  final uri = 'http://localhost:5000' + '/ask?question=' + query;

  http.Response response = await http.get(Uri.parse(uri), headers: headers);

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

Future<SQLResponse> updateSQLResponse(String query) async {
  var headers = {
    'Content-Type': 'text/plain',
  };
  if (query == "") {
    query = "What is the share of electric cars in 2016 for Wetzikon?";
  }

  final uri = 'http://localhost:5000' + '/ask-extended?question=' + query;

  http.Response response = await http.get(Uri.parse(uri), headers: headers);

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return SQLResponse.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to update ValueNetResponse.');
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
  final TextEditingController _valuenet_controller = TextEditingController();
  final TextEditingController _sql_controller = TextEditingController();

  late Future<ValueNetResponse> _futureValueNetResponse;
  late Future<SQLResponse> _futureSQLResponse;

  @override
  void initState() {
    super.initState();
    _futureValueNetResponse = fetchValueNetResponse();
    _futureSQLResponse = fetchSQLResponse();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Swiss Open Data',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('ValueNet DEMO by Open DataHunters'),
        ),
        body: Column(
          children: [
            Container(
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
                          Text(snapshot.data!.result),
                          TextField(
                            controller: _valuenet_controller,
                            decoration: const InputDecoration(
                              hintText:
                                  "Enter Question, for example: What is the share of electric cars in 2017 for Kloten?",
                              border: OutlineInputBorder(),
                            ),
                          ),
                          ElevatedButton(
                            onPressed: () {
                              setState(() {
                                _futureValueNetResponse =
                                    updateValueNetResponse_FOITT(
                                        _valuenet_controller.text);
                              });
                            },
                            child: const Text('Ask Question'),
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
            Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.all(8.0),
              child: FutureBuilder<SQLResponse>(
                future: _futureSQLResponse,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.done) {
                    if (snapshot.hasData) {
                      return Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          Text(snapshot.data!.further_information),
                          TextField(
                            controller: _sql_controller,
                            decoration: const InputDecoration(
                              hintText:
                                  "Enter Question, for example: What is the share of electric cars in 2017 for Kloten?",
                              border: OutlineInputBorder(),
                            ),
                          ),
                          ElevatedButton(
                            onPressed: () {
                              setState(() {
                                _futureSQLResponse =
                                    updateSQLResponse(_sql_controller.text);
                              });
                            },
                            child: const Text(
                                'Get additional Informations about Question'),
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
          ],
        ),
      ),
    );
  }
}
